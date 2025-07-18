from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def testar_chromedriver():
    # Caminho para o chromedriver 
    caminho_driver = "/usr/bin/chromedriver"

    # Configurações do Chrome headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializa o driver
    try:
        service = Service(caminho_driver)
        driver = webdriver.Chrome(service=service, options=options)

        print("- ChromeDriver iniciado com sucesso!")

        # Acessa uma página simples
        driver.get("https://www.google.com")

        titulo = driver.title
        print(f"- Título da página: {titulo}")

        # Verifica se o título contém "Google"
        assert "Google" in titulo
        print("- Teste de título: OK")

        driver.quit()
        print("- Navegador fechado com sucesso!")

    except Exception as e:
        print("- Ocorreu um erro ao iniciar o ChromeDriver:")
        print(str(e))

if __name__ == "__main__":
    testar_chromedriver()
