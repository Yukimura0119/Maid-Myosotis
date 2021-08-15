from ssl import Options
import discord
from discord.ext import commands

import youtube_dl
import asyncio

from extension.cog import CogExtension
from tools import message

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
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

playlist = asyncio.Queue()
next_song = asyncio.Event()


class Music(CogExtension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vc = None

        async def audio_player_task():
            while True:
                next_song.clear()
                current = await playlist.get()
                print(current['title'])
                self.vc.play(
                    discord.FFmpegPCMAudio(current['url'], **ffmpeg_opts), after=lambda x: self.bot.loop.call_soon_threadsafe(next_song.set))
                await next_song.wait()
        self.bg_task = self.bot.loop.create_task(audio_player_task())

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        ch = ctx.author.voice.channel
        await ch.connect()
        self.vc = ctx.voice_client

    @commands.command()
    async def play(self, ctx, url: str):
        vc = ctx.voice_client
        file = ydl.extract_info(url, download=False)
        title = file['title']
        await playlist.put(file)
        # vc.play(discord.FFmpegPCMAudio(file['url']))
        await ctx.send(message.codeblock(f'ADD - {title}'))

    @ commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send(message.codeblock('Song Resumed.'))

    @ commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send(message.codeblock('Song Paused.'))

    @ commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send(message.codeblock('Song Stopped.'))


def setup(bot):
    bot.add_cog(Music(bot))
