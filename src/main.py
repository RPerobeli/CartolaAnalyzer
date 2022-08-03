
# import
from Funcoes.LimpaDataFrame import *
from Funcoes.LibPartidas import *
from Funcoes.RetrieveDataFromRepository import *
# main

# Recupera Data do repositório github usado como referencia
cartola2022 = RetrieveDataFromRepository(2022)
# print(cartola2022.shape)
# print(cartola2022.info)
# print(cartola2022.columns)

listaColunas = ['atletas.atleta_id',
                'atletas.rodada_id',
                'atletas.clube_id',
                'atletas.status_id',
                'atletas.pontos_num',
                'atletas.posicao_id',
                'atletas.preco_num',
                'atletas.variacao_num',
                'atletas.media_num',
                'atletas.jogos_num',
                'atletas.slug',
                'atletas.nome',
                'rodada',
                'atletas.clube.id.full.name']

cartola2022 = RetiraColunasIndesejadas(
    data=cartola2022, ColunasDesejadas=listaColunas)
RodadaAtual = GetRodadaAtual(cartola2022)
print(RodadaAtual)
# Inserir no dataframe se a pontuação do jogador na rodada X foi ou nao como jogador da casa
dfPartidasAteRodadaAtual = RetrievePartidasFromApi(rodadaAtual=RodadaAtual)

dfPartidasAteRodadaAtual = RetiraColunasIndesejadas(
    dfPartidasAteRodadaAtual, ['rodada', 'clube_casa_id', 'clube_visitante_id'])

[JogadoresCasa, JogadoresFora] = SeparaDataframeHomeAway(
    cartola2022, dfPartidasAteRodadaAtual)
