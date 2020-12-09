# KurwA
# Realistic
# Mad
# A.I


import discord

import asyncio
from discord.ext import commands
from CONST import constants
from Bot_Commands import minecraft, anime as anm, cocktail as ckt, game_random, weather as wth 
from Games import connect4

TOKEN = constants.TOKEN
gamesDict = {}
client = discord.Client()

client = commands.Bot(command_prefix='kc!')

"""###Bot Commands###"""

#Weather Command
@client.command()
async def weather(ctx, *args):
    await ctx.send(wth.getWeather('-'.join(args)))

#Cocktail Command
@client.command()
async def cocktail(ctx):
    await ctx.send(embed = ckt.getCocktail())

#Season Release Command
@client.command()
async def upcoming(ctx, *args):
    reactions = ['⏮️','◀️', '▶️', '⏭️']
    message = await ctx.send(embed = anm.getSeasonAnime())
    for reaction in reactions:
        await message.add_reaction(reaction)
    

#Anime Command
@client.command()
async def anime(ctx, *args):
    await ctx.send(embed = anm.getAnime(' '.join(args)))

@client.command()
async def random(ctx, *args):
    if args[0]=="apex":
        await ctx.send(f"{ctx.author} you play {game_random.apexLoadout()}")
    elif args[0]=="ow":
        role = "all"
        if len(args)>1:
            role = args[1]
        await ctx.send(game_random.owChar(role))
    elif args[0]=="r6" and len(args)>1:
        await ctx.send(game_random.r6Char(args[1]))
    elif args[0]=="lol":
        await ctx.send(game_random.lolChar())
    
@client.command()
async def sethome(ctx, *args):
    if len(args) < 3:
        return
    
    minecraft.setHome(ctx.author, *args)
    await ctx.send("New Home Set")

@client.command()
async def homes(ctx, arg = None):
    await ctx.send(embed = minecraft.showHomes(arg))

@client.command()
async def addwaypoint(ctx, *args):
    if len(args) < 4:
        return
    
    await ctx.send(minecraft.addPlace(ctx.author, *args))

@client.command()
async def waypoints(ctx, *args):
    message = await ctx.send(embed=minecraft.showPlaces())
    for reaction in ['⏮️','◀️', '▶️', '⏭️']:
        await message.add_reaction(reaction)

@client.command()
async def connect(ctx):
    """
    Connect 4 game
    """
    gamesDict.update({str(ctx.author): connect4(ctx.author)})
    
    message = await ctx.send(embed=gamesDict[str(ctx.author)].gameStart())
    await message.add_reaction('🎮')


@client.event
async def on_raw_reaction_add(payload):
    connectReaction = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    if payload.user_id == client.user.id:
        return

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji.name, payload.member)

    if len(message.embeds[0]) == 0:
        return
    embed = message.embeds[0]

    try:
        pageId = int(embed.footer.text.split("/")[0])
        lastPage = int(embed.footer.text.split("/")[1])
    except (AttributeError, ValueError) as e:
        print(e)

    if embed.title == "Waypoints":
        await message.edit(embed= minecraft.editWaypointList(payload, pageId, lastPage))
    elif embed.title == "Connect 4":
        if embed.footer.text == "Waiting for player":
            await message.edit(embed=gamesDict[str(embed.description)].reactionEdit(payload, message, gamesDict, client)[0])
            await message.remove_reaction(payload.emoji.name, client.user)
            for reaction in connectReaction:
                await message.add_reaction(reaction)
        else:
            newEmbed, columnFull = gamesDict[str(embed.description.split(' ')[0])].reactionEdit(payload, message, gamesDict, client)
            await message.edit(embed=newEmbed)
            if columnFull:
                await message.remove_reaction(payload.emoji.name, client.user)
            
    else:
        await message.edit(embed= anm.editAnimeList(payload, pageId, lastPage))
    
    


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await client.process_commands(message)
        
client.run(TOKEN)
