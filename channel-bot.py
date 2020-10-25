import os

from discord.ext import commands
from dotenv import load_dotenv

def check_existing_channel(channel_name, guild):
    for existing_channel in guild.voice_channels:
        if channel_name == existing_channel.name:
            return True
    return False

        
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", case_insensitive=True)

ready_members = []
    
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="test")
async def test(ctx, arg):
    await ctx.send(arg)
    
@bot.command(name="ready")
async def get_ready(ctx):
    ready_members.append(ctx)
    if (len(ready_members) > 3):
        create_channel(ctx, arg)


async def create_channel(ctx, arg):
    print("ran this")
    valid_name_num = 0
    channel_name = arg
    while check_existing_channel(channel_name, ctx.guild):
        channel_name = arg + str(valid_name_num)
        valid_name_num += 1
    await ctx.send("Creating new voice channel: " + channel_name)
    new_channel = await ctx.guild.create_voice_channel(name=channel_name)
    await new_channel.set_permissions(bot.user, create_instant_invite=True)
    invite = await new_channel.create_invite()
    direct_message = await ctx.message.author.create_dm()
    await direct_message.send(content=invite)
    def check(*args):
        return len(new_channel.members) == 0
    await bot.wait_for('voice_state_update', check=check)
    await new_channel.delete()  


bot.run(TOKEN)

