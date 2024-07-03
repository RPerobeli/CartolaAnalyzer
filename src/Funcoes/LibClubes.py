import requests
import json
import pandas as pd


def GetClubes():
    URL = f"https://api.cartola.globo.com/clubes"
    response = requests.get(URL)
    clubes = json.loads(response.text)
    return clubes
# endFunction

#usa sofascore como fonte de dados
def GetClubesBySofascore():
    id_brasileirao = 325
    URL = f""
