# KurwA
# Realistic
# Mad
# A.I


import discord

import asyncio
from discord.ext import commands
from CONST import constants

import Command as cmd


TOKEN = constants.TOKEN
OBJECT_LI = []
client = discord.Client()

client = commands.Bot(command_prefix='kc!')

"""###Bot Commands###"""

#Weather Command
@client.command()
async def weather(ctx, *args):
    await ctx.send(cmd.Weather.getWeather('-'.join(args)))

#Cocktail Command
@client.command()
async def cocktail(ctx):
    await ctx.send(embed = cmd.Cocktail.getCocktail())

#Season Release Command
@client.command()
async def upcoming(ctx, *args):
    reactions = ['⏮️','◀️', '▶️', '⏭️']
    message = await ctx.send(embed = cmd.Anime.getSeasonAnime())
    for reaction in reactions:
        await message.add_reaction(reaction)
    

#Anime Command
@client.command()
async def anime(ctx, *args):
    await ctx.send(cmd.Anime.getAnime)

@client.command()
async def random(ctx, *args):
    if args[0]=="apex":
        await ctx.send(f"{ctx.author} you play {cmd.Random.apexLoadout()}")
    elif args[0]=="ow":
        role = "all"
        if len(args)>1:
            role = args[1]
        await ctx.send(cmd.Random.owChar(role))
    elif args[0]=="r6" and len(args)>1:
        await ctx.send(cmd.Random.r6Char(args[1]))
    elif args[0]=="lol":
        await ctx.send(cmd.Random.lolChar())
    
@client.command()
async def sethome(ctx, *args):
    if len(args) < 3:
        return
    
    cmd.Minecraft.setHome(ctx.author, *args)
    await ctx.send("New Home Set")

@client.command()
async def home(ctx, arg = None):
    await ctx.send(embed = cmd.Minecraft.showHomes(arg))


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name == '⏮️':
        await message.edit(embed=cmd.Anime.getSeasonAnime(0))
    elif payload.emoji.name == '◀️':
        animeId = int(message.embeds[0].footer.text.split("/")[0])-2

        if animeId == -1:
            animeId = 49

        await message.edit(embed=cmd.Anime.getSeasonAnime(animeId))
    elif payload.emoji.name == '▶️':
        animeId = int(message.embeds[0].footer.text.split("/")[0])

        if animeId == 50:
            animeId = 0

        await message.edit(embed=cmd.Anime.getSeasonAnime(animeId))
    elif payload.emoji.name == '⏭️':
        await message.edit(embed=cmd.Anime.getSeasonAnime(49))
    
    await message.remove_reaction(payload.emoji.name, payload.member)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await client.process_commands(message)
        
client.run(TOKEN)


