import discord
from discord.ext import commands

from extension.cog import CogExtension
from tools import message


class Event(CogExtension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch = member.guild.system_channel
        if ch is None:
            ch = member.guild.text_channels[0]
        await ch.send(message.codeblock(f'{member} Ya Hello!'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = member.guild.system_channel
        if ch is None:
            ch = member.guild.text_channels[0]
        await ch.send(message.codeblock(f'{member} Bye Bye!'))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.lower() == 'yukitan' and msg.author != self.bot.user:
            await msg.channel.send(message.codeblock('Nani?'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if hasattr(ctx.command, 'on_error'):
            return
        await ctx.send(message.codeblock(err))


def setup(bot):
    bot.add_cog(Event(bot))
