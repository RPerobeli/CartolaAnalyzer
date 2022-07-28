# import
#from dataprep.eda import create_report
from Funcoes.LimpaDataFrame import *
from Funcoes.LibPartidas import *
from Funcoes.RetrieveDataFromRepository import *
import matplotlib.pyplot as plt
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
# print(cartola2022)
RodadaAtual = GetRodadaAtual(cartola2022)
print(RodadaAtual)
# Inserir no dataframe se a pontuação do jogador na rodada X foi ou nao como jogador da casa
GetPartidasByRodada(cartola2022, RodadaAtual)

#%%
