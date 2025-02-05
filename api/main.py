from sys import builtin_module_names
import discord
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
import pytz
import json
import os
import aiohttp
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)
async def on_ready():
    print(f"Logged in as {bot.user}")

TOKEN = os.getenv("Discord_bot_token")
DEVLOG_FILE = "devlog.json"
LOGS_PER_PAGE = 5
VALID_PROJECTS = ["fluorez", "dead_dreams"]
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"  # Stable Diffusion model
OPENAI_API_KEY= ""

client = commands.Bot(command_prefix=",", help_command=None, intents=intents)

#Prefix Defining
@client.event
async def on_ready():
  print("Bot is working.")

def ensure_devlog_file():
    if not os.path.exists(DEVLOG_FILE) or os.stat(DEVLOG_FILE).st_size == 0:
        with open(DEVLOG_FILE, "w") as f:
            json.dump([], f, indent=4)

#Just a testing command
@client.command()
async def hi(ctx):
  await ctx.send("Hello!")

if not os.path.exists(DEVLOG_FILE):
    with open(DEVLOG_FILE, "w") as f:
        json.dump([], f, indent=4)

#1- once ",hello" is sent, the bot tell that it is online.
@client.command(name="online", aliases=["working", "up", "on"])
async def online(ctx):
  await ctx.send("Hi, the bot is functioning correctly.")


#2- rules command
@client.command(name="rules",
                aliases=["rule", "RULES", "Rules", "RULE", "Rule"])
async def rules(ctx):
  embed = discord.Embed(
    title="Rules", description="**📌 Server Rules**", color=discord.Color.blue())
  embed.set_author(name="Retro Palm Studios")
  embed.add_field(name="📜 **__General Rules__**",
                  value=(
                     "\n"
                     "1️⃣ **Respect Everyone** – No harassment, hate speech, racism, sexism, or personal attacks. Treat everyone with respect.\n"
                     "2️⃣ **No NSFW Content** – This includes media, links, and discussions. Keep it clean.\n"
                     "3️⃣ **No Spamming** – Avoid excessive messages, emojis, or mentions.\n"
                     "4️⃣ **No Sharing Private Information** – Do not share personal details without consent.\n"
                     "4️⃣ **Keep It Relevant** – Stay on topic in each channel. Random discussions go in designated channels.\n"
                     "5️⃣ **No Drama or Toxicity** – Keep arguments private. Don't bring unnecessary negativity into the server.\n"
                     "6️⃣ **No Doxxing or Personal Info** – Do not share anyone's personal details without consent.\n"
                  ),
    inline=False)
  embed.add_field(name="🚫 **__Security & Safety__**",
                  value=(
                     "\n"
                     "7️⃣ **No Impersonation** – Don’t pretend to be staff, another user, or a well-known figure.\n"
                     "8️⃣ **No Hacking, Piracy, or Illegal Activities** – Discussions or links related to hacking, pirated software, or anything illegal are strictly forbidden.\n"
                     "9️⃣ **Follow Discord's [TOS](https://discord.com/terms) & [Guidlines](https://discord.com/guidelines)** - If Discord doesn’t allow it, we don’t either.\n"),
                  inline=False)
  embed.add_field(name="⚖ **__Moderation & Conduct__**",
                  value=(
                  "🔹 **Listen to Mods & Admins** – If a mod asks you to stop doing something, listen to them. Repeated violations may lead to bans.\n"
                  "🔹 **Use Common Sense** – If you think something might break the rules, it probably does. Don’t test the limits."
                  ),
                  inline=False)
  embed.set_footer(
    text="Enjoy your experience in our server!")
  await ctx.send(embed=embed)


#3- purge command
@client.command(name="clear", aliases=["delete", "remove", "purge", "del"])
@commands.has_permissions(manage_messages=True)
async def Clear(ctx, amount=2):
  await ctx.channel.purge(limit=amount)

current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

#4- kick commands
@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  if reason == None:
    reason = " NO REASON PROVIDED"
  embed = discord.Embed(
    title="USER KICKED", color=discord.Color.blue()
  )
  embed.set_author(name=member.name, icon_url=member.avatar)
  embed.add_field(
    name="Details",
    value=(
        f"**User Kicked:** {member.mention}\n"
        f"**Moderator:** {ctx.author.mention}\n"
        f"**Reason provided:** {reason}\n"
        f"**Kicked on:** {time}"
    ),
    inline=False
)
  await ctx.guild.kick(member)
  kick_log = client.get_channel(887292002499182612)
  await kick_log.send(embed=embed)

@client.command(name="Time")
async def time(ctx):
   await ctx.send(time)

#5- ban command
@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  if reason == None:
    reason = " NO REASON PROVIDED"
  embed = discord.Embed(
    title="USER BANNED", color=discord.Color.blue()
  )
  embed.set_author(name=member.name, icon_url=member.avatar)
  embed.add_field(
    name="Details",
    value=(
        f"**User Banned:** {member.mention}\n"
        f"**Moderator:** {ctx.author.mention}\n"
        f"**Reason provided:** {reason}\n"
        f"**Kicked on:** {time}"
    ),
    inline=False
)
  await member.ban(reason=reason)
  ban_log = client.get_channel(887292002499182612)
  await ban_log.send(embed=embed)


