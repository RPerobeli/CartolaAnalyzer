import requests
import json
import pandas as pd


def GetJogadores():
    URL = f"https://api.cartola.globo.com/atletas/mercado"
    response = requests.get(URL)
    proximas = json.loads(response.text)
    return proximas['atletas']
# endFunction