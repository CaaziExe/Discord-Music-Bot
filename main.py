import discord
import os
from discord.ext import commands
import youtube_dl
from youtubesearchpython import VideosSearch

TOKEN = os.environ["DISCORD_TOKEN"]

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    await client.process_commands(message)

@client.command()
async def j(ctx):
    if ctx.author.voice is None:
        await ctx.send('Silahkan join voice channel terlebih dahulu!!')
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    await ctx.send('Joined')

@client.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('Disconnected')

@client.command()
async def p(ctx, *, arg):
    #join
    if ctx.author.voice is None:
        await ctx.send('Silahkan join voice channel terlebih dahulu!!')
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    await ctx.send('Joined')

    #play
    ctx.voice_client.stop()
    video = VideosSearch(arg + 'song', limit=1)
    url = video.result()['result'][0]['link']
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send('Paused')

@client.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send('Resume')

@client.command()
async def skip(ctx):
    await ctx.voice_client.stop()

client.run(TOKEN)