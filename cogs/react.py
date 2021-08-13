import discord
from discord.ext import commands

from pathlib import Path
import random

from extension.cog import CogExtension


class React(CogExtension):
    @commands.command()
    async def image(self, ctx, num=1):
        imgs = random.sample(
            [p for p in Path(".").glob("./data/image/*")], num)
        for img in imgs:
            dcFile = discord.File(img)
            await ctx.send(file=dcFile)


def setup(bot):
    bot.add_cog(React(bot))
