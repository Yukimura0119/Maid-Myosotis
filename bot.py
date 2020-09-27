import discord
from discord.ext import commands
import json

with open('setting.json', 'r', encoding='utf8') as settingfile:
    settingdata = json.load(settingfile)

    
bot = commands.Bot(command_prefix='ykt ')

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(settingdata['EntranceChannelID'])
    await channel.send(f'{member} Ya Hello!')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(settingdata['EntranceChannelID'])
    await channel.send(f'{member} Bye Bye!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}ms')


bot.run(settingdata['token'])

