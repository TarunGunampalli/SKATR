from sheetsEX import users_sheet
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

# Discord Bot Token
load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

# Initializes Discord privileged gateway intents
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

names = []
ids = []
pfp_urls = []

bot = commands.Bot(command_prefix="!", case_insensitive=True)

# Gets all members names from servers
def get_members():
    for guild in client.guilds:
        for member in guild.members:
            names.append(member.name)
            ids.append(member.id)
            pfp_urls.append(str(member.avatar_url))


# def get_member_ids():
#     for guild in client.guilds:
#         for member in guild.members:
#             yield member.id

# Bot login initialization
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="name")
async def test(ctx, *, arg):
    await ctx.send(arg)
    id = ctx.message.author.id
    cell = users_sheet.find(str(id))
    users_sheet.update_cell(cell.row, cell.col + 2, arg)


@bot.command(name="email")
async def test(ctx, *, arg):
    await ctx.send(arg)
    id = ctx.message.author.id
    cell = users_sheet.find(str(id))
    users_sheet.update_cell(cell.row, cell.col + 3, arg)

@bot.command(name="password")
async def test(ctx, *, arg):
    await ctx.send(arg)
    id = ctx.message.author.id
    cell = users_sheet.find(str(id))
    users_sheet.update_cell(cell.row, cell.col + 4, arg)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# Populates main sheet with member names and ids
    if message.content.startswith('!populate_users'):
        get_members()
        counter = 0
        for id in ids:
            counter += 1
            users_sheet.update_cell(counter + 1, 1, str(id))
        counter = 0
        for name in names:
            counter += 1
            users_sheet.update_cell(counter + 1, 2, name)
        print(users_sheet.cell(2, 1).value)
        counter = 0
        print(pfp_urls)
        for pfp in pfp_urls:
            counter += 1
            users_sheet.update_cell(counter + 1, 3, pfp)

        await message.channel.send('Populated sheet!')

# # Populates relationship sheet with member
#     if message.content.startswith('!populate_questions'):
#         get_members()
#         counter = 0
#         for id in ids:
#             counter += 1
#             match_survey.update_cell(1, counter + 1, str(id))
#             macth_survey.update_cell(counter + 1, 1, str(id))
#             q2_sheet.update_cell(1, counter + 1, str(id))
#             q2_sheet.update_cell(counter + 1, 1, str(id))
#             q3_sheet.update_cell(1, counter + 1, str(id))
#             q3_sheet.update_cell(counter + 1, 1, str(id))

client.run(TOKEN)
