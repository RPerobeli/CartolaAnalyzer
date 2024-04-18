import pandas as pd
import numpy as np


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

def ReplaceIdForName(df_partidas, df_clubes):
    df_partidas['clube_casa'] = np.zeros(df_partidas.shape[0]).astype(str)
    df_partidas['clube_visitante'] = np.zeros(df_partidas.shape[0]).astype(str)
    for i in range(0,df_partidas.shape[0]):
        df_partidas.at[i, 'clube_casa'] = df_clubes[f'{df_partidas.at[i, 'clube_casa_id']}']['nome_fantasia']
        df_partidas.at[i, 'clube_visitante'] = df_clubes[f'{df_partidas.at[i, 'clube_visitante_id']}']['nome_fantasia']
    return df_partidas
#endFunction

def ReplaceIdForNameJogadores(df_jogadores, df_clubes):
    df_jogadores.insert(1, 'clube', '')

    for i in range(df_jogadores.shape[0]):
        clube_id = df_jogadores.at[i, 'clube_id']
        clube_nome = df_clubes[f'{clube_id}']['nome_fantasia']

        df_jogadores.at[i, 'clube'] = clube_nome

    return df_jogadores

#endFunction

def FormarDreamTeam(atacantes, meias, laterais, zagueiros, goleiros, tecnicos, esquema):
    dt = pd.concat([atacantes.head(esquema[3]), meias.head(esquema[2]), laterais.head(esquema[1]), zagueiros.head(esquema[0]), goleiros.head(1), tecnicos.head(1)])
    return dt
# endFunction

def NormalizeEficienciaDataFrame(dfJogadores):
    #media
    maiorMedia = dfJogadores['media_num'].max()
    menorMedia = dfJogadores['media_num'].min()
    dfJogadores['media_num'] = dfJogadores['media_num']/(maiorMedia-menorMedia)
    #custo_beneficio
    piorCustoBeneficio = dfJogadores['custo_beneficio'].max()
    melhorCustoBeneficio = dfJogadores['custo_beneficio'].min()
    dfJogadores['custo_beneficio'] = dfJogadores['custo_beneficio']/(piorCustoBeneficio-melhorCustoBeneficio)
    return dfJogadores
# endFunction

def CalculaEficiencia(dfJogadores, PontuacaoOverValorizacao):
    if(PontuacaoOverValorizacao):
        dfJogadores['eficiencia'] = dfJogadores['media_num']+(1-dfJogadores['custo_beneficio'])+dfJogadores['probabilidade_valorizar']
    else:
        dfJogadores['eficiencia'] = (1-dfJogadores['minimo_para_valorizar'])+(1-dfJogadores['custo_beneficio'])
#endFunction