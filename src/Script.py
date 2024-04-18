# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados

#TODO: recuperar todas as pontuacoes das rodadas até o momento e recuperar tendencias de valorizacao, media jogando em casa e fora de casa

#inputs
'''Ideia é valorizar o time ou atingir maior pontuacao?
    Usará tecnica de goleiro reserva?
    Qual o esquema tático?
'''
PontuacaoOverValorizacao = True
isTecnicaGoleiroReserva = True
esquema = [4,3,3]


#recuperar dados próx partidas
rodadaAtual = 2
df_partidas = RetrieveDataFromApi.RetrievePartidasFromApi(rodadaAtual=rodadaAtual)
df_partidas = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa_id', 'clube_visitante_id'])
print("PARTIDAS DA RODADA:")
print(df_partidas)
#recuperar dados jogadores
df_jogadores = RetrieveDataFromApi.RetrieveJogadoresFromApi()

#adiciona informacoes de pontuacao
df_jogadores['minimo_para_valorizar'] = df_jogadores['media_num']*0.45
df_jogadores['custo_beneficio'] = df_jogadores['preco_num']/df_jogadores['media_num']


#Separar jogadores com status provavel e não provavel
df_jogadores_nulos = df_jogadores[df_jogadores['status_id'] != 7]
df_jogadores = df_jogadores[df_jogadores['status_id'] == 7]

#separar jogadores jogando em casa e jogadores fora de casa
df_jogadores_casa, df_jogadores_fora = LimpaDados.SeparaDataframeHomeAway(df_jogadores, df_partidas) 

colunasDesejadasExposicao = [
        'minimo_para_valorizar',
        'clube_id',
        'pontos_num',
        'media_num',
        'variacao_num',
        'preco_num',
        'apelido',
        'custo_beneficio'
    ]


#Atacantes
atacantes = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 5]
if(PontuacaoOverValorizacao):
    atacantes = atacantes.sort_values('custo_beneficio', ascending=True)
else:
    atacantes = atacantes.sort_values('minimo_para_valorizar', ascending=True)

atacantes = RetrieveDataFromApi.FiltraColunasDesejadas(atacantes, colunasDesejadasExposicao)
print("ATACANTES:")
print(atacantes)
#Meias
meias = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 4]
if(PontuacaoOverValorizacao):
    meias = meias.sort_values('custo_beneficio', ascending=True)
else:
    meias = meias.sort_values('minimo_para_valorizar', ascending=True)

meias = RetrieveDataFromApi.FiltraColunasDesejadas(meias, colunasDesejadasExposicao)
print("MEIAS:")
print(meias)
#Zagueiros
zagueiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 3]
if(PontuacaoOverValorizacao):
    zagueiros = zagueiros.sort_values('custo_beneficio', ascending=True)
else:
    zagueiros = zagueiros.sort_values('minimo_para_valorizar', ascending=True)

zagueiros = RetrieveDataFromApi.FiltraColunasDesejadas(zagueiros, colunasDesejadasExposicao)
print("ZAGUEIROS:")
print(zagueiros)
#Laterais
laterais = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 2]
if(PontuacaoOverValorizacao):
    laterais = laterais.sort_values('custo_beneficio', ascending=True)
else:
    laterais = laterais.sort_values('minimo_para_valorizar', ascending=True)

laterais = RetrieveDataFromApi.FiltraColunasDesejadas(laterais, colunasDesejadasExposicao)
print("LATERAIS:")
print(laterais)
#Goleiros
goleiros = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 1]
if(PontuacaoOverValorizacao):
    goleiros = goleiros.sort_values('custo_beneficio', ascending=True)
else:
    goleiros = goleiros.sort_values('minimo_para_valorizar', ascending=True)

goleiros = RetrieveDataFromApi.FiltraColunasDesejadas(goleiros, colunasDesejadasExposicao)
print("GOLEIROS:")
print(goleiros)
#Tecnicos
tecnicos = df_jogadores_casa[df_jogadores_casa['posicao_id'] == 6]
if(PontuacaoOverValorizacao):
    tecnicos = tecnicos.sort_values('custo_beneficio', ascending=True)
else:
    tecnicos = tecnicos.sort_values('minimo_para_valorizar', ascending=True)

tecnicos = RetrieveDataFromApi.FiltraColunasDesejadas(tecnicos, colunasDesejadasExposicao)
print("TECNICOS:")
print(tecnicos)
