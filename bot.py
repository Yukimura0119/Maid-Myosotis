import discord
from discord.ext import commands
from discord.flags import Intents

from pathlib import Path
import json


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
    await ctx.send(f'{ext} loaded successfully.')


@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f'core.cogs.{ext}')
    await ctx.send(f'{ext} unloaded successfully.')


@bot.command()
async def reload(ctx, ext):
    bot.reload_extension(f'core.cogs.{ext}')
    await ctx.send(f'{ext} reloaded successfully.')


with open('data/settings.json', 'r', encoding='utf8') as SettingFile:
    sf = json.load(SettingFile)


for cog in [p.stem for p in Path(".").glob("./core/cogs/*.py")]:
    bot.load_extension(f'core.cogs.{cog}')
    print(f'Loaded {cog}.')
print('Done.')


print('YuKiTaN starting...')
bot.run(sf['Authorization'], reconnect=True)
