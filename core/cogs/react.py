import discord
from discord.ext import commands
from core.ext import Cog_ext
import random
import json
import os

with open('data/settings.json', 'r', encoding='utf8') as settingfile:
    db = json.load(settingfile)


class React(Cog_ext):
    @commands.command()
    async def pic(self, ctx):
        pic = discord.File(
            db['picture-path']+'//'+random.choice(os.listdir(db['picture-path'])))
        await ctx.send(file=pic)


def setup(bot):
    bot.add_cog(React(bot))
