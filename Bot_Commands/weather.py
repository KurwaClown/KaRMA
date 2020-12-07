from requests import get
import json

def getWeather(city):
    r = get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=62bea2e44e33de44829585e5157e7ce1&lang=fr")
    data=r.json()
    if data["cod"]==200:

        temp = str(data['main']['temp'])
        weather = data['weather'][0]['description']
        cityName = data['name']

        info = "Il fait actuellement {}°C à {} avec un temps {}".format(temp, cityName, weather)
        return info
    else: return "{} n'a pas été trouvé".format(city)