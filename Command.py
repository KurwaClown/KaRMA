import requests
import json
from jikanpy import Jikan
import discord
from datetime import datetime, date
from random import randint, sample

import sqlite3

from CONST import constants

class Weather(object):
    @staticmethod
    def getWeather(city):
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=62bea2e44e33de44829585e5157e7ce1&lang=fr")
        data=r.json()
        if data["cod"]==200:

            temp = str(data['main']['temp'])
            weather = data['weather'][0]['description']
            cityName = data['name']

            info = "Il fait actuellement {}°C à {} avec un temps {}".format(temp, cityName, weather)
            return info
        else: return "{} n'a pas été trouvé".format(city)

class Cocktail(object):
    @staticmethod
    def conversionCheck(args):
        try:
            volume = float(args[0])
            unit = args[1]
        except IndexError as e:
            print("no arg")
        pass
        
    @staticmethod
    def ouncesConversion(volume):
        return round(float(volume)*29.57,2)
    
    @staticmethod
    def getCocktail():
        r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
        data=r.json()
        infos = data["drinks"][0]
        
        embedVar = discord.Embed(title=infos['strDrink'], color=0x00ff00)
        embedVar.add_field(name="Instruction", value=infos['strInstructions'], inline=False)
        
        for index in range(1, 15):
            ingredient = infos["strIngredient{}".format(index)]
            measure = infos["strMeasure{}".format(index)]
            if not measure == None:
                embedVar.add_field(name="Ingredient {}".format(index), value="{} {}".format(measure, ingredient), inline=False)
        return embedVar

class Anime(object):


    @staticmethod
    def getAnime(animeSearched):
        search_result = Jikan().search('anime', animeSearched)
        return search_result["results"][0]["title"]

            
    @staticmethod
    def getSeasonAnime(animePos=1):
        searchResult = Jikan().top(type='anime', page=1, subtype='upcoming')
        animeID = searchResult['top'][animePos-1]['mal_id']
        searchResult = Jikan().anime(animeID)


        embedVar = discord.Embed(title=f"{searchResult['title']}", color=0x4dffa6)

        embedVar.set_thumbnail(url=searchResult['image_url'])

        embedVar.add_field(name = "Date de Sortie", value=f"{searchResult['aired']['prop']['from']['day']}/{searchResult['aired']['prop']['from']['month']}/{searchResult['aired']['prop']['from']['year']}", inline=True)
        embedVar.add_field(name="Titre Anglais", value=searchResult['title_english'])


        try:
            youtubeIdStart = searchResult['trailer_url'].find('embed/')+6
            youtubeIdEnd = searchResult['trailer_url'].find('?enable')
            embedVar.add_field(name="Trailer", value=f"https://www.youtube.com/watch?v={searchResult['trailer_url'][youtubeIdStart:youtubeIdEnd]}", inline=False)
        except AttributeError as e:
            print(e)

        embedVar.add_field(name= "Synopsis", value=f"{searchResult['synopsis'][0:1023]}", inline=False)
        embedVar.set_footer(text=f"{animePos}/50")
        
        return embedVar

    def editAnimeList(self, payload, pageId, max):
        if payload.emoji.name == '⏮️':
            return self.getSeasonAnime(1)
        elif payload.emoji.name == '◀️':
            pageId = pageId - 1

            if pageId == 0:
                pageId = max

            return self.getSeasonAnime(pageId)
        elif payload.emoji.name == '▶️':
            pageId = pageId + 1

            if pageId == max+1:
                pageId = 1

            return self.getSeasonAnime(pageId)
        elif payload.emoji.name == '⏭️':
            return self.getSeasonAnime(max)

            
         
