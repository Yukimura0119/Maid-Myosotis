import discord
from discord.ext import commands
from core.ext import cog_ext


class Main(cog_ext):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)


def setup(bot):
    bot.add_cog(Main(bot))
