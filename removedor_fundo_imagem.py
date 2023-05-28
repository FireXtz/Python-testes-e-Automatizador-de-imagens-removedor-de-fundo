import numpy as np
import cv2 as cv
import requests
import os

# Autor: Francisco Jarmison De Sousa Paiva
# Matricula: 20221113414
# Programação Orientada a Objetos


# função utilizada para renomear os arquivos exemplo se for baixado 100 img sera
# renomeado de 001,002,003..... respectivamente por ordem de download caso for apagado sera retomado
# o valor anterior ou proximo
def rename_file(pasta_origem, pasta_destino):
    arquivos = os.listdir(pasta_origem)
    arquivos.sort()

    for i, a in enumerate(arquivos):

        nm = f"{str(i + 1).zfill(3)}.png"
        co = os.path.join(pasta_origem, a)
        cd = os.path.join(pasta_destino, nm)
        os.rename(co, cd)

        print(f"Imagem {a} renomeada e movida para {nm}")

# função que remove o fundo, ainda sim consegue deixar 60% da imagem transparente
# o algoritmo ainda esta bem incossistente pois foi feito na mão mesmo apenas utilizando
# algumas tecnicas de prossesamento de imagem.
def remove_background_img(urls_imagens, pasta_destino):
    for url in urls_imagens:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = cv.imdecode(np.frombuffer(response.content, np.uint8), cv.IMREAD_UNCHANGED)
            origin = img.copy()
            l = int(max(5, 6))
            u = int(min(6, 6))
            ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            edges = cv.GaussianBlur(img, (21, 51), 3)
            edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(edges, l, u)
            _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)
            mask = 255 - mask
            mask = np.array(mask, dtype=np.uint8)
            img_rgba = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
            gradient = np.tile(np.linspace(0, 255, img.shape[1]), (img.shape[0], 1)).astype(np.uint8)
            mask = cv.bitwise_and(mask, gradient)
            img_rgba[mask != 0] = (0, 0, 0, 0)
            nome_arquivo = url.split('/')[-1]
            caminho_destino = os.path.join(pasta_destino, nome_arquivo)
            caminho_destino_png = os.path.splitext(caminho_destino)[0] + '.png'
            cv.imwrite(caminho_destino_png, img_rgba)
            os.remove(caminho_destino)
            print(f"Imagem {nome_arquivo} processada e salva como PNG com fundo removido!")

        except Exception as e:
            print(f"Http response in... {url}: {str(e)}")

urls_imagens = [
    "https://images.pexels.com/photos/1592384/pexels-photo-1592384.jpeg",
    "https://img.freepik.com/fotos-gratis/foto-da-cintura-para-cima-de-uma-mulher-tenra-feminina-e-gentil-com-penteado-encaracolado-penteado-para-o-lado-direito-inclinando-a-cabeca-e-sorrindo-sedutor-tornando-o-olhar-romantico-para-a-camera-se-abracando-sobre-o-fundo-amarelo_1258-81987.jpg"
]

# aqui é onde é configurado as pastas de destinos
# a pasta temporaria é criada e logo apos salva o download nela
# apaga o arquivo salvo da pasta_temporaria e apos isso é feito uma copia da imagem ja processada
# assim consigo baixar o arquivo numa pasta temporaria e logo apos isso excluir ele para então enviar
# para imagens_processadas como um .png ja processado sem o fundo

pasta_destino = "imagens_processadas"
pasta_temporaria = "imagens_temporarias"

# caso não existir ele cria a pasta de destino
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# caso não existir ele cria a pasta temporaria
if not os.path.exists(pasta_temporaria):
    os.makedirs(pasta_temporaria)
# chamada do metodo remove_background_img e rename_file
remove_background_img(urls_imagens, pasta_temporaria)
rename_file(pasta_temporaria, pasta_destino)

# laço for iterando um listdir da pasta temporaria apos isso
# o caminho do arquivo é feito um join na pasta temporaria e passando como parametro o arquivo tambem
for arquivo in os.listdir(pasta_temporaria):
    caminho_arquivo = os.path.join(pasta_temporaria, arquivo)
    os.remove(caminho_arquivo)
os.rmdir(pasta_temporaria)
