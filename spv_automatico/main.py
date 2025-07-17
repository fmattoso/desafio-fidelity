# ===================== main.py =====================
# Lógica principal do sistema

import datetime
import time
from tqdm import tqdm
import banco
import navegador

FILTROS_VALIDOS = [0, 1, 2, 3]

class SPVAutomatico:

    def __init__(self, filtro=0):
        self.filtro = filtro

    def executar(self):
        filtro = self.filtro
        pesquisas = banco.buscar_pesquisas(filtro)
        tempo_inicio = datetime.datetime.now()

        if pesquisas:
            for registro in tqdm(pesquisas, desc=f"Filtro {filtro}"):
                codPesquisa = registro[1]
                nome = registro[4]
                cpf = registro[5]
                rg = registro[6]

                documento = None
                if filtro == 0 and cpf:
                    documento = cpf
                elif filtro in (1, 3) and rg:
                    documento = rg
                elif filtro == 2 and nome:
                    documento = nome

                if documento:
                    page = navegador.carregar_site(filtro, documento)
                    resultado = navegador.interpretar_resultado(page)
                    banco.salvar_resultado(codPesquisa, resultado, filtro)

                if (datetime.datetime.now() - tempo_inicio).total_seconds() > 600:
                    break

            if filtro < max(FILTROS_VALIDOS):
                SPVAutomatico(filtro + 1).executar()
            else:
                navegador.restartar_programa()
        else:
            print("Nenhuma pesquisa encontrada. Aguardando...")
            time.sleep(60)
            navegador.restartar_programa()

if __name__ == "__main__":
    spv = SPVAutomatico(0)
    spv.executar()
