from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import streamlit as st
import base64
import subprocess
import os
import pandas as pd
import locale


servico = Service(ChromeDriverManager().install())


caminho_script = 'VinWebClickMMR.py'

comando = ['streamlit', 'run', '--server.address', 'localhost', '--server.port', '8501', caminho_script]

resultado = subprocess.run(comando)

st.set_page_config(layout="wide")

def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

#side_bg = 'FundoStreamlit.jpg'
side_bg = 'LogoStreamlitCarAuctionSmart.jpg'

sidebar_bg(side_bg)

st.sidebar.title('')


col1, col2, col3 = st.columns([4, 1, 15])

col1.subheader('')
col1.subheader('Preencha!')
col3.title('CarAuction Smart')


opcoesgrades = ["Grade**", 5.0 , 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0]


VIN = col1.text_input('Digite VIN Number')
ODO = col1.text_input('Digite Odometro do Carro')
opcao_selecionada = col1.selectbox('Selecione a Grade:', opcoesgrades)




if opcao_selecionada == 5.0:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[2]/span
    botao = 2

elif opcao_selecionada == 4.5:

    #
    botao = 7

elif opcao_selecionada == 4.0:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[12]/span
    botao = 12
    

elif opcao_selecionada == 3.5:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[17]/span
    botao = 17
    

elif opcao_selecionada == 3.0:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[22]/span
    botao = 22

elif opcao_selecionada == 2.5:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[27]/span
    botao =  27

elif opcao_selecionada == 2.0:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[32]/span
    botao = 32

elif opcao_selecionada == 1.5:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[37]/span
    botao = 37

elif opcao_selecionada == 1.0:

    #//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[42]/span
    botao = 42

else:
    
    botao = 1


