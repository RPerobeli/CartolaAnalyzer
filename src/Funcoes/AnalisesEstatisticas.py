import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def AnalisarParametrosJogadores(dfJogadores):
    jogadoresId = dfJogadores['atletas.atleta_id'].unique()

    ListaDicionariosParametrosJogadores = []
    ParametrosJogador = {}
    indice = 0
    for id in jogadoresId:
        
        dfJogador = dfJogadores.query(f'`atletas.atleta_id`== {id}')
        nomeJogadorList = dfJogador['atletas.slug'].unique()
        nomeJogador = nomeJogadorList[0]
        clubeJogadorList = dfJogador['atletas.clube.id.full.name'].unique()
        clubeJogador = clubeJogadorList[0]

        dfJogador = dfJogador.query(f'`atletas.pontos_num` != 0')
        print(dfJogador['atletas.pontos_num'].describe())
        ax = sns.boxplot(y=dfJogador['atletas.pontos_num'])
        plt.show()

        """mediaJogador = dfJogador['atletas.pontos_num'].mean()
        desvioPadraoJogador = dfJogador['atletas.pontos_num'].std()
        if(dfJogador['atletas.pontos_num'].size < 5):
            mediaMovelJogador = dfJogador['atletas.pontos_num'].mean()
        else:
            mediaMovelJogador = dfJogador['atletas.pontos_num'].values[range(-5,0)].mean()

        ParametrosJogador = {'Id': id, 'Nome' : nomeJogador, 'Media': mediaJogador, 'MediaMovel': mediaMovelJogador, 'DesvioPadrao': desvioPadraoJogador, "Clube": clubeJogador}
        df = pd.DataFrame(ParametrosJogador, index=[indice])
        indice += 1
        ListaDicionariosParametrosJogadores.append(df)   """
        break
    # endfor
    #dfParametrosTodosJogadores = pd.concat(ListaDicionariosParametrosJogadores)
    #return dfParametrosTodosJogadores
# endFunction

""" (['atletas.atleta_id', 'atletas.rodada_id', 'atletas.clube_id',
       'atletas.status_id', 'atletas.pontos_num', 'atletas.posicao_id',
       'atletas.preco_num', 'atletas.variacao_num', 'atletas.media_num',
       'atletas.jogos_num', 'atletas.slug', 'atletas.nome', 'rodada',
       'atletas.clube.id.full.name'] """