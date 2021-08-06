import discord
from discord.ext import commands
from core.ext import cog_ext
from pathlib import Path
import random


class React(cog_ext):
    @commands.command()
    async def image(self, ctx, num=1):
        imgs = random.sample(
            [p for p in Path(".").glob("./data/image/*")], num)
        for img in imgs:
            dcFile = discord.File(img)
            await ctx.send(file=dcFile)


def setup(bot):
    bot.add_cog(React(bot))
