import discord
from discord.ext import commands

from pathlib import Path
import json

from discord.flags import Intents


class YuKiTaN(commands.Bot):
    def __init__(self):
        # p.stem can remove profix
        self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        super().__init__(command_prefix='$',
                         case_insensitive=True, intents=discord.Intents.all())

    def setup(self):
        print('Loading cogs...')

        for cog in self._cogs:
            self.load_extension(f'core.cogs.{cog}')
            print(f'Loaded {cog}.')
        print('Done.')

    def run(self):
        self.setup()

        with open('data/settings.json', 'r', encoding='utf8') as SettingFile:
            sf = json.load(SettingFile)

        print('YuKiTaN starting...')
        super().run(sf['Authorization'], reconnect=True)

    async def shutdown(self):
        print('YuKiTaN closing...')
        await super().close()
        print('Done.')

    async def close(self):
        print('YuKiTaN interrupted.')
        await self.shutdown()

    async def on_connect(self):
        print(
            f'YuKiTaN connected to Discord (latency: {round(self.latency*1000)} ms).')

    async def on_resumed(self):
        print('YuKiTaN resumed.')

    async def on_disconnect(self):
        print('YuKiTaN disconnected.')

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, 'original', exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print('>> YuKiTaN is on service <<')

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or('$')(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)


@commands.command()
async def load(self, ctx, ext):
    self.load_extension(f'cog.{ext}')
    await ctx.send(f'{ext} loaded successfully.')


@commands.command()
async def unload(self, ctx, ext):
    self.unload_extension(f'cog.{ext}')
    await ctx.send(f'{ext} unloaded successfully.')


@commands.command()
async def reload(self, ctx, ext):
    self.reload_extension(f'cog.{ext}')
    await ctx.send(f'{ext} reloaded successfully.')
