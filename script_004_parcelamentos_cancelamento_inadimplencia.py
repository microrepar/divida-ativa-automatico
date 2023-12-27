#!/usr/bin/env python
# coding: utf-8
import contextlib
import time
from pathlib import Path

from rpapy.core import click_vision, write_text_vision
from selenium.webdriver.support import expected_conditions as EC

from config import Config
from divida_ativa_page import (get_divida_ativa_driver, get_element_by_xpath,
                               registrar_arquivo_nao_encontrado)

diretorio_destino = Config.DIR_DESTINO
    
diretorio_destino = diretorio_destino / 'xls'
with contextlib.suppress(Exception):
    diretorio_destino.mkdir()

for ano in range(Config.ANO_FINAL, Config.ANO_INICIAL-1, -1):

    nome_arquivo = f"parcelamentos-cancelamento-inadimplencia-{ano}.xls".replace("/", ".")

    file_xls = diretorio_destino / nome_arquivo

    if file_xls.exists():
        continue

    for _ in range(3):
        
        try:            
            driver = get_divida_ativa_driver()

            link_consulta_inscritos = get_element_by_xpath(
                driver, ('//b[contains(text(), "- Parcelamentos") and '
                        'contains(text(), "inadimplencia")]//ancestor::a'), max_wait=20)
            link_consulta_inscritos.click()

            ano_inicial_parcelamento = get_element_by_xpath(
                driver, '//input[@name="ano_ini"]')
            ano_inicial_parcelamento.clear()
            ano_inicial_parcelamento.send_keys(ano)

            dias_atraso = get_element_by_xpath(
                driver, '//input[@name="dias_atraso"]')
            dias_atraso.clear()
            dias_atraso.send_keys('60')

            click_vision('btn_continuar', before=1)

            # Altera o diretório
            write_text_vision(
                "campo_nome_destino",
                text=str(diretorio_destino.absolute()) + '{ENTER}',
                # backend="uia",
                move_x=100,
                max_wait=Config.MAX_WAIT or 5000,
                after=3,
            )

            # Altera o nome do documento que e preciona enter para salvar
            write_text_vision(
                'campo_nome_destino', 
                text='{VK_CONTROL down}a{DELETE}{VK_CONTROL up}{VK_SHIFT up}'+ nome_arquivo, 
                backend='uia', 
                move_x=100, 
                max_wait=30,
                after=3)

            # Altera o nome do documento que e preciona enter para salvar
            write_text_vision(
                'campo_nome_destino', 
                text='{ENTER}', 
                backend='uia', 
                move_x=100, 
                max_wait=30,
                after=3)
            
            print("Download concluído:", nome_arquivo)
            
            
            break

        except Exception as error:
            time.sleep(5)
            
        finally:
            with contextlib.suppress(Exception):
                driver.close()
    else:   #forelse
        registrar_arquivo_nao_encontrado(nome_arquivo)