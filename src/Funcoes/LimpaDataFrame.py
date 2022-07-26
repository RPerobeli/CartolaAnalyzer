from Funcoes.LimpaDataFrame import *
from Funcoes.LibPartidas import *
from Funcoes.RetrieveDataFromRepository import *
from Funcoes.AnalisesEstatisticas import *


def RetiraColunasIndesejadas(data, ColunasDesejadas):
    data = data[ColunasDesejadas]
    return data
# endFunction


def GetRodadaAtual(data):
    RodadaAtual = data['atletas.rodada_id'].max()
    return RodadaAtual
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



