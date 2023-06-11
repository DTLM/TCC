import random
import cv2
import os
from pathlib import Path

# CAMINHOS -------------------------------------------------------------------------------------------------------------------
absPath = os.getcwd()
baseFolder = "Dados"

# base onde se encontram as imagens
folderGrupos = "\\Dados\\train grupos"
folderTrain = "\\Dados\\train diseases"
folderTestGrupos = "\\Dados\\test grupos"
folderTestDiseases = "\\Dados\\test diseases"

folderNoiseFilter = "noise filter"
folderPeperFilter = "peper filter"
folderFiltroDuplo = "filtro duplo"

#estrutura interna de arquivos para teste e treinamento
folderTreinoDoenca = "treino doencas"
folderTreinoGrupo = "treino grupo"
folderTesteDoenca = "teste doencas"
folderTesteGrupo = "teste grupo"

# FILTROS ------------------------------------------------------------------------------------------------------------------------

# salt-and-pepper noise can
# be applied only to grayscale images
# Reading the color image in grayscale image
# code from: https://www.geeksforgeeks.org/add-a-salt-and-pepper-noise-to-an-image-with-python/
def add_noise(img):
        # Getting the dimensions of the image
        row , col = img.shape
        
        # Randomly pick some pixels in the
        # image for coloring them white
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300, 10000)
        for i in range(number_of_pixels):
            
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to white
            img[y_coord][x_coord] = 255
            
        # Randomly pick some pixels in
        # the image for coloring them black
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300 , 10000)
        for i in range(number_of_pixels):
            
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to black
            img[y_coord][x_coord] = 0

        return img
  

def noiseFactory(destino, img):
    if(os.path.exists(img)):
        image = cv2.imread(img)

        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
        bg=cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
        out_gray=cv2.divide(image, bg, scale=255)
        out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 

        cv2.imwrite(destino,out_binary)
        cv2.imwrite(destino,out_gray)

    else:
        print("caminho não existe.")

def noiseFactoryDoubleFilter(destino, img):
        
        image = img
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
        bg=cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
        out_gray=cv2.divide(image, bg, scale=255)
        out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 

        cv2.imwrite(destino,out_binary)
        cv2.imwrite(destino,out_gray)

        return destino
    
#DIRETORIOS ---------------------------------------------------------------------------------------------------------------------

def criarDiretoriosBase(caminho, destino):
     # diretorios padrões, ignorar as imagens dentro
     for filename in os.listdir(absPath + caminho):
        # aqui tem as pastas de doenças dentro da pasta principal
        path = destino + "\\" + filename
        if os.path.isdir(path) == False:
            os.makedirs(path, exist_ok = True)
        else:
            print("dir já existe")

def criarDiretorios():
    #peper
    #para treino
    #criarDiretoriosBase(folderGrupos, absPath +"\\"+ baseFolder + "\\" + folderPeperFilter + "\\" + folderTreinoGrupo)
    #para teste
    #criarDiretoriosBase(folderTestGrupos, absPath +"\\"+ baseFolder + "\\" + folderPeperFilter + "\\" + folderTesteGrupo)
    # para treino não grupo
    criarDiretoriosBase(folderTrain, absPath +"\\"+ baseFolder + "\\" + folderPeperFilter + "\\" + folderTesteDoenca)
    #doenças não grupo
    criarDiretoriosBase(folderTestDiseases, absPath +"\\"+ baseFolder + "\\" + folderPeperFilter + "\\" + folderTreinoDoenca)

# CHAMADA DE FILTROS --------------------------------------------------------------------------------------------------

