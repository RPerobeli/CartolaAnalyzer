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


def SeparaDataframeHomeAway(dfJogadores, dfPartidas):
    jogadoresCasa = []
    jogadoresFora = []

    rodadas = dfPartidas['rodada'].unique()
    for numRodada in rodadas:
        dfPartidasRodada = dfPartidas[dfPartidas['rodada'] == numRodada]
        clubesCasaNaRodada = dfPartidasRodada['clube_casa_id']
        clubesForaNaRodada = dfPartidasRodada['clube_visitante_id']
        dfJogadoresCasaRodada = dfJogadores.query(
            f'`atletas.rodada_id` == {numRodada} & `atletas.clube_id` in @clubesCasaNaRodada')
        dfJogadoresForaRodada = dfJogadores.query(
            f'`atletas.rodada_id` == {numRodada} & `atletas.clube_id` in @clubesForaNaRodada')
        jogadoresCasa.append(dfJogadoresCasaRodada)
        jogadoresFora.append(dfJogadoresForaRodada)
    # endFor
    jogadoresCasa = pd.concat(jogadoresCasa)
    jogadoresFora = pd.concat(jogadoresFora)
    return jogadoresCasa, jogadoresFora
# endFunction
