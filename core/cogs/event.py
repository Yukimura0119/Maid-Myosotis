import discord
from discord.ext import commands
from discord.ext.commands import errors
from core.ext import Cog_ext
import os
import json


with open('data/settings.json', 'r', encoding='utf8') as settingfile:
    db = json.load(settingfile)


class Event(Cog_ext):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(db['Channel-ID'])
        await channel.send(f'{member} Ya Hello!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(db['Channel-ID'])
        await channel.send(f'{member} Bye Bye!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.lower() == 'yukitan' and msg.author != self.bot.user:
            await msg.channel.send('Nani?')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if hasattr(ctx.command, 'on_error'):
            return
        await ctx.send(err)


def setup(bot):
    bot.add_cog(Event(bot))
