import pandas as pd


def SeparaDataframeHomeAway(dfJogadores, dfPartidas):
    clubesCasaNaRodada = dfPartidas['clube_casa_id']
    clubesForaNaRodada = dfPartidas['clube_visitante_id']

    dfJogadoresCasa = dfJogadores.loc[dfJogadores['clube_id'].isin(clubesCasaNaRodada)]
    dfJogadoresFora = dfJogadores.loc[dfJogadores['clube_id'].isin(clubesForaNaRodada)]

    '''dfJogadoresCasaRodada = dfJogadores.query(
        f"'clube_id' in @clubesCasaNaRodada")
    dfJogadoresForaRodada = dfJogadores.query(
        f"'clube_id' in @clubesForaNaRodada")
    '''
    return dfJogadoresCasa, dfJogadoresFora
# endFunction