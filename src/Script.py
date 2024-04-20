# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados

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

#Recuperar Clubes
df_clubes = RetrieveDataFromApi.RetrieveClubesFromApi()

#recuperar dados próx partidas
rodadaAtual = 3
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
print(df_jogadores_rodadas_anteriores)


#recuperar dados jogadores
df_jogadores = RetrieveDataFromApi.RetrieveJogadoresFromApi()

df_jogadores = LimpaDados.ReplaceIdForNameJogadores(df_jogadores, df_clubes)
maiorPontuacao = df_jogadores['pontos_num'].max()
menorPontuacao = df_jogadores['pontos_num'].min()


#adiciona informacoes de pontuacao
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

df_jogadores['custo_beneficio'] = df_jogadores['preco_num']/df_jogadores['media_num'].abs()
df_jogadores['media_movel'] = 0.0

for i in range(df_jogadores.shape[0]):
    for j in range(df_jogadores_rodadas_anteriores.shape[0]):
    

#Separar jogadores com status provavel e não provavel
df_jogadores_nulos = df_jogadores[df_jogadores['status_id'] != 7]
df_jogadores = df_jogadores[df_jogadores['status_id'] == 7]

#separar jogadores jogando em casa e jogadores fora de casa
df_jogadores_casa, df_jogadores_fora = LimpaDados.SeparaDataframeHomeAway(df_jogadores, df_partidas) 

colunasDesejadasExposicao = [
        'minimo_para_valorizar',
        'clube',
        'entrou_em_campo',
        'pontos_num',
        'media_num',
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
    mediaUltimaRodadaAta = df_jogadores['pontos_num'].mean()
    atacantes = atacantes[atacantes['pontos_num']>= mediaUltimaRodadaAta]
    atacantes = atacantes.sort_values('custo_beneficio', ascending=True)
else:
    atacantes = atacantes.sort_values('probabilidade_valorizar', ascending=True)

atacantes = RetrieveDataFromApi.FiltraColunasDesejadas(atacantes, colunasDesejadasExposicao)
print("ATACANTES:")
print(atacantes)

#Meias
meias = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 4]

if(PontuacaoOverValorizacao):
    mediaUltimaRodadaMei = df_jogadores['pontos_num'].mean()
    meias = meias[meias['pontos_num']>= mediaUltimaRodadaMei]
    meias = meias.sort_values('custo_beneficio', ascending=True)
else:
    meias = meias.sort_values('probabilidade_valorizar', ascending=True)

meias = RetrieveDataFromApi.FiltraColunasDesejadas(meias, colunasDesejadasExposicao)
print("MEIAS:")
print(meias)
#Zagueiros
zagueiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 3]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaZag = df_jogadores['pontos_num'].mean()
    zagueiros = zagueiros[zagueiros['pontos_num']>= mediaUltimaRodadaZag]
    zagueiros = zagueiros.sort_values('custo_beneficio', ascending=True)
else:
    zagueiros = zagueiros.sort_values('probabilidade_valorizar', ascending=True)

zagueiros = RetrieveDataFromApi.FiltraColunasDesejadas(zagueiros, colunasDesejadasExposicao)
print("ZAGUEIROS:")
print(zagueiros)
#Laterais
laterais = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 2]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaLat = df_jogadores['pontos_num'].mean()
    laterais = laterais[laterais['pontos_num']>= mediaUltimaRodadaLat]
    laterais = laterais.sort_values('custo_beneficio', ascending=True)
else:
    laterais = laterais.sort_values('probabilidade_valorizar', ascending=True)

laterais = RetrieveDataFromApi.FiltraColunasDesejadas(laterais, colunasDesejadasExposicao)
print("LATERAIS:")
print(laterais)
#Goleiros
goleiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 1]
if(PontuacaoOverValorizacao):
    mediaUltimaRodadaGol = df_jogadores['pontos_num'].mean()
    goleiros = goleiros[goleiros['pontos_num']>= mediaUltimaRodadaGol]
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