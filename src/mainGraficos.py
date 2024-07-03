# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

#Separar jogadores com status provavel e não provavel
df_jogadores_nulos = df_jogadores[df_jogadores['status_id'] != 7]
df_jogadores = df_jogadores[df_jogadores['status_id'] == 7]

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
clubes = df_jogadores['clube'].unique()
atacantes = df_jogadores[df_jogadores['posicao_id'] == 5].sort_values("media_movel",ascending=False)
print("ATACANTES")
print(atacantes)

meias = df_jogadores[df_jogadores['posicao_id'] == 4].sort_values("media_movel",ascending=False)
print("MEIAS")
print(meias)

laterais = df_jogadores[df_jogadores['posicao_id'] == 2].sort_values("media_movel",ascending=False)
print("LATERAIS")
print(laterais)

zagueiros = df_jogadores[df_jogadores['posicao_id'] == 3].sort_values("media_movel",ascending=False)
print("ZAGUEIROS")
print(zagueiros)

goleiros = df_jogadores[df_jogadores['posicao_id'] == 1].sort_values("media_movel",ascending=False)
print("GOLEIROS")
print(goleiros)

dados = meias
sns.barplot(data=dados, x=dados['apelido'], y=dados['media_movel'], hue="clube")
locs,labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.show()

