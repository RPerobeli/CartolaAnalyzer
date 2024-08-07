# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados
import pandas as pd


#inputs
'''Ideia é valorizar o time ou atingir maior pontuacao?
    Usará tecnica de goleiro reserva?
    Qual o esquema tático?
    Qual a quantidade de cartoletas disponiveis?
'''
PontuacaoOverValorizacao = True
isTecnicaGoleiroReserva = True
esquema = [2,2,3,3] #num zagueiros / laterais /meias / atacantes
cartoletas = 120
rodadaAtual = 8


#Recuperar Clubes
df_clubes = RetrieveDataFromApi.RetrieveClubesFromApi()

#recuperar dados próx partidas
df_partidas = RetrieveDataFromApi.RetrievePartidasFromApi(rodadaAtual=rodadaAtual)
df_partidas = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa_id', 'clube_visitante_id'])
df_partidas = LimpaDados.ReplaceIdForName(df_partidas, df_clubes)



#recuperar dados jogadores rodadas anteriores
df_jogadores_rodadas_anteriores = RetrieveDataFromApi.RetrieveJogadoresRodadasAntigasFromApi(rodadaAtual)

#recuperar dados jogadores
df_jogadores = RetrieveDataFromApi.RetrieveJogadoresFromApi()

df_jogadores = LimpaDados.ReplaceIdForNameJogadores(df_jogadores, df_clubes)


#adiciona informacoes de pontuacao
df_jogadores = LimpaDados.CompletaInformacoesEstatisticas(rodadaAtual, df_jogadores_rodadas_anteriores, df_jogadores)

#separar jogadores por time
df_partidas = LimpaDados.RecuperaMediasTimes(df_jogadores,df_partidas)
df_partidas = LimpaDados.RecuperaMediasTimes(df_jogadores,df_partidas)

LimpaDados.RecuperaMediasDosClubesPorPosicao(df_jogadores)

df_partidasExposicao = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa', 'clube_visitante','delta_media_clube'])
print("PARTIDAS DA RODADA:")
print(df_partidasExposicao.sort_values('delta_media_clube', ascending=True))

#Separar jogadores com status provavel e não provavel
df_jogadores_nulos = df_jogadores[df_jogadores['status_id'] != 7]
df_jogadores = df_jogadores[df_jogadores['status_id'] == 7]



#separar jogadores jogando em casa e jogadores fora de casa
df_jogadores_casa, df_jogadores_fora = LimpaDados.SeparaDataframeHomeAway(df_jogadores, df_partidas)

#corta jogadores com custo_beneficio ruim e com consistencia duvidosa: 
#df_jogadores_casa = df_jogadores_casa[df_jogadores_casa['custo_beneficio'] < 2.0]
#df_jogadores_casa = df_jogadores_casa[df_jogadores_casa['constancia'] > 1.0]
#df_jogadores_casa = df_jogadores_casa[df_jogadores_casa['variacao_num'] < 1.0]

colunasDesejadasExposicao = [
        'atleta_id',
        'clube',
        'entrou_em_campo',
        'media_num',
        'media_movel',
        'desv_padrao',
        'constancia',
        'variacao_num',
        'preco_num',
        'apelido',
        'custo_beneficio',
        'probabilidade_valorizar'
    ]


#Atacantes
atacantes = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 5]

if(PontuacaoOverValorizacao):
    atacantes = atacantes.sort_values('media_movel', ascending=False)
else:
    atacantes = atacantes.sort_values('probabilidade_valorizar', ascending=False)

atacantes = RetrieveDataFromApi.FiltraColunasDesejadas(atacantes, colunasDesejadasExposicao)
print("ATACANTES:")
print(atacantes)

#Meias
meias = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 4]

if(PontuacaoOverValorizacao):
    meias = meias.sort_values('media_movel', ascending=False)
else:
    meias = meias.sort_values('probabilidade_valorizar', ascending=True)

meias = RetrieveDataFromApi.FiltraColunasDesejadas(meias, colunasDesejadasExposicao)
print("MEIAS:")
print(meias)
#Zagueiros
zagueiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 3]
if(PontuacaoOverValorizacao):
    zagueiros = zagueiros.sort_values('media_movel', ascending=False)
else:
    zagueiros = zagueiros.sort_values('probabilidade_valorizar', ascending=True)

zagueiros = RetrieveDataFromApi.FiltraColunasDesejadas(zagueiros, colunasDesejadasExposicao)
print("ZAGUEIROS:")
print(zagueiros)
#Laterais
laterais = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 2]
if(PontuacaoOverValorizacao):
    laterais = laterais.sort_values('media_movel', ascending=False)
else:
    laterais = laterais.sort_values('probabilidade_valorizar', ascending=True)

laterais = RetrieveDataFromApi.FiltraColunasDesejadas(laterais, colunasDesejadasExposicao)
print("LATERAIS:")
print(laterais)
#Goleiros
goleiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 1]
if(PontuacaoOverValorizacao):
    goleiros = goleiros.sort_values('media_movel', ascending=False)
else:
    goleiros = goleiros.sort_values('probabilidade_valorizar', ascending=True)

goleiros = RetrieveDataFromApi.FiltraColunasDesejadas(goleiros, colunasDesejadasExposicao)
print("GOLEIROS:")
print(goleiros)
#Tecnicos
tecnicos = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 6]
if(PontuacaoOverValorizacao):
    tecnicos = tecnicos.sort_values('media_movel', ascending=False)
else:
    tecnicos = tecnicos.sort_values('probabilidade_valorizar', ascending=True)

tecnicos = RetrieveDataFromApi.FiltraColunasDesejadas(tecnicos, colunasDesejadasExposicao)
print("TECNICOS:")
print(tecnicos)


'''
print('DREAM TEAM:')
dream_team = LimpaDados.FormarDreamTeam(atacantes, meias, laterais, zagueiros, goleiros, tecnicos, esquema)
print(dream_team)
'''