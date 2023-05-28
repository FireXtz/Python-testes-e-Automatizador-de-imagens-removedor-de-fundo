# Autor: Francisco Jarmison De Sousa Paiva
# Matricula: 20221113414
# Teste de Software

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

url = 'https://ge.globo.com/'

try:
    driver.get(url)
    driver.implicitly_wait(10)
except:
    driver.quit()
    quit()

try:
    menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-produto"]/div[2]/div/div/div[1]/div')))
    menu.click()
except:
    driver.quit()
    quit()

try:
    menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav/div/div[1]/ul/li[1]/a')))
    menu.click()
except:
    driver.quit()
    quit()

try:
    tabela = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/main/div[2]/div/section[1]/article/section[1]/div/table[1]/tbody/tr[1]')))
    primeiro_time = tabela.text.strip()

    with open('primeiro_time.txt', 'w') as arquivo:
        arquivo.write(primeiro_time)

except:
    driver.quit()
    quit()

driver.quit()