#6- meme command
@client.command(name="meme", aliases=["MEME", "memer", "emem", "meem", "emme"])
async def meme(ctx):
    async def fetch_meme():
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    meme_data = await fetch_meme()
    if meme_data is None:
        await ctx.send("Failed to fetch a meme. Please try again later!")
        return

    meme_url = meme_data["url"]
    meme_title = meme_data["title"]
    meme_author = meme_data["author"]
    meme_subreddit = meme_data["subreddit"]
    meme_postlink = meme_data["postLink"]

    # Create an embed for the meme
    embed = discord.Embed(title=meme_title, color=discord.Color.blue())
    embed.set_image(url=meme_url)
    embed.set_footer(
        text=f"Meme by: {meme_author} | Subreddit: {meme_subreddit} | [Post Link]{meme_postlink}"
    )

    # Define the "More" button
    class MoreMemeView(View):
        @discord.ui.button(label="More", style=discord.ButtonStyle.primary)
        async def more_button(self, interaction: discord.Interaction, button: Button):
            meme_data = await fetch_meme()
            if meme_data is None:
                await interaction.response.send_message(
                    "Failed to fetch a meme. Please try again later!", ephemeral=True
                )
                return

            # Update the embed with a new meme
            new_embed = discord.Embed(
                title=meme_data["title"], color=discord.Color.blue()
            )
            new_embed.set_image(url=meme_data["url"])
            new_embed.set_footer(
                text=f"Meme by: {meme_data['author']} | Subreddit: {meme_data['subreddit']} | [Post Link]({meme_data['postLink']})"
            )
            await interaction.response.edit_message(embed=new_embed, view=self)

    # Send the initial embed with the "More" button
    await ctx.send(embed=embed, view=MoreMemeView())


#7- games command
@client.command(name="games",
                aliases=["Games", "GAMES", "Game", "game", "GAME", "gamelist"])
async def games(ctx):
  embed = discord.Embed(
    title="Games",
    description="These are all the games we have released/plan to release.", color=discord.Color.blue()
  )
  embed.set_author(name="Retro Palm Studios")
  embed.add_field(name="__1. Dead Dreams__",
                  value=("Genre: Horror\n"
                         "Status: UnReleased\n"
                         "Release Date: TBA (Demo: Early 2025)\n"
                         "Condition: Under Development\n"
                         "Description:\n\n"
                         "Dead Dreams is our current project, which is a FNAF fan game. It features two styles of gameplay - The regular FNAF style sections (You have cameras, you close doors, etc.), and the Free Roam section, which is the main feature of this game. The game will feature its own unique storyline, as well as wide variety of mechanics.\n")
  )
  embed.set_footer(
    text=
    "Thanks for reading! Please support us by playing our games and giving us feedbacks."
  )
  await ctx.send(embed=embed)

#8- Help Command
@client.command(name="help",
                aliases=["HELP", "Help", "commands", "Commands", "COMMANDS"])
async def help(ctx):
  embed = discord.Embed(title="Commands List", color=discord.Color.blue())
  embed.set_author(name="Retro Palm Studios")
  embed.add_field(name="Syntax",
                  value=("The prefix used is `,`\n"
                        "Syntax is `,<Command name>`\n"),
                  inline=False)
  embed.add_field(name="1. Rules",
                  value=("Shows the list of rules in our server.\n"
                         "Aliases: `rules`, `rule`, `RULES`, `Rules`, `RULE`, `Rule`\n\n"
                         "Permissions required: none\n"
                         "____\n"),
                  inline=False)
  embed.add_field(name="2. Memes",
                  value=("Picks a random meme from reddit and shows it to you.\n"
                         "Aliases: `meme`, `MEME`, `memer`, `emem`, `meem`, `emme`\n\n"
                         "Permissions required: none\n"
                         "____\n"),
                  inline=False)
  embed.add_field(name="3. Games",
                  value=("Shows a list of our projects.\n"
                          "Aliases: `games`, `Games`, `GAMES`, `Game`, `game`, `GAME`, `gamelist`\n\n"
                          "Permissions required: none\n"
                          "____\n"),
                  inline=False)
  embed.add_field(name="4. Purge",
                  value=("Deletes the number of messages entered.\n"
                         "Aliases: `clear`, `delete`, `remove`, `purge`, `del`\n"
                         "Syntax: `,purge <number of messages>`\n"
                         "Permissions required: Manage_Messages\n\n"
                         "____\n"),
                  inline=False)
  embed.add_field(name="5. Kick",
                  value=("Kicks the member.\n"
                         "Aliases: `kick`\n"
                         "Syntax: `,kick <member> <reason>`\n\n"
                         "Permissions required: kick_members\n"
                         "____\n"),
                  inline=False)
  embed.add_field(name="6. Ban",
                  value=("Bans the member.\n"
                         "Aliases: `ban`\n"
                         "Syntax: `,ban <member> <reason>`\n\n"
                         "Permissions required: ban_members\n"
                         "____\n"),
                  inline=False)
  embed.set_footer(
    text="Please contact the moderators if you feel something is wrong or if you are confused."
    )
  await ctx.send(embed=embed)

