from jikanpy import Jikan
import discord


def getAnime(animeSearched):
    search_result = Jikan().search('anime', animeSearched)
    animeID =  search_result["results"][0]['mal_id']
    search_result  = Jikan().anime(animeID)
    return showAnime(search_result)

        

def getSeasonAnime(animePos=1):
    searchResult = Jikan().top(type='anime', page=1, subtype='upcoming')
    animeID = searchResult['top'][animePos-1]['mal_id']
    searchResult = Jikan().anime(animeID)


    embedVar = showAnime(searchResult)
    embedVar.set_footer(text=f"{animePos}/50")
    
    return embedVar

def showAnime(animeData):
    embedVar = discord.Embed(title=f"{animeData['title']}", color=0x4dffa6)

    embedVar.set_thumbnail(url=animeData['image_url'])

    embedVar.add_field(name = "Date de Sortie", value=f"{animeData['aired']['prop']['from']['day']}/{animeData['aired']['prop']['from']['month']}/{animeData['aired']['prop']['from']['year']}", inline=True)
    embedVar.add_field(name="Titre Anglais", value=animeData['title_english'])


    try:
        youtubeIdStart = animeData['trailer_url'].find('embed/')+6
        youtubeIdEnd = animeData['trailer_url'].find('?enable')
        embedVar.add_field(name="Link", value=f"{animeData['url']}", inline=False)
        embedVar.add_field(name="Trailer", value=f"https://www.youtube.com/watch?v={animeData['trailer_url'][youtubeIdStart:youtubeIdEnd]}", inline=False)
        
    except AttributeError as e:
        print(e)

    embedVar.add_field(name= "Synopsis", value=f"{animeData['synopsis'][0:500]}...", inline=False)
    
    return embedVar

def editAnimeList(payload, pageId, max):
    if payload.emoji.name == '⏮️':
        return getSeasonAnime(1)
    elif payload.emoji.name == '◀️':
        pageId = pageId - 1

        if pageId == 0:
            pageId = max

        return getSeasonAnime(pageId)
    elif payload.emoji.name == '▶️':
        pageId = pageId + 1

        if pageId == max+1:
            pageId = 1

        return getSeasonAnime(pageId)
    elif payload.emoji.name == '⏭️':
        return getSeasonAnime(max)