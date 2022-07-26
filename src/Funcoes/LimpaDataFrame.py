def RetiraColunasIndesejadas(data, ColunasDesejadas):
    data = data[ColunasDesejadas]
    return data
# endFunction


def GetRodadaAtual(data):
    RodadaAtual = data['atletas.rodada_id'].max()
    return RodadaAtual
# endFunction
