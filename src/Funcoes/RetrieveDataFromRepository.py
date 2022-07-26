
import re                          # Expressão regulares
import requests                    # Acessar páginas da internet
from bs4 import BeautifulSoup      # Raspar elementos de páginas da internet
import pandas as pd                # Abrir e concatenar bancos de dados


def RetrieveDataFromRepository(year):
    # URL com caminho do repositório
    URL = f'https://github.com/henriquepgomide/caRtola/tree/master/data/{year}'
    html = requests.get(URL)
    # Criar objeto BeautifulSoup para raspar urls
    soup = BeautifulSoup(html.text, 'lxml')
    # print(soup)
    '''
    Selecionar aqueles href que:
    a) possuem o padrão rodada-[número de um ou dois dígitos]
    b) terminam com csv.
    '''
    regex = 'rodada-([0-9]|[0-9][0-9])\.csv'

    dict_of_files = {}
    # Encontrar tags de nosso interesse
    for tag in soup.find_all('a', attrs={'href': re.compile(regex)}):
        href_str = tag.get('href')
        file_name = re.sub(f'/henriquepgomide/caRtola/blob/master/data/{year}/',   # Substituir padrão por nada
                           '',
                           href_str)

        file_url = re.sub(f'/henriquepgomide/caRtola/blob/master/data/{year}/',    # Substituir padrão por links para arquivos raw
                          f'https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/{year}/',
                          href_str)

        dict_of_files[file_name] = file_url
    # endfor
    # print(list(dict_of_files.items())[0])

    # Ler os dataframes dos arquivos
    list_of_dataframes = []
    for key, item in dict_of_files.items():
        df = pd.read_csv(item)
        df['rodada'] = key
        list_of_dataframes.append(df)
    # endfor
    cartolaDF = pd.concat(list_of_dataframes)
    cartolaDF = cartolaDF[cartolaDF['atletas.posicao_id'] != 'tec']
    return cartolaDF

# endFunction
