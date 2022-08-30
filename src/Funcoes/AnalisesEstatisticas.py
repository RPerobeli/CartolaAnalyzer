import pandas as pd
import numpy as np


def AnalisarParametrosJogadores(dfJogadores):
    jogadoresId = dfJogadores['atletas.atleta_id'].unique()
    for id in jogadoresId:
        dfJogador = dfJogadores.query(f'`atletas.atleta_id`== {id}')
        #separar os dados calculados em um novo dataframe e retornar para o main
    #endfor
# endFunction
