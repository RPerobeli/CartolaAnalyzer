import pandas as pd                # Abrir e concatenar bancos de dados
import Funcoes.LibPartidas as LibPartidas
import Funcoes.LibJogadores as  LibJogadores
import Funcoes.LibClubes as LibClubes
import Funcoes.LimpaDados as LimpaDados

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

def RetrieveJogadoresRodadasAntigasFromApi(rodadaAtual):
    ListaJogadoresPorRodada = []
    for i in range(rodadaAtual-5, rodadaAtual):
        if(i<=0):
            continue
        atletasrodada = LibJogadores.GetJogadoresByRodada(i)
        df_jogadores = pd.DataFrame.from_dict(atletasrodada)
        df_jogadores = df_jogadores.transpose().reset_index()
        df_jogadores['rodada'] = i
        colunasDesejadas = [
        'rodada',
        'index',
        'apelido',
        'pontuacao', 
        'entrou_em_campo'
        ]
        df_jogadores = FiltraColunasDesejadas(df_jogadores, colunasDesejadas)
        ListaJogadoresPorRodada.append(df_jogadores)
    # endfor
    df = pd.concat(ListaJogadoresPorRodada).reset_index(drop=True)
    df = LimpaDados.CalculaMediaMovel(df)
    df = LimpaDados.CalculaDesvioPadrao(df)
    print(df)
    df = df.groupby(['index','media_movel','desv_padrao']).max().reset_index()
    return df
# endFunction




def RetrieveClubesFromApi():
    clubes = LibClubes.GetClubes()
    df_clubes = pd.DataFrame.from_dict(clubes)
    return df_clubes
#endFunction

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