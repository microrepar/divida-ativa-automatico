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
    str_data_inicio = f"01/01/{ano}"
    str_data_fim = f"31/12/{ano}"

    nome_arquivo = f"parcelamento-cancelados-processo-judicial-filtro{0}-{str_data_inicio}-{str_data_fim}.xls".replace("/", ".")

    file_xls = diretorio_destino / nome_arquivo

    if file_xls.exists():
        continue

    for _ in range(3):
        try:

            driver = get_divida_ativa_driver()

            link_consulta_inscritos = get_element_by_xpath(driver, '//b[contains(text(), "- Parcelamentos") and contains(text(), "processo ")]//ancestor::a', max_wait=20)
            link_consulta_inscritos.click()

            radio_por_pagamento = get_element_by_xpath(driver, '//b[contains(text(), "Por Pagamento")]//preceding::input[1]')
            # radio_por_cancelamento = get_element_by_xpath(driver, '//b[contains(text(), "Por Cancelamento")]//preceding::input[1]')
            # radio_primeira_parcela_paga = get_element_by_xpath(driver, '//b[contains(text(), "Primeira parcela paga")]//preceding::input[1]')

            radio_por_pagamento.click()

            saldo_parcela_acima_de = get_element_by_xpath(driver, '//input[@name="pr_vlrtotal"]')
            saldo_parcela_acima_de.clear()
            saldo_parcela_acima_de.send_keys('0,01')

            data_inicio_field = get_element_by_xpath(driver, '//input[@name="dt_ini"]', max_wait=20)
            data_inicio_field.clear()
            data_inicio_field.send_keys(str_data_inicio)

            data_fim_field = get_element_by_xpath(driver, '//input[@name="dt_fim"]', max_wait=20)
            data_fim_field.clear()
            data_fim_field.send_keys(str_data_fim)

            click_vision('btn_continuar')

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
                text='{VK_CONTROL down}a{DELETE}{VK_CONTROL up}{VK_SHIFT up}' + nome_arquivo, 
                backend='uia', 
                move_x=100, 
                max_wait=30,
                after=5)

            # Altera o nome do documento que e preciona enter para salvar
            write_text_vision(
                'campo_nome_destino', 
                text='{ENTER}', 
                backend='uia', 
                move_x=100, 
                max_wait=30,
                after=5)
            
            print("Download concluído:", nome_arquivo)

            time.sleep(10)
            break
        
        except Exception as error:
            time.sleep(5)
        finally:
            with contextlib.suppress(Exception):
                driver.close()
    else:   #forelse
        registrar_arquivo_nao_encontrado(nome_arquivo)