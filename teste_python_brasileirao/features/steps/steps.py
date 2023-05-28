from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

# Autor: Francisco Jarmison De Sousa Paiva
# Matricula: 20221113414
# Teste De Software

@given('Eu acesso o site do Globo Esporte')
def step_acesso_site_globo_esporte(context):
    context.driver = driver
    context.driver.get('https://ge.globo.com/')
    context.driver.implicitly_wait(10)

@when('Eu navego para a página do Brasileirão')
def step_navegar_pagina_brasileirao(context):
    menu = WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-produto"]/div[2]/div/div/div[1]/div')))
    menu.click()
    menu = WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav/div/div[1]/ul/li[1]/a')))
    menu.click()

@then('Eu capturo o nome do primeiro time na tabela e salvo em um arquivo')
def step_capturar_primeiro_time(context):
    tabela = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/main/div[2]/div/section[1]/article/section[1]/div/table[1]/tbody/tr[1]')))
    primeiro_time = tabela.text.strip()

    with open('../../primeiro_time.txt', 'w') as arquivo:
        arquivo.write(primeiro_time)