class Random():

    @staticmethod
    def apexLoadout():
        loadout = sample(range(1,len(constants.WEAPONS)),2)
        return f"{constants.LEGENDS[randint(1, len(constants.LEGENDS))]} with {constants.WEAPONS[loadout[0]]} and {constants.WEAPONS[loadout[1]]}"

    @staticmethod
    def owChar(arg):
        if arg=="all":
            role = randint(1,3)
            return constants.HEROES[role][randint(1,len(constants.HEROES[role]))]
        elif arg == "tank":
            return constants.HEROES[1][randint(1,8)]
        elif arg == "dps":
            return constants.HEROES[2][randint(1,17)]
        elif arg == "heal":
            return constants.HEROES[3][randint(1,7)]
        elif arg == "role":
            return constants.OWROLE[randint(1,3)]

    @staticmethod
    def r6Char(arg):
        return constants.OPERATORS[arg][randint(1, len(constants.OPERATORS[arg]))]

    @staticmethod
    def lolChar():
        return constants.CHAMPIONS[randint(1, len(constants.CHAMPIONS))]
        

class Minecraft(object):
    @staticmethod
    def setHome(user, *coords):
        
        for coord in coords: 
            if coord[0]== '-':
                if not coord.lstrip('-').isdigit():
                    return
            elif not coord.isdigit():
                return

        x,y,z = [int(i) for i in coord]
        user = str(user)[:str(user).rindex('#')]

        conn = sqlite3.connect("Minecraft.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO home(username, x, y, z) VALUES(?,?,?,?)", [str(user), x, y, z])
        except sqlite3.IntegrityError as e:
            print(e)
            print("Database Error, trying to modify row instead")
            cur.execute("UPDATE home SET x = ?, y = ?, z = ? WHERE username = ?", [x,y,z,user])

        conn.commit()
        conn.close()

    @staticmethod
    def showHomes(name):    
        embedVar = discord.Embed(title="Homes", color=0xFF0000)

        query = "SELECT * FROM home"
        if not name==None:
            query += f" WHERE username LIKE '{name}%'"

        conn = sqlite3.connect("Minecraft.db")
        cur = conn.cursor()

        cur.execute(query)

        homes = cur.fetchall()

        for home in homes:
            embedVar.add_field(name=f"{home[1]}'s Home", value=f'x : {home[2]}\ny : {home[3]}\nz : {home[4]}\n')

        conn.close()
        return embedVar

    @staticmethod
    def addPlace(user, *args):
        for i in range(3): 
            if args[i][0]== '-':
                if not args[i].lstrip('-').isdigit():
                    return
            elif not args[i].isdigit():
                return

        x,y,z = [int(args[i]) for i in range(3)]
        name = args[3]
        conn = sqlite3.connect("Minecraft.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO location(name, x, y, z, username) VALUES(?,?,?,?, ?)", [str(name), x, y, z, str(user)])
            message = "Nouvelle endroit ajouté"
        except sqlite3.IntegrityError as e:
            print(e)
            message = f"L'endroit {name} existe déjà"
        

        conn.commit()
        conn.close()
        return message

    @staticmethod
    def showPlaces(placeid = 1):
        embedVar = discord.Embed(title="Waypoints", color=0xFF0000)

        query = "SELECT * FROM location WHERE id = ?"

        conn = sqlite3.connect("Minecraft.db")
        cur = conn.cursor()

        cur.execute("SELECT COUNT() FROM location")
        waypointsCount = cur.fetchone()[0]

        cur.execute(query, [placeid])

        waypoint = cur.fetchone()
        embedVar.add_field(name="Nom", value=f"{waypoint[1]}")
        embedVar.add_field(name="Utilisateur", value=f"{waypoint[5]}")

        embedVar.add_field(name="Coordonées", value=f"x : {waypoint[2]}\ny : {waypoint[3]}\nz : {waypoint[4]}\n", inline=False)

        embedVar.set_footer(text=f"{int(waypoint[0])}/{waypointsCount}")

        conn.close()
        return embedVar

    def editWaypointList(self, payload, pageId, max):
        if payload.emoji.name == '⏮️':
            return self.showPlaces(1)
        elif payload.emoji.name == '◀️':
            pageId = pageId - 1

            if pageId == 0:
                pageId = max

            return self.showPlaces(pageId)
        elif payload.emoji.name == '▶️':
            pageId = pageId + 1

            if pageId == max+1:
                pageId = 1

            return self.showPlaces(pageId)
        elif payload.emoji.name == '⏭️':
            return self.showPlaces(max)
        