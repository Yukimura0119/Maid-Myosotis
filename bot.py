import discord
from discord.ext import commands
import os
import json


with open('settings.json', 'r', encoding='utf8') as settingfile:
    db = json.load(settingfile)


bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print(">> Bot is online <<")


@bot.command()
async def load(ctx, ext):
    bot.load_extension(f'lib.{ext}')
    await ctx.send(f'{ext} loaded successfully.')


@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f'lib.{ext}')
    await ctx.send(f'{ext} unloaded successfully.')


@bot.command()
async def reload(ctx, ext):
    bot.reload_extension(f'lib.{ext}')
    await ctx.send(f'{ext} reloaded successfully.')

for filename in os.listdir(db['lib-path']):
    if(filename.endswith('.py')):
        bot.load_extension(f'lib.{filename[:-3]}')

if(__name__ == "__main__"):
    bot.run(db['Authorization'])
