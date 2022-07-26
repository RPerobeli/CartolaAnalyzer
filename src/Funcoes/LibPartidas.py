import requests
import json


def GetPartidasByRodada(dataframe, numRodada):
    URL = f"https://api.cartolafc.globo.com/partidas/{numRodada}"
    response = requests.get(URL)
    PartidasCompleteData = json.loads(response.text)
    print(type(PartidasCompleteData))
# endFunction
