#!/usr/bin/python3

import os

from discord import Member

from sheetsEX import users_sheet, survey_sheet
import discord
from discord.ext import commands
from dotenv import load_dotenv
# from bot import members

# # Initializes Discord privileged gateway intents
# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)

# names = []
# ids = []
# pfp_urls = []
# members = []

# checks to see if a channel with name channel_name already exists in the guild
# the bot is currently in
def check_existing_channel(channel_name, guild):
    for existing_channel in guild.voice_channels:
        if channel_name == existing_channel.name:
            return True
    return False

# check to see if the member calling !ready has already called it
def already_ready(new_ready, ready_members):
    for ready_member in ready_members:
        if new_ready == ready_member:
            return True
    return False


# get the discord auth token from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# create the discord bot with "!" to denote commands in discord messages
bot = commands.Bot(command_prefix="!", case_insensitive=True)

# initialize empty list that will be used to store members that are currently
# ready
ready_members = []
    
# @client.event
# async def on_ready():
#     get_members()
#     # client.loop.stop()
#     # client.loop.close()

@bot.event
async def on_ready():
    print("bot ready")
    # for member in bot.get_all_members():
    #     if type(member) is Member:
    #         direct_message = await member.create_dm()
    #         await direct_message.send(content="Start setup by sending \"!name\" followed by your name")

@bot.command(name="name")
async def name(ctx, *, arg):
    id = ctx.message.author.id
    id = ctx.message.author.id
    cell = users_sheet.find(str(id))
    users_sheet.update_cell(cell.row, cell.col + 3, arg)
    await ctx.send("Thanks! Continue setup by sending \"!email\" followed by your email")

@bot.command(name="email")
async def email(ctx, arg):
    id = ctx.message.author.id
    cell = users_sheet.find(str(id))
    users_sheet.update_cell(cell.row, cell.col + 4, arg)
    await ctx.send("Thanks! Return to your server to start meeting new people!")

    
@bot.command(name="ready")
async def get_ready(ctx):
    if already_ready(ctx.message.author, ready_members):
        await ctx.send("You're already ready")
    else:
        ready_members.append(ctx.message.author)
    cell = 0
    # while (cell != 1)
    #     cell = survey_sheet.find(str(ctx.message.author.id))
    if (len(ready_members) >= 3):
        await create_channel(ctx)

@bot.command(name="cancel")
async def cancel_ready(ctx):
    if already_ready(ctx.message.author, ready_members):
        ready_members.remove(ctx.message.author)
    else:
        await ctx.send("You can't call cancel without being ready")


async def create_channel(ctx):
    valid_name_num = 0
    base_name = "Meeting Room "
    channel_name = base_name
    while check_existing_channel(channel_name, ctx.guild):
        channel_name = base_name + str(valid_name_num)
        valid_name_num += 1
    await ctx.send("Creating new voice channel: " + channel_name)
    new_channel = await ctx.guild.create_voice_channel(name=channel_name)
    await new_channel.set_permissions(bot.user, create_instant_invite=True)
    invite = await new_channel.create_invite()
    for member in ready_members:
        direct_message = await member.create_dm()
        await direct_message.send(content=invite)
    def check(*args):
        return len(new_channel.members) == 0
    await bot.wait_for('voice_state_update', check=check)
    await end_of_channel(new_channel)

async def end_of_channel(new_channel):
    await new_channel.delete()
    # new_group = await bot.user.create_group(*ready_members)
    for member in ready_members:
        direct_message = await member.create_dm()
        await direct_message.send(content="Remember to go to the BumpBot App to fill out the survey!")
        ready_members.remove(member)

    # new_group.send(content="Welcome! How was your meeting?")

bot.run(TOKEN)