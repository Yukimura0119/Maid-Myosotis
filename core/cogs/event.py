import discord
from discord.ext import commands
from discord.ext.commands import errors
from core.ext import cog_ext
import json

with open('data/settings.json', 'r', encoding='utf8') as SettingFile:
    sf = json.load(SettingFile)


class Event(cog_ext):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch = member.guild.system_channel
        if ch is None:
            ch = member.guild.text_channels[0]
        await ch.send(f'```\n{member} Ya Hello!\n```')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = member.guild.system_channel
        if ch is None:
            ch = member.guild.text_channels[0]
        await ch.send(f'```\n{member} Bye Bye!\n```')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.lower() == 'yukitan' and msg.author != self.bot.user:
            await msg.channel.send('```\nNani?\n```')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if hasattr(ctx.command, 'on_error'):
            return
        await ctx.send(f'```\n{err}\n```')


def setup(bot):
    bot.add_cog(Event(bot))
