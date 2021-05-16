import discord
from discord import channel
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
MUSIC_CHANNEL = 'tunes'
QUEUE_LIMIT = 10
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

client = commands.Bot(command_prefix='!')

#Maybe code for multiple instances of the player and its respective queue
# players = {}
queue = []

@client.event
async def on_ready():
	print('DEV MUSIC ONLINE')

@client.command(pass_context=True)
async def leave(ctx):
  server = ctx.message.guild
  voice_client =  server.voice_client
  await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
  if ctx.channel.name != MUSIC_CHANNEL:
    await ctx.send('Commands can only be made in the {0}'.format(MUSIC_CHANNEL))
    return
  if not is_connected(ctx):
    voice_channel = ctx.message.author.voice.channel
    await voice_channel.connect()
  if not is_valid_url(url):
    await ctx.send('Invalid youtube url')
    return
  voice = get(client.voice_clients, guild=ctx.guild)
  if not voice.is_playing():
      play_song(ctx,voice,url)
  else:
    if len(queue) < QUEUE_LIMIT:
      enqueue(url)
      await ctx.send("Adding to queue...")
    else:
      await ctx.send("Maximum of 10 songs can be queued")

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def is_valid_url(url):
  return 'youtu' in url

def play_song(ctx, voice, url):
  with YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download=False)
  URL = info['formats'][0]['url']
  voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=  lambda e: dequeue(ctx, voice))
  voice.is_playing()

#check queue length to limit number, maybe 'next' command, and a 'check queue' command
def enqueue(url):
    queue.append(url)

def dequeue(ctx,voice):
  if len(queue) > 0:
    next_song = queue.pop(0)
    play_song(ctx, voice, next_song)

client.run(BOT_TOKEN)