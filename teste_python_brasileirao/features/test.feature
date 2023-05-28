Feature: Testes de automação do site Globo Esporte
# Autor: Francisco Jarmison De Sousa Paiva
# Matricula: 20221113414
# Teste De Software
Scenario: Capturar o nome do primeiro time na tabela do Brasileirão
    Given Eu acesso o site do Globo Esporte
    When Eu navego para a página do Brasileirão
    Then Eu capturo o nome do primeiro time na tabela e salvo em um arquivo