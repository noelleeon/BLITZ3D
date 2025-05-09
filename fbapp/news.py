###############################################
# Filename: news.py                           #
# Purpose: Grabs the latest 20 news headlines #
# for NFL football.                           #
###############################################
from django.conf import settings
import requests

def newz(request):
    url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLNews"
    querystring = {"fantasyNews":"true","maxItems":"20"}
    headers = {
      ,
    }
    response = requests.get(url, headers=headers, params=querystring)
    resp = response.json()
    newz = resp['body']
    return {'newz':newz}