#9- img gen
async def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        return None
@client.command(name="generate")
async def generate(ctx, *, prompt: str):
    await ctx.send(f"Generating an image for: `{prompt}`...")

    # Generate the image
    image_data = await generate_image(prompt)

    if image_data:
        # Save the image to file and send it back
        with open("generated_image.png", "wb") as f:
            f.write(image_data)

        await ctx.send(file=discord.File("generated_image.png"))
    else:
        await ctx.send("Failed to generate the image. Please try again later.")


# D E V L O G        

# ✅ Ensure the devlog file exists and is valid
def ensure_devlog_file():
    if not os.path.exists(DEVLOG_FILE) or os.stat(DEVLOG_FILE).st_size == 0:
        with open(DEVLOG_FILE, "w") as f:
            json.dump({}, f, indent=4)

# ✅ Get current IST time
def get_current_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime("%Y-%m-%d")

# ✅ Command to add a devlog
@client.command()
async def devlog(ctx, action: str = None, project: str = None, number: str = None, heading: str = None, *, details: str = None):
    """Handles devlog actions (Adding new logs)."""

    developer_role = discord.utils.get(ctx.guild.roles, name="Developer")
    if developer_role not in ctx.author.roles:
        await ctx.send("🚫 You need the 'Developer' role to use this command.")
        return

    if action != "add" or project not in VALID_PROJECTS or not number or not heading or not details:
        await ctx.send("⚠️ **Invalid usage!** Use:\n`,devlog add <bot/game> <number> <heading> <details>`")
        return

    ensure_devlog_file()

    with open(DEVLOG_FILE, "r") as f:
        logs = json.load(f)

    if project not in logs:
        logs[project] = []

    logs[project].append({
        "number": number,
        "heading": heading,
        "details": details,
        "author": ctx.author.name,
        "timestamp": get_current_time()
    })

    with open(DEVLOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    await ctx.send(f"✅ **Devlog {number} added successfully for {project}!**")

# ✅ Pagination with Buttons
class DevlogView(discord.ui.View):
    def __init__(self, logs, project, page, total_pages):
        super().__init__()
        self.logs = logs
        self.project = project
        self.page = page
        self.total_pages = total_pages

    async def update_embed(self, interaction):
        start_idx = (self.page - 1) * LOGS_PER_PAGE
        end_idx = start_idx + LOGS_PER_PAGE
        logs_to_display = self.logs[::-1][start_idx:end_idx]

        embed = discord.Embed(title=f"🛠️ {self.project.upper()} Development Logs (Page {self.page}/{self.total_pages})", color=discord.Color.blue())

        for log in logs_to_display:
            embed.add_field(
                name=f"📌 {log['number']} - {log['heading']} ({log['timestamp']})",
                value=f"**Details:**\n{log['details']}\n\n**Author:** {log['author']}",
                inline=False
            )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️ Prev", style=discord.ButtonStyle.primary)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.total_pages:
            self.page += 1
            await self.update_embed(interaction)

# ✅ Command to view paginated devlogs (With Buttons)
@client.command()
async def devlogs(ctx, project: str = None):
    """Displays development logs for a specific project with pagination buttons."""

    if project not in VALID_PROJECTS:
        await ctx.send(f"⚠️ **Invalid project!** Choose from: {', '.join(VALID_PROJECTS)}\nUsage: `,devlogs fluorez` or `,devlogs dead_dreams`")
        return

    ensure_devlog_file()

    with open(DEVLOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("⚠️ Error: Devlog file is corrupted! Resetting...")
            with open(DEVLOG_FILE, "w") as reset_file:
                json.dump({}, reset_file, indent=4)
            return

    if project not in logs or not logs[project]:
        await ctx.send(f"📭 No devlogs available for **{project}**!")
        return

    total_pages = max(1, (len(logs[project]) + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE)

    view = DevlogView(logs[project], project, 1, total_pages)

    # Initial Embed
    start_idx = 0
    end_idx = LOGS_PER_PAGE
    logs_to_display = logs[project][::-1][start_idx:end_idx]

    embed = discord.Embed(title=f"🛠️ {project.upper()} Development Logs (Page 1/{total_pages})", color=discord.Color.blue())

    for log in logs_to_display:
        embed.add_field(
            name=f"📌 {log['number']} - {log['heading']} ({log['timestamp']})",
            value=f"**Details:**\n{log['details']}\n\n**Author:** {log['author']}",
            inline=False
        )

    await ctx.send(embed=embed, view=view)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

client.run(TOKEN)
