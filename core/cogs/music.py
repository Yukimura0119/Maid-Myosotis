import discord
from discord.ext import commands

import youtube_dl
import asyncio

from extension.cog import CogExtension

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/data/music/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
ffmpeg_opts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

playlist = asyncio.Queue()
song_name_list = asyncio.Queue()


class Music(CogExtension):

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        ch = ctx.author.voice.channel
        await ch.connect()

    @commands.command()
    async def play(self, ctx, url: str):
        vc = ctx.voice_client
        file = ydl.extract_info(url, download=False)
        title = file['title']
        vc.play(discord.FFmpegPCMAudio(file['url']))
        await ctx.send(f'```\nNow playing - {title}\n```')

    @ commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send('```\nSong Resumed.\n```')

    @ commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send('```\nSong Paused.\n```')

    @ commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send('```\nSong Stopped.\n```')


def setup(bot):
    bot.add_cog(Music(bot))
