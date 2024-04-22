# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados
import pandas as pd

#TODO: recuperar todas as pontuacoes das rodadas até o momento e recuperar tendencias de valorizacao, media jogando em casa e fora de casa

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
rodadaAtual = 4

#Recuperar Clubes
df_clubes = RetrieveDataFromApi.RetrieveClubesFromApi()

#recuperar dados próx partidas
df_partidas = RetrieveDataFromApi.RetrievePartidasFromApi(rodadaAtual=rodadaAtual)
df_partidas = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa_id', 'clube_visitante_id'])
df_partidas = LimpaDados.ReplaceIdForName(df_partidas, df_clubes)
df_partidasExposicao = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa', 'clube_visitante'])
print("PARTIDAS DA RODADA:")
print(df_partidasExposicao)


#recuperar dados jogadores rodadas anteriores
df_jogadores_rodadas_anteriores = RetrieveDataFromApi.RetrieveJogadoresRodadasAntigasFromApi(rodadaAtual)


#recuperar dados jogadores
df_jogadores = RetrieveDataFromApi.RetrieveJogadoresFromApi()

df_jogadores = LimpaDados.ReplaceIdForNameJogadores(df_jogadores, df_clubes)


#adiciona informacoes de pontuacao
df_jogadores = LimpaDados.CompletaInformacoesEstatisticas(rodadaAtual, df_jogadores_rodadas_anteriores, df_jogadores)


#Separar jogadores com status provavel e não provavel
df_jogadores_nulos = df_jogadores[df_jogadores['status_id'] != 7]
df_jogadores = df_jogadores[df_jogadores['status_id'] == 7]

#separar jogadores jogando em casa e jogadores fora de casa
df_jogadores_casa, df_jogadores_fora = LimpaDados.SeparaDataframeHomeAway(df_jogadores, df_partidas) 

colunasDesejadasExposicao = [
        'atleta_id',
        'minimo_para_valorizar',
        'clube',
        'entrou_em_campo',
        'pontos_num',
        'media_num',
        'media_movel',
        'desv_padrao',
        'variacao_num',
        'preco_num',
        'apelido',
        'custo_beneficio',
        'probabilidade_valorizar'
    ]
#Normalizacao dos dados de interesse
#df_jogadores_casa = LimpaDados.NormalizeEficienciaDataFrame(df_jogadores_casa)

#Atacantes
atacantes = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 5]

if(PontuacaoOverValorizacao):
    mediaUltimaRodadaAta = atacantes['pontos_num'].mean()
    atacantes = atacantes[atacantes['media_num']>= mediaUltimaRodadaAta]
    atacantes = atacantes.sort_values('custo_beneficio', ascending=True)
else:
    atacantes = atacantes.sort_values('probabilidade_valorizar', ascending=True)

atacantes = RetrieveDataFromApi.FiltraColunasDesejadas(atacantes, colunasDesejadasExposicao)
print("ATACANTES:")
print(atacantes)

#Meias
meias = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 4]

if(PontuacaoOverValorizacao):
    mediaUltimaRodadaMei = meias['pontos_num'].mean()
    meias = meias[meias['media_num']>= mediaUltimaRodadaMei]
    meias = meias.sort_values('custo_beneficio', ascending=True)
else:
    meias = meias.sort_values('probabilidade_valorizar', ascending=True)

meias = RetrieveDataFromApi.FiltraColunasDesejadas(meias, colunasDesejadasExposicao)
print("MEIAS:")
print(meias)
#Zagueiros
zagueiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 3]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaZag = zagueiros['pontos_num'].mean()
    zagueiros = zagueiros[zagueiros['media_num']>= mediaUltimaRodadaZag]
    zagueiros = zagueiros.sort_values('custo_beneficio', ascending=True)
else:
    zagueiros = zagueiros.sort_values('probabilidade_valorizar', ascending=True)

zagueiros = RetrieveDataFromApi.FiltraColunasDesejadas(zagueiros, colunasDesejadasExposicao)
print("ZAGUEIROS:")
print(zagueiros)
#Laterais
laterais = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 2]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaLat = laterais['pontos_num'].mean()
    laterais = laterais[laterais['media_num']>= mediaUltimaRodadaLat]
    laterais = laterais.sort_values('custo_beneficio', ascending=True)
else:
    laterais = laterais.sort_values('probabilidade_valorizar', ascending=True)

laterais = RetrieveDataFromApi.FiltraColunasDesejadas(laterais, colunasDesejadasExposicao)
print("LATERAIS:")
print(laterais)
#Goleiros
goleiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 1]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaGol = goleiros['pontos_num'].mean()
    goleiros = goleiros[goleiros['media_num']>= mediaUltimaRodadaGol]
    goleiros = goleiros.sort_values('custo_beneficio', ascending=True)
else:
    goleiros = goleiros.sort_values('probabilidade_valorizar', ascending=True)

goleiros = RetrieveDataFromApi.FiltraColunasDesejadas(goleiros, colunasDesejadasExposicao)
print("GOLEIROS:")
print(goleiros)
#Tecnicos
tecnicos = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 6]
if(PontuacaoOverValorizacao):
    tecnicos = tecnicos.sort_values('custo_beneficio', ascending=True)
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