if st.button('Ok') and VIN:


    navegador = webdriver.Chrome(service=servico)
    navegador.minimize_window()
    navegador1 = webdriver.Chrome(service=servico)
    navegador1.minimize_window()
    
    #Conectar na pagina
    navegador.get("https://api.manheim.com/auth/authorization.oauth2?adaptor=manheim_customer&client_id=zdvy6trhqhe94qvmzpkq7v52&redirect_uri=https://mmr.manheim.com/oauth/callback&response_type=code&scope=profile+openid+email&signup=manheim&state=country%3DUS%26popup%3Dtrue%26source%3Dman")

    navegador.minimize_window()


    navegador1.get(f'https://www.cargurus.com/Cars/instantMarketValueFromVIN.action?startUrl=%2FCars%2Fl-Used-2017-Toyota-RAV4-c26004&++++++++carDescription.vin%0D%0A={VIN}')

    navegador1.minimize_window()
    #time.sleep(1)

    user = navegador.find_element(By.XPATH, '//*[@id="user_username"]')

    user.send_keys("Marciogomesvip")

    senha = navegador.find_element(By.XPATH, '//*[@id="user_password"]')

    senha.send_keys("MIXcds02@#")

    senha.send_keys(Keys.RETURN)

    InputVin = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="vinText"]')))

    InputVin.send_keys(VIN)

    InputVin.send_keys(Keys.RETURN)

    time.sleep(2)

    ODO = pd.to_numeric(ODO)

    Odometro = navegador.find_element(By.XPATH, '//input[@id="Odometer"]')
        

    Odometro.send_keys(str(ODO))


    Odometro.send_keys(Keys.RETURN)

    Combox = WebDriverWait(navegador, 10).until(
       EC.visibility_of_element_located((By.XPATH, '//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div')))
    
    Combox.click()


    # Verifica se o valor é um número válido antes de construir o XPath
    if isinstance(botao, int):
        xpath = '//*[@id="Condition Report"]/div[1]/div/div[1]/div/div[2]/div[2]/button[' + str(botao) + ']/span'
    else:
        raise ValueError('O número do botão deve ser um número inteiro.')

    # Usando a expressão XPath atualizada na função WebDriverWait
    Grade = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    Grade.click()

    time.sleep(1)

    AdjustedMMR = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]')))

    TAdjustedMMR = AdjustedMMR.text
    #col1.text(f' Base MMR = {TBaseMMR}')

    MMRRange = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[2]/span/span[1]')))

    TMMRRange = MMRRange.text
    #col1.text(f' MMR Range = {TMMRRange}')

    EstimatedRetailValue = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[5]/div/div/div/div/div/div[1]')))

    TEstimatedRetailValue = EstimatedRetailValue.text
    #col1.text(f' Estimated Retail Value = {TEstimatedRetailValue}')

    TypicalRange1 = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[5]/div/div/div/div/div/div[2]/div/div[2]/span[1]')))

    TTypicalRange1 = TypicalRange1.text


    TypicalRange2 = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[5]/div/div/div/div/div/div[2]/div/div[2]/span[2]')))

    TTypicalRange2 = TypicalRange2.text

    #col1.text(f' TipicalRange = {TTypicalRange1} - {TTypicalRange2}')

    ModelCarro = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]/h4')))

    ModelCarro = ModelCarro.text


    Download = navegador.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[1]/a[1]')
    
    Download.click()    

    #Auto Check

    ClickAutoCheck = WebDriverWait(navegador, 10).until(
       EC.visibility_of_element_located((By.XPATH, '//*[@id="autoCheckLink"]/span')))
    
    ClickAutoCheck.click()

    #time.sleep(3)

    OldURL = navegador.window_handles[0]


    NewURL = navegador.window_handles[1]

    navegador.switch_to.window(NewURL)


    #time.sleep(5)

    AutoCheckScore = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-skip-to-content"]/div[1]/div[2]/div/div[1]/div[1]/span')))
    
    
    TAutoCheckScore = AutoCheckScore.text

    AutoCheckScoreComparation = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-skip-to-content"]/div[1]/div[2]/div/div[2]/span[1]/p')))

    TAutoCheckScoreComparation = AutoCheckScoreComparation.text

    #col1.text(f' Auto Check Score = {TAutoCheckScore} - {TAutoCheckScoreComparation}')

    MajorStateTitleBrandCheck = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-skip-to-content"]/div[3]/div[1]/div/div/div[1]/div[2]/span')))


    TMajorStateTitleBrandCheck = MajorStateTitleBrandCheck.text
    #col1.text(f' Major State Title Brand Check = {TMajorStateTitleBrandCheck}')


    AcidenteCheck = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-skip-to-content"]/div[3]/div[1]/div/div/div[3]/div[2]/span')))

    TAcidenteCheck = AcidenteCheck.text
    #col1.text(f' Accident Check = {TAcidenteCheck}')

    DamageCheck = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-skip-to-content"]/div[3]/div[1]/div/div/div[5]/div[2]/span')))

    TDamageCheck = DamageCheck.text
    #col1.text(f' Damage Check = {TDamageCheck}')

    #navegador1.get(f'https://www.cargurus.com/Cars/instantMarketValueFromVIN.action?startUrl=%2FCars%2Fl-Used-2017-Toyota-RAV4-c26004&++++++++carDescription.vin%0D%0A={VIN}')

    #navegador1.minimize_window()

    ClickCarGurus = WebDriverWait(navegador1, 10).until(
       EC.visibility_of_element_located((By.XPATH, '//*[@id="searchByVinToggle"]')))
    
    ClickCarGurus.click()
    
    ValueGurus = WebDriverWait(navegador1, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="instantMarketValuePrice"]')))
    

    TValueGurus = ValueGurus.text
    #col1.text(f' Damage Check = {TDamageCheck}')


    # Obtém o caminho absoluto da pasta Downloads
    pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Lista todos os arquivos na pasta Downloads
    arquivos_downloads = os.listdir(pasta_downloads)

    # Filtra apenas os arquivos CSV na lista de arquivos
    arquivos_csv = [arquivo for arquivo in arquivos_downloads if arquivo.endswith('.csv')]

    # Verifica se foram encontrados arquivos CSV
    if len(arquivos_csv) > 0:
        # Obtém o caminho absoluto do arquivo CSV mais recente
        caminho_arquivo = os.path.join(pasta_downloads, max(arquivos_csv, key=lambda arquivo: os.path.getmtime(os.path.join(pasta_downloads, arquivo))))

        # Define as colunas que você quer carregar
        colunas_desejadas = ['Date', 'Price (USD)', 'Odometer (mi)', 'Condition', 'Year', 'Exterior Color']  # substitua pelos nomes das colunas que você quer

        # Carrega o arquivo CSV para um DataFrame, apenas com as colunas desejadas
        df = pd.read_csv(caminho_arquivo, usecols=colunas_desejadas)

        df['Odometer (mi)'] = df['Odometer (mi)'].str.replace(',', '').astype(float)

        df = df.rename(columns={'Condition': 'Grade'})

        #convertendo em inteiro
        df['Odometer (mi)'] = pd.to_numeric(df['Odometer (mi)'], errors='coerce')
        df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')
        df['Price (USD)'] = df['Price (USD)'].str.replace('$', '')
        df['Price (USD)'] = pd.to_numeric(df['Price (USD)'], errors='coerce')


        #filtra o Odometro
        filtered_df = df[(df['Odometer (mi)'] >= ODO - 10000) & 
            (df['Odometer (mi)'] <= ODO + 10000) & 
            (df['Grade'] >= opcao_selecionada - 0.5) & 
            (df['Grade'] <= opcao_selecionada + 0.5)]


        num_linhas_filtradas = filtered_df.shape[0]

        soma_price = filtered_df['Price (USD)'].sum()

        PrecoSugerido = soma_price / num_linhas_filtradas

        
        # Configurando o local para formato de moeda USD
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        valor_formatado = locale.currency(PrecoSugerido, grouping=True)

    else:
        print('Nenhum arquivo CSV encontrado na pasta Downloads.')

    
    col3.subheader(f'{ModelCarro}')

    if valor_formatado != "$nan":

        col3.markdown(f'#### Suggested Purchase Value  {valor_formatado}')
    else:

        col3.markdown(f'#### Suggested Purchase Value  {TAdjustedMMR}')
        

    #col3.write(valor_formatado)
    col3.write('(based on the average of the last cars sold at Manheim, considering mileage and vehicle grade)')

    col3.markdown(f'#### CarGurus Instant Market Value™ {TValueGurus}')

    #col3.text(f'Suggested Purchase Value {valor_formatado} /n (based on the average of the last cars sold at Manheim, considering mileage and vehicle grade)')

    col3.text(f' Odometro = {ODO}')

    col3.text(f' Adjusted MMR = {TAdjustedMMR}')
  
    col3.text(f' MMR Range = {TMMRRange}')
    
    col3.text(f' Estimated Retail Value = {TEstimatedRetailValue}')
   
    col3.text(f' TipicalRange = {TTypicalRange1} - {TTypicalRange2}')

    col3.text(f' Auto Check Score = {TAutoCheckScore} - \n{TAutoCheckScoreComparation}')
  
    col3.text(f' Major State Title Brand Check = {TMajorStateTitleBrandCheck}')

    col3.text(f' Accident Check = {TAcidenteCheck}')

    col3.text(f' Damage Check = {TDamageCheck}')

    with col3:

        st.dataframe(filtered_df)
        #st.dataframe(df)


    navegador.quit()
    