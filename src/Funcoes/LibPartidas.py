import requests
import json
import pandas as pd


def GetPartidasByRodada(numRodada):
    URL = f"https://api.cartolafc.globo.com/partidas/{numRodada}"
    response = requests.get(URL)
    PartidasCompleteData = json.loads(response.text)
    return PartidasCompleteData['partidas']
# endFunction


def GetProximasPartidas(numRodada):
    URL = f"https://api.cartola.globo.com/partidas"
    response = requests.get(URL)
    proximas = json.loads(response.text)
    if(proximas['rodada'] == numRodada+1):
        return proximas['partidas']
    else:
        print('erro na aquisição de proximas partidas.')
    # endif
# endFunction


