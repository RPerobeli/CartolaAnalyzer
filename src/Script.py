# import
import Funcoes.RetrieveDataFromApi as RetrieveDataFromApi
import Funcoes.LimpaDados as LimpaDados


#inputs
'''Ideia é valorizar o time ou atingir maior pontuacao?
    Usará tecnica de goleiro reserva?
    Qual o esquema tático?
'''
PontuacaoOverValorizacao = True
isTecnicaGoleiroReserva = True
esquema = [4,3,3]


#recuperar dados próx partidas
rodadaAtual = 1
df_partidas = RetrieveDataFromApi.RetrievePartidasFromApi(rodadaAtual=rodadaAtual)
df_partidas = RetrieveDataFromApi.FiltraColunasDesejadas(
        df_partidas, ['rodada', 'clube_casa_id', 'clube_visitante_id'])
print(df_partidas)
#recuperar dados jogadores
df_jogadores = RetrieveDataFromApi.RetrieveJogadoresFromApi()
df_jogadores['minimo_para_valorizar'] = df_jogadores['media_num']*0.45
print(df_jogadores)

df_jogadores_casa, df_jogadores_fora = LimpaDados.SeparaDataframeHomeAway(df_jogadores, df_partidas) 

#df_jogadores = df_jogadores[df_jogadores['status_id' == 7]]