# caminho tem que ter Dados\ treino ou teste de grupo e doenças (fonte)
# destino tem que ter Dados\ nome filtro\ tipo do treino ou teste
def copiarPorPathNoiseFilter(caminho, destino):
    # exemplo folder train grupos
    if os.path.isdir(absPath + caminho):
        for filename in os.listdir(absPath + caminho):
            path = ""
            path = absPath + caminho + "\\" + filename
            # verifica se os arquivos de grupo existem
            if os.path.isdir(path):
                # verifica se dentro do noise filter tem um treino grupo
                if os.path.isdir(destino):
                    for fileDestino in os.listdir(destino):
                        if(fileDestino == filename):
                            pathDestino = ""
                            pathDestino = destino + "\\" + fileDestino
                            # pegando as imagens
                            for img in os.listdir(path):
                                pathImg = ""
                                pathImg = path + "\\" + img
                                pathDestinoAux = pathDestino  + "\\" + img
                                if(os.path.exists(pathImg)):
                                    noiseFactory(pathDestinoAux, pathImg)
                                else:
                                    print("Não existe")
                else:
                    print("destino não existe")
                    break

            else:
                print("dir não encontrado")

def copiarPorPathPeperFilter(caminho, destino):
    # exemplo folder train grupos
    if os.path.isdir(absPath + caminho):
        for filename in os.listdir(absPath + caminho):
            path = ""
            path = absPath + caminho + "\\" + filename
            # verifica se os arquivos de grupo existem
            if os.path.isdir(path):
                # verifica se dentro do noise filter tem um treino grupo
                if os.path.isdir(destino):
                    for fileDestino in os.listdir(destino):
                        if(fileDestino == filename):
                            pathDestino = ""
                            pathDestino = destino + "\\" + fileDestino
                            # pegando as imagens
                            for img in os.listdir(path):
                                pathImg = ""
                                pathImg = path + "\\" + img
                                pathDestinoAux = pathDestino  + "\\" + img
                                if(os.path.exists(pathImg)):
                                    imagem = cv2.imread(pathImg, cv2.IMREAD_GRAYSCALE)
                                    cv2.imwrite(pathDestinoAux , add_noise(imagem))
                                else:
                                    print("Não existe")
                else:
                    print("destino não existe")
                    break

            else:
                print("dir não encontrado")

def copiarPorPathDoublerFilter(caminho, destino):
    # exemplo folder train grupos
    if os.path.isdir(absPath + caminho):
        for filename in os.listdir(absPath + caminho):
            path = ""
            path = absPath + caminho + "\\" + filename
            # verifica se os arquivos de grupo existem
            if os.path.isdir(path):
                # verifica se dentro do noise filter tem um treino grupo
                if os.path.isdir(destino):
                    for fileDestino in os.listdir(destino):
                        if(fileDestino == filename):
                            pathDestino = ""
                            pathDestino = destino + "\\" + fileDestino
                            # pegando as imagens
                            for img in os.listdir(path):
                                pathImg = ""
                                pathImg = path + "\\" + img
                                pathDestinoAux = pathDestino  + "\\" + img
                                if(os.path.exists(pathImg)):
                                    imagemAux = cv2.imread(pathImg)
                                    imagemPath = noiseFactoryDoubleFilter(pathDestinoAux, imagemAux)
                                    imagem = cv2.imread(imagemPath, cv2.IMREAD_GRAYSCALE)
                                    os.remove(imagemPath)
                                    cv2.imwrite(imagemPath , add_noise(imagem))
                                    
                                else:
                                    print("Não existe")
                else:
                    print("destino não existe")
                    break

            else:
                print("dir não encontrado")



def prepareAmbiente():
    criarDiretorios()

    # dentro do diretorio tem arquivos dos 4 grupos e dentro desses grupos tem as imagens
    copiarPorPathPeperFilter(folderGrupos, absPath + "\\" + baseFolder + "\\" +"peper filter" + "\\" + folderTreinoGrupo)
    copiarPorPathPeperFilter(folderTrain, absPath + "\\" + baseFolder + "\\" +"peper filter" + "\\" + folderTreinoDoenca)
    copiarPorPathPeperFilter(folderTestGrupos, absPath + "\\" + baseFolder + "\\" +"peper filter" + "\\" + folderTesteGrupo)
    copiarPorPathPeperFilter(folderTestDiseases, absPath + "\\" + baseFolder + "\\" +"peper filter" + "\\" + folderTesteDoenca)
    

#prepareAmbiente()