import pandas as pd                # Abrir e concatenar bancos de dados
import Funcoes.LibPartidas as LibPartidas
import Funcoes.LibJogadores as  LibJogadores

def FiltraColunasDesejadas(data, ColunasDesejadas):
    data = data[ColunasDesejadas]
    return data
# endFunction

def RetrievePartidasFromApi(rodadaAtual):
    ListaPartidasPorRodada = []
    DictPartidas = {}
    partidas = LibPartidas.GetPartidasByRodada(rodadaAtual)
    DictPartidas[rodadaAtual] = partidas['partidas']
    for key, item in DictPartidas.items():
        df = pd.DataFrame(item)
        df['rodada'] = key
        ListaPartidasPorRodada.append(df)
    # endfor
    dfPartidasAteoMomento = pd.concat(ListaPartidasPorRodada)
    return dfPartidasAteoMomento
# endFunction


def RetrieveJogadoresFromApi():
    jogadores = LibJogadores.GetJogadores()
    df_jogadores = pd.DataFrame.from_dict(jogadores)

    colunasDesejadas = [
        'minimo_para_valorizar',
        'jogos_num',
        'atleta_id', 
        'rodada_id',
        'clube_id',
        'posicao_id',
        'status_id',
        'pontos_num',
        'media_num',
        'variacao_num',
        'preco_num',
        'entrou_em_campo',
        'apelido'
    ]
    df_jogadores = FiltraColunasDesejadas(df_jogadores, colunasDesejadas)
    return df_jogadores
#endFunction