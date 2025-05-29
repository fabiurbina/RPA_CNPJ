
from selenium import webdriver  # Inicializa o navegador
from selenium.webdriver.chrome.service import Service  # Serviço do ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Gerencia o download do ChromeDriver
from selenium.webdriver.common.by import By  # Localizadores de elementos (ID, XPATH, etc.)
from selenium.webdriver.support.ui import WebDriverWait  # Esperas explícitas
from selenium.webdriver.support import expected_conditions as EC  # Condições esperadas para WebDriverWait
from selenium.webdriver.common.keys import Keys  # Simulação de teclas do teclado
from selenium.webdriver.chrome.options import Options  # Configurações do Chrome
from selenium.webdriver.support.ui import Select  # Manipulação de dropdowns
from selenium.webdriver.common.action_chains import ActionChains  # Ações avançadas como mouseover
from selenium.common.exceptions import (  # Tratamento de exceções específicas do Selenium
    TimeoutException, NoSuchElementException, ElementNotInteractableException,
    UnexpectedTagNameException, StaleElementReferenceException)
import time
import re
import requests
from requests.auth import HTTPBasicAuth
import time
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path



def executar_automacao(dados = None):

    load_dotenv()

    # Pega as variáveis de ambiente
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TOKEN_URL = os.getenv("TOKEN_URL")
    CNPJ_API_URL = os.getenv("CNPJ_API_URL")
    CNPJ_API_URL_1 = os.getenv("CNPJ_API_URL_1")
    SITE = os.getenv("SITE")

    # Armazena token atual em cache
    token_data = {
        "access_token": None,
        "expires_at": 0
    }

    # === FUNÇÃO PARA GERAR TOKEN ===
    def gerar_token():
        response = requests.post(
            TOKEN_URL,
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            token_json = response.json()
            token_data["access_token"] = token_json["access_token"]
            token_data["expires_at"] = time.time() + token_json["expires_in"] - 10
            print("✅ Novo token gerado com sucesso!")
        else:
            raise Exception(f"Erro ao gerar token: {response.status_code} - {response.text}")

    # === RETORNA TOKEN VÁLIDO ===
    def get_token():
        if token_data["access_token"] is None or time.time() > token_data["expires_at"]:
            gerar_token()
        return token_data["access_token"]


    # === FUNÇÃO DE CONSULTA AO CNPJ ===
    def consultar_cnpj(cnpj: str, id_finalidade: int = 1):
        headers = {
            "Authorization": f"Bearer {get_token()}",
            "Accept": "application/json"
        }

        params = {
            "cnpj": cnpj,
            "idFinalidade": id_finalidade
        }

        response = requests.get(CNPJ_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na consulta do CNPJ: {response.status_code} - {response.text}")
        

    #=== FUNÇÃO DE CONSULTA AO CPF ===
    def consultar_cpf(cpf: str, id_finalidade: int = 1):
        headers = {
            "Authorization": f"Bearer {get_token()}",
            "Accept": "application/json"
        }

        params = {
            "cpf": cpf,
            "idFinalidade": id_finalidade
        }

        response = requests.get(CNPJ_API_URL_1, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na consulta do cpf: {response.status_code} - {response.text}")
        


    #FIXME: AQUI FUNCIONA O RPA
    def abrir_site(url):

        options = webdriver.ChromeOptions()

        # 🔧 Reduz o consumo bloqueando imagens
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)

        # ⚙️ Argumentos para deixar o Chrome leve
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-hang-monitor')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-prompt-on-repost')
        options.add_argument('--disable-web-security')
        
        #Abre o site da neoway
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        #time.sleep(10000)
    #---------------------------------------------------------------------------------------------------------------------------------------------

    #função para fechar tela aberta no momento
        try:
            wait = WebDriverWait(driver, 50)
                            # Aguarda a opção específica estar presente
            irparalog = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="username-input"]')
                ))

            irparalog.send_keys("neoway@rnradv.com.br")
        except TimeoutException:
            print("Campo não localizado, verificar codigo!")
        
    #---------------------------------------------------------------------------------------------------------------------------------------------
        #função para colocar a senha    
        try:
            wait = WebDriverWait(driver, 50)
                            # Aguarda a opção específica estar presente
            Senha = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="password-input"]')
                ))

            Senha.send_keys("Rnradv2025*")
        except TimeoutException:
            print("Campo não localizado, verificar codigo!")
        


    #---------------------------------------------------------------------------------------------------------------------------------------------
        #função para colocar a senha    
        try:
            wait = WebDriverWait(driver, 50)
                            # Aguarda a opção específica estar presente
            submit = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="login"]')
                ))

            submit.click()
        except TimeoutException:
            print("Campo não localizado, verificar codigo!")
        


        #---------------------------------------------------------------------------------------------------------------------------------------------
        #função para colocar a senha    
        try:
            wait = WebDriverWait(driver,50)
                            # Aguarda a opção específica estar presente
            search = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div[1]/ul/li[1]/div/img')
                ))

            search.click()
        except TimeoutException:
            print("Campo não localizado, verificar codigo!")
        #time.sleep(10000)
        
    #---------------------------------------------------------------------------------------------------------------------------------------------
        #Aguarda a interação do usuário  
        while True:
            entrada = input("Digite 'OK' para continuar: ")
            if entrada.strip().upper() == "OK":
                break
            print("Aguardando você digitar 'OK'...")

        print("Você digitou OK. Continuando o código...")
        #
        try:
        # Localiza o elemento que mostra o total de registros
            elemento_total = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/section/div/div[1]/div[3]/div[2]/div[2]/div/span')
            texto = elemento_total.text.strip()  # exemplo: "de  659.785"

            # Extrai o número usando regex
            match = re.search(r"[\d\.]+", texto)
            if match:
                total_str = match.group().replace('.', '')
                total = int(total_str)
                print(f"🔢 Total de registros encontrados: {total}")
            else:
                print("❌ Não foi possível extrair o número.")

        except Exception as e:
            print(f"❌ Erro ao buscar o total de registros: {e}")

        #time.sleep(100000)
    #---------------------------------------------------------------------------------------------------------------------------------------------
        cnpjs = []

        while True:
            try:
                total_paginas = int(input("🔢 Digite o número total de páginas que deseja processar: "))
                if total_paginas <= 0:
                    raise ValueError
                break
            except ValueError:
                print("❌ Valor inválido. Digite um número inteiro positivo.")

        wait = WebDriverWait(driver, 200)
        for pagina in range(1, total_paginas + 1):
            print(f"\n📄 Página {pagina}")
            
            # Espera o primeiro CNPJ da página estar visível para garantir que carregou
            try:
                wait.until(EC.visibility_of_element_located((
                    By.XPATH,
                    '//*[@id="main-wrapper"]/section/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[2]/p'
                )))


                time.sleep(5)
            except:
                print(f"⚠️ Tempo esgotado esperando carregar a página {pagina}")
                break

            # Coleta os CNPJs da página
            for i in range(1, 101):
                try:
                    xpath = f'//*[@id="main-wrapper"]/section/div/div[1]/div[3]/div[2]/div[1]/div[{i}]/div/div[2]/div/div[1]/div/div[2]/p'
                    elemento = driver.find_element(By.XPATH, xpath)
                    cnpjs.append(elemento.text.strip())
                except:
                    break  # Sai do loop se não encontrar mais elementos
            
            # Tenta clicar para ir para a próxima página
            try:
                botao_proxima = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@id="main-wrapper"]/section/div/div[1]/div[3]/div[2]/div[2]/ul/li[2]/a'
                )))
                botao_proxima.click()
            except Exception as e:
                print(f"❌ Erro ao clicar para ir à próxima página: {e}")
                break

        # Mostra os CNPJs coletados
        print(f"🔢 Total de CNPJs coletados: {len(cnpjs)}")
        cnpj_filtrados = cnpjs[:2]
        return cnpj_filtrados
        


    import pandas as pd
    import re

    # Suas funções consultar_cnpj e consultar_cpf devem estar definidas anteriormente

    def extrair_dados_cnpj(cnpj_para_consulta: str, id_finalidade: int = 1) -> pd.DataFrame:
        try:
            resultado = consultar_cnpj(cnpj_para_consulta, id_finalidade=id_finalidade)

            cnpj = resultado.get("resposta", {}).get("dadosCadastrais", {})
            df_cnpj = pd.DataFrame([cnpj]) if cnpj else pd.DataFrame()

            socios = resultado.get("resposta", {}).get("socios", [])
            df_socios = pd.DataFrame(socios) if socios else pd.DataFrame()

            celulares = resultado.get("resposta", {}).get("telefones", {}).get("moveis", [])
            celulares_formatados = [tel.get("numero") for tel in celulares]
            df_celulares = pd.DataFrame(celulares_formatados, columns=["celular"])

            max_linhas = max(len(df_socios), len(df_celulares), 1)
            if not df_cnpj.empty:
                df_cnpj = pd.concat([df_cnpj] * max_linhas, ignore_index=True)

            df_socios = df_socios.reindex(range(max_linhas)).reset_index(drop=True)
            df_celulares = df_celulares.reindex(range(max_linhas)).reset_index(drop=True)

            df_resultado = pd.concat([df_socios, df_celulares, df_cnpj], axis=1)

            df_resultado_novo = pd.DataFrame({
                'documento': df_resultado.get('documento'),
                'razaoSocial': df_resultado.get('razaoSocial'),
                'cnpj': df_resultado.get('cnpj'),
                'cnaeGrupo': df_resultado.get('cnaeGrupo'),
                'nomeOuRazaoSocial': df_resultado.get('nomeOuRazaoSocial'),
                'celularCartaoCNPJ': df_resultado.get('celular')
            })

            df_resultado_novo['documento'] = df_resultado_novo['documento'].astype(str).str.replace(r'\D', '', regex=True)
            df_resultado_novo = df_resultado_novo[df_resultado_novo['documento'].str.strip() != '']
            df_resultado_novo = df_resultado_novo.reset_index(drop=True)

            return df_resultado_novo

        except Exception as e:
            print(f"Erro ao extrair dados do CNPJ {cnpj_para_consulta}: {e}")
            return pd.DataFrame()


    def extrair_telefones_cpf(cpf_para_consulta: str, id_finalidade: int = 1) -> pd.DataFrame:
        try:
            if not cpf_para_consulta.strip():
                raise ValueError("CPF vazio.")

            resultado = consultar_cpf(cpf_para_consulta, id_finalidade=id_finalidade)
            telefones = resultado.get("resposta", {}).get("telefones", {})
            lista_telefones = []

            for tipo, chave in [('fixo', 'fixos'), ('móvel', 'moveis')]:
                for tel in telefones.get(chave, []):
                    lista_telefones.append({
                        "cpf": cpf_para_consulta,
                        "tipo": tipo,
                        "numero": tel.get("numero"),
                        "whatsApp": tel.get("aplicativos", {}).get("whatsApp", False),
                        "ultimo_contato": tel.get("ultimoContato"),
                        "relacao": tel.get("relacao")
                    })

            return pd.DataFrame(lista_telefones)

        except Exception as e:
            print(f"Erro ao extrair telefones do CPF {cpf_para_consulta}: {e}")
            return pd.DataFrame()


    def extrair_telefones_varios_cpfs(lista_cpfs, id_finalidade=1):
        df_final = pd.DataFrame()

        for cpf in lista_cpfs:
            df_telefone = extrair_telefones_cpf(cpf, id_finalidade)
            if not df_telefone.empty:
                df_final = pd.concat([df_final, df_telefone], ignore_index=True)

        return df_final if not df_final.empty else pd.DataFrame()



    if __name__ == "__main__":
        # === Parte 0: Obter lista de CNPJs de outra função
        lista_cnpjs = abrir_site(SITE)  # Essa função deve retornar uma lista de strings com os CNPJs
        print(lista_cnpjs)
        #time.sleep(10000)
        # === Parte 1: Consultar dados por vários CNPJs
        df_resultado_total = pd.DataFrame()

        for cnpj in lista_cnpjs:
            df_temp = extrair_dados_cnpj(cnpj)
            if not df_temp.empty:
                df_resultado_total = pd.concat([df_resultado_total, df_temp], ignore_index=True)

        if df_resultado_total.empty:
            print("Nenhum dado retornado das consultas de CNPJs.")
        else:
            print("✅ Dados dos CNPJs consultados:")
            print(df_resultado_total)

            #df_resultado_total.to_excel("socios_com_celulares.xlsx", index=False)

            # === Parte 2: Buscar telefones por CPF
            lista_cpfs = df_resultado_total['documento'].dropna().tolist()
            df_telefones = extrair_telefones_varios_cpfs(lista_cpfs)

            df_resultado_total = df_resultado_total.rename(columns={"documento": "cpf"})
            df_completo = pd.merge(df_telefones, df_resultado_total, on='cpf', how='left')

            # Reorganiza as colunas
            colunas = [
                'cpf', 'nomeOuRazaoSocial', 'razaoSocial', 'cnpj', 'cnaeGrupo',
                'tipo', 'numero', 'whatsApp', 'celularCartaoCNPJ'
            ]
            df_completo = df_completo[colunas]

            # Pega o caminho da pasta Downloads do usuário
            downloads_path = str(Path.home() / "Downloads")

            # Nome do arquivo
            arquivo = "resultado_completo.xlsx"

            # Caminho completo do arquivo na pasta Downloads
            caminho_arquivo = os.path.join(downloads_path, arquivo)

            # Salva o DataFrame lá
            df_completo.to_excel(caminho_arquivo, index=False)

            # Exibição
            if not df_telefones.empty:
                #print("\n📞 Telefones encontrados:")
                print(df_completo)
            else:
                print("❌ Nenhum telefone encontrado para os CPFs fornecidos.")

if __name__ == "__main__":
    resultado = executar_automacao()
    print(resultado)
