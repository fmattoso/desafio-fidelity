# Módulo: navegador.py (responsável por interação com o Selenium)

import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Detecta o sistema operacional
sistema = platform.system().lower()

# EXECUTAVEL = 'C:/Users/teste/OneDrive/Documentos/'

NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
CONSTA01 = 'Processos encontrados'
CONSTA02 = 'Audiências'

# Inicializa o navegador correto com base no sistema

def iniciar_navegador():
    if sistema == "windows":
        edge_driver_path = os.path.expanduser("~/Documents/msedgedriver.exe")
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = EdgeService(executable_path=edge_driver_path)
        driver = webdriver.Edge(service=service, options=options)
    else:
        chrome_driver_path = "/usr/bin/chromedriver" 
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    return driver

def carregar_site(filtro, documento):
    browser = iniciar_navegador()
    browser.get("https://esaj.tjsp.jus.br/cpopg/open.do")

    try:
        # select_el = browser.find_element('xpath','//*[@id="cbPesquisa"]')
        # Aguardar até que o elemento esteja disponível
        select_el = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cbPesquisa"]'))
        )
        select_ob = Select(select_el)

        if filtro in (0, 1, 3):
            select_ob.select_by_value('DOCPARTE')
            browser.find_element('xpath','//*[@id="campo_DOCPARTE"]').send_keys(documento)
        elif filtro == 2:
            select_ob.select_by_value('NMPARTE')
            browser.find_element('xpath','//*[@id="pesquisarPorNomeCompleto"]').click()
            browser.find_element('xpath','//*[@id="campo_NMPARTE"]').send_keys(documento)

        browser.find_element('xpath','//*[@id="botaoConsultarProcessos"]').click()

        browser.implicitly_wait(3)
        # Salvar o conteúdo em um arquivo (teste)
        # with open(f'browser.page_source_{filtro}.html', 'w', encoding='utf-8') as file:
        #    file.write(browser.page_source)        
            
        return browser.page_source

    except Exception as e:
        print(f"Erro ao carregar o site: {e}")
        time.sleep(120)
        restartar_programa()


def interpretar_resultado(page):
    if NADA_CONSTA in page:
        return 1  # Nada consta
    elif (CONSTA01 in page or CONSTA02 in page) and ('Criminal' in page or 'criminal' in page):
        return 2  # Consta criminal
    elif (CONSTA01 in page or CONSTA02 in page) and ('Cível' in page or 'cível' in page):
        return 5  # Consta cível
    return 7  # Resultado indefinido


def restartar_programa():
    import sys
    python = sys.executable
    os.execl(python, python, *sys.argv)
