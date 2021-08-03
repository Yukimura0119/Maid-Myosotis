import discord
from discord.ext import commands
from core.ext import Cog_ext
from pathlib import Path
import random
import os


class React(Cog_ext):
    @commands.command()
    async def pic(self, ctx):
        pic = discord.File(random.choice(
            [p for p in Path(".").glob("./data/picture/*")]))
        await ctx.send(file=pic)


def setup(bot):
    bot.add_cog(React(bot))
