from requests import get
import discord


def conversionCheck(args):
    try:
        volume = float(args[0])
        unit = args[1]
    except IndexError as e:
        print("no arg")
    pass
    

def ouncesConversion(volume):
    return round(float(volume)*29.57,2)


def getCocktail():
    r = get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
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