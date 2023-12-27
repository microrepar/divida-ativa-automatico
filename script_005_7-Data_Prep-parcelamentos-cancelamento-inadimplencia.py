#!/usr/bin/env python
# coding: utf-8

# ## Divída Ativa
# 
# More background on the project
# 
# ### Data Sources
# - file1 : Description of where this file came from
# 
# ### Changes
# - 12-18-2023 : Started project
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import Config

# ### File Locations
today = datetime.today()
nome_arquivo = 'parcelamentos-cancelamento-inadimplencia'
file_directory = Config.DIR_DESTINO / "csv"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{nome_arquivo}.pkl"

in_files = [f for f in file_directory.glob('*.csv') 
            if f.name.startswith(nome_arquivo)]

dtypes = {
    'Inscrição': 'string',
    'Ano': 'Int64',
    'Numero': 'Int64',
}

dataframe_list = []
for file_ in in_files:
    try:
        dfi = pd.read_csv(file_, skiprows=1, sep=';')
        if dfi.shape[0] > 0:
            contador = 0
            while contador <= 10:
                if 'Inscrição' in dfi.columns:
                    break
                columns = dfi.iloc[0]
                dfi.columns = columns
                dfi = dfi.iloc[1:]
                # print(dfi.columns)
                contador += 1
            dataframe_list.append(dfi)
            
        # print(dfi.columns, file_)

    except Exception  as error:
        print(error)
    

if dataframe_list:
    print('Qtd dataframes', len(dataframe_list))
    for dfi in dataframe_list:
        print(dfi.shape)
        
    df = pd.concat(dataframe_list, ignore_index=True)
    print(df.shape)
    df.head()

    # https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
    df.columns = [x.strip() for x in df.columns]

    cols_to_rename = {'col1': 'New_Name'}
    df.rename(columns=cols_to_rename, inplace=True)

    df.to_pickle(summary_file)
else:
    print(f'Nenhum dado foi encontrado nos arquivos .csv que iniciam com "{nome_arquivo}"')
