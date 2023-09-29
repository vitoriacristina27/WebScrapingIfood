import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar opções do Chrome (opcional)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Execute em segundo plano (sem interface gráfica), se necessário
# chrome_options.add_argument("--disable-gpu")  # Desative a aceleração de hardware, se necessário

# Crie uma instância do driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

ifood_url = 'https://www.ifood.com.br/restaurantes'
driver.get(ifood_url)

time.sleep(10)
use_my_location_button = driver.find_element(By.XPATH, '//button[@class="btn-address--full-size"]')
use_my_location_button.click()
time.sleep(3)

# Role a página para baixo para carregar mais restaurantes
n_scrolls = 2  # Defina o número desejado de rolagens
for _ in range(n_scrolls):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(3)

# Clique no botão "Ver mais" algumas vezes (ajuste conforme necessário)
n_clicks_ver_mais = 2  # Defina o número desejado de cliques no botão "Ver mais"
for _ in range(n_clicks_ver_mais):
    ver_mais_button = driver.find_element(By.XPATH, '//button[@aria-label="Ver mais"]')
    ver_mais_button.click()
    time.sleep(10)  # Aguarde a página carregar completamente após clicar em "Ver mais"

# Encontre todos os elementos com a classe 'merchant-v2__content'
restaurant_elements = driver.find_elements(By.CLASS_NAME, 'merchant-v2__content')

restaurants = []

for element in restaurant_elements:
    # Coletar informações de cada restaurante
    info = element.text.split('\n')
    restaurant_name = info[0]
    restaurants.append(restaurant_name)

driver.quit()

# Crie um DataFrame com os dados dos restaurantes
df = pd.DataFrame({
    'Restaurante': restaurants,
})

# Salve os dados em um arquivo CSV
df.to_csv('dados-ifood.csv', index=False)
print(df)
