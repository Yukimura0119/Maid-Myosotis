import discord
from discord.ext import commands

from pathlib import Path
import json


with open('data/setting/secret.json', 'r', encoding='utf8') as jdata:
    secret = json.load(jdata)

bot = commands.Bot(command_prefix='$', case_insensitive=True,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    bot.client_id = (await bot.application_info()).id
    print('>> YuKiTaN is on service <<')


@bot.event
async def on_connect():
    print(
        f'YuKiTaN connected to Discord (latency: {round(bot.latency*1000)} ms).')


@bot.command()
async def load(ctx, ext):
    bot.load_extension(f'core.cogs.{ext}')
    await ctx.send(f'```\n{ext} loaded successfully.\n```', delete_after=10)


@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f'core.cogs.{ext}')
    await ctx.send(f'```\n{ext} unloaded successfully.\n```')


@bot.command()
async def reload(ctx, ext):
    bot.reload_extension(f'core.cogs.{ext}')
    await ctx.send(f'```\n{ext} reloaded successfully.\n```')


@bot.command()
async def close(ctx):
    if ctx.message.author.id == int(secret['myID']):
        await ctx.send('```\nBye bye.\n```')
        await bot.close()
    else:
        await ctx.send('```\nPemission denied.(Only Yukimura0119 can use this commnad)\n```')

for cog in [p.stem for p in Path(".").glob("./core/cogs/*.py")]:
    bot.load_extension(f'core.cogs.{cog}')
    print(f'Loaded {cog}.')
print('Done.')


print('YuKiTaN starting...')
bot.run(secret['Authorization'], reconnect=True)
