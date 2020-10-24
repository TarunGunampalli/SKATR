import discord
intents = discord.Intents.default()
intents.members = True

from dotenv import load_dotenv
import os
load_dotenv('.env')

client = discord.Client(intents=intents)
TOKEN = os.getenv('TOKEN')

def get_member_names():
    for guild in client.guilds:
        for member in guild.members:
            yield member.name

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!members'):
        people = set(get_member_names())
        for person in people:
            await message.channel.send(person)


client.run(TOKEN)
