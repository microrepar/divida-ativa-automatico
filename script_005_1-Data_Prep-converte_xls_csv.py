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

import contextlib
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from RPA.Desktop import Desktop
from rpapy.core import click_vision, double_click_vision, write_text_vision

from config import Config

today = datetime.today()
file_directory = Config.DIR_DESTINO / 'xls'
summary_file = Path.cwd() / "data" / "processed" / f"summary_.pkl"

# for f in list(file_directory.glob('*.xls'))[:5]:
#     print(f.name)

in_files = [f for f in file_directory.glob('*.xls')]
# print(in_files[:5])

desktop = Desktop()

for file_ in in_files:
    
    file_csv = file_.parent.parent / 'csv'
    with contextlib.suppress(Exception):
        file_csv.mkdir()
    
    file_csv = file_csv / file_.name
    file_csv = file_csv.with_suffix('.csv')

    print('>>>>>>converting>>>>>>', file_csv.name)
    
    if file_csv.exists(): 
        continue

    workbook = desktop.open_file(file_)
    
    click_vision('btn_sim_continuar', before=1, ignore_error=True, max_wait=60)
    click_vision('btn_sim_continuar', before=1, max_wait=3, ignore_error=True)
    
    click_vision('btn_menu_arquivo', before=1, ignore_error=True)
    
    for _ in range(50):
        try:
            double_click_vision('btn_item_salvar_como', before=1, after=2, max_wait=10)
            break
        except:
            time.sleep(5)
            click_vision('btn_menu_arquivo', before=2, max_wait=10)
        
    double_click_vision('btn_procurar', before=1)

    write_text_vision('campo_nome_arquivo', text=str(file_csv.parent) + '{ENTER}', before=2, after=1, move_x=200)

    click_vision('label_tipo_ext', move_x=200, after=1)
    click_vision('list_item_csv_utf8', before=1)
    
    click_vision('btn_salvar', before=1, after=15)
    
    workbook.stop()

