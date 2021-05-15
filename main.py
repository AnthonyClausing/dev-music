import discord
from discord import channel
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
client = commands.Bot(command_prefix='!')

players = {}

#todo 
#check: if valid youtube url
#check: if player is already on/connected
#create: queue for player
@client.event
async def on_ready():
	print('DEV MUSIC ONLINE')

@client.command(pass_context=True)
async def leave(ctx):
  server = ctx.message.guild
  # del players[server.id]
  voice_client =  server.voice_client
  await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
  channel = ctx.message.author.voice.channel
  await channel.connect()
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)
  if not voice.is_playing():
      with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
      URL = info['formats'][0]['url']
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
  else:
      await ctx.send("Already playing a song")
      return

# async def on_message(message):
# 	author = message.author
# 	print({"name": author},'hello')
# 	if message.author == client.user:
# 		return 
# 	if message.content.startswith('!play') and 'youtu' in message.content:
# 		id_string = message.content.split('/')[3]
# 		print(id_string)
# 		# video_id = id_string[8:] if 'watch' in id_string else id_string
# 		# await message.channel.send(video_id)

client.run(BOT_TOKEN)