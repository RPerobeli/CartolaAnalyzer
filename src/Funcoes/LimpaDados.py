import pandas as pd
import numpy as np


def SeparaDataframeHomeAway(dfJogadores, dfPartidas):
    clubesCasaNaRodada = dfPartidas['clube_casa_id'].to_list()
    clubesForaNaRodada = dfPartidas['clube_visitante_id']
 
    clubesFortesForaDeCasa = dfPartidas[dfPartidas['delta_media_clube'] < -0.5]['clube_visitante_id'].to_list()
    clubesCasaNaRodada = clubesCasaNaRodada + clubesFortesForaDeCasa
    clubesCasaNaRodada = pd.Series(clubesCasaNaRodada) 

    dfJogadoresCasa = dfJogadores.loc[dfJogadores['clube_id'].isin(clubesCasaNaRodada)]
    dfJogadoresFora = dfJogadores.loc[dfJogadores['clube_id'].isin(clubesForaNaRodada)]

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
        
def CalculaMediaMovel(df):
    df['media_movel'] = 0.0
    jogadores = df['index'].unique()
    for i in range(0,jogadores.shape[0]):
        df_mediaMovel = df[df['index']==jogadores[i]]
        mediaMovel = df_mediaMovel['pontuacao'].mean()
        for j in range(0,df.shape[0]):
            if(df.at[j,'index'] == jogadores[i]):
                df.at[j,'media_movel'] = mediaMovel
            #endif
        #endfor
    #endfor
    return df
#endFunction

def CalculaDesvioPadrao(df):
    df['desv_padrao'] = 0.0
    jogadores = df['index'].unique()
    for i in range(0,jogadores.shape[0]):
        df_std = df[df['index']==jogadores[i]]
        desvioPadrao = df_std['pontuacao'].std()
        for j in range(0,df.shape[0]):
            if(df.at[j,'index'] == jogadores[i]):
                df.at[j,'desv_padrao'] = desvioPadrao
            #endif
        #endfor
    #endfor
    return df
#endFunction

def CalculaTendencia(df):
    df['tendencia'] = 0.0
    jogadores = df['index'].unique()
    for i in range(0,jogadores.shape[0]):
        df_tendencia = df[df['index']==jogadores[i]]
        menorRodada = df_tendencia['rodada'].min()
        maiorRodada = df_tendencia['rodada'].max()
        pontAntiga = df_tendencia[df_tendencia['rodada']==menorRodada]['pontuacao']
        pontRecente = df_tendencia[df_tendencia['rodada']==menorRodada]['pontuacao']
        tendencia = pontRecente - pontAntiga
        for j in range(0,df.shape[0]):
            if(df.at[j,'index'] == jogadores[i]):
                df.at[j,'tendencia'] = tendencia
            #endif
        #endfor
    #endfor
    return df
#endFunction

def CompletaInformacoesEstatisticas(rodadaAtual, df_jogadores_rodadas_anteriores, df_jogadores):
    maiorPontuacao = df_jogadores['pontos_num'].max()
    menorPontuacao = df_jogadores['pontos_num'].min()
    if(rodadaAtual == 2):
        df_jogadores['minimo_para_valorizar'] = df_jogadores['preco_num']*0.45
        if(maiorPontuacao-menorPontuacao!=0):
            df_jogadores['probabilidade_valorizar'] = (maiorPontuacao - df_jogadores['minimo_para_valorizar'])/(maiorPontuacao-menorPontuacao)
        else:
            df_jogadores['probabilidade_valorizar'] = 0
    elif(rodadaAtual >=3):
        df_jogadores['minimo_para_valorizar'] = df_jogadores['pontos_num']
        if(maiorPontuacao-menorPontuacao!=0):
            df_jogadores['probabilidade_valorizar'] = (maiorPontuacao - df_jogadores['media_num'])/(maiorPontuacao-menorPontuacao)
        else:
            df_jogadores['probabilidade_valorizar'] = 0

    df_jogadores['media_movel'] = 0.0
    df_jogadores['desv_padrao'] = 0.0

    jogadores = df_jogadores_rodadas_anteriores['apelido']

    for jogador in jogadores:
        mediaMovel = df_jogadores_rodadas_anteriores[df_jogadores_rodadas_anteriores['apelido'] == jogador]['media_movel'].values[0]
        desvioPadrao = df_jogadores_rodadas_anteriores[df_jogadores_rodadas_anteriores['apelido'] == jogador]['desv_padrao'].values[0]
        if(df_jogadores.loc[df_jogadores['apelido'] == jogador].empty):
            continue
        else:
            df_jogadores.loc[df_jogadores['apelido'] == jogador,'media_movel'] = float(mediaMovel)
            df_jogadores.loc[df_jogadores['apelido'] == jogador,'desv_padrao'] = float(desvioPadrao)

    df_jogadores['custo_beneficio'] = df_jogadores['preco_num']/df_jogadores['media_movel'].abs()
    df_jogadores['constancia'] = df_jogadores['media_movel']/df_jogadores['desv_padrao'].abs()

    return df_jogadores
#endFunction

def RecuperaMediasTimes(df_jogadores,df_partidas):
    df_partidas['delta_media_clube'] = 0.0
    df = df_jogadores.groupby('clube', as_index=False)['media_movel'].mean().sort_values('media_movel', ascending=False)
    print(df)
    for i in range(0,df_partidas.shape[0]):
        mandante = df_partidas.loc[i,'clube_casa']
        visitante = df_partidas.loc[i,'clube_visitante']
        media_mandante = df[df['clube'] == mandante]['media_movel'].to_numpy()[0]
        media_visitante = df[df['clube'] == visitante]['media_movel'].to_numpy()[0]
        df_partidas.at[i,'delta_media_clube'] = (media_mandante - media_visitante)
    return df_partidas
#endFunction