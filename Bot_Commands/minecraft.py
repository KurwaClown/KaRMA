import sqlite3

from CONST import constants
import discord


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
    
    print(message)
    conn.commit()
    conn.close()
    return message


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

def editWaypointList(payload, pageId, max):
    if payload.emoji.name == '⏮️':
        return showPlaces(1)
    elif payload.emoji.name == '◀️':
        pageId = pageId - 1

        if pageId == 0:
            pageId = max

        return showPlaces(pageId)
    elif payload.emoji.name == '▶️':
        pageId = pageId + 1

        if pageId == max+1:
            pageId = 1

        return showPlaces(pageId)
    elif payload.emoji.name == '⏭️':
        return showPlaces(max)
    