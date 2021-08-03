import discord
from discord.ext import commands
from core.ext import cog_ext
from pathlib import Path
import random


class React(cog_ext):
    @commands.command()
    async def pic(self, ctx):
        pic = discord.File(random.choice(
            [p for p in Path(".").glob("./data/picture/*")]))
        await ctx.send(file=pic)


def setup(bot):
    bot.add_cog(React(bot))
