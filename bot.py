import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
bot = commands.Bot(command_prefix="!", case_insensitive=True)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="test")
async def test(ctx, arg):
    await ctx.send(arg)
    
# client.run(TOKEN)
bot.run(TOKEN)

