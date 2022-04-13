from PIL import ImageChops, Image
import math, operator
from functools import *
import shutil
import os
from os import mkdir

# Directorio de las imagenes
path = os.path.expanduser(r"___________") 

carpeta_1 = os.path.join(path,"folder_1")
carpeta_2 = os.path.join(path, "folder_2")
try:
    carpeta_result=mkdir(os.path.join(path, "Resultados")) # Crea una carpeta de resultados
except FileExistsError:
    carpeta_result=os.path.join(path, "Resultados")


# ------------------------
# Root-mean-square --> Compara las imagenes
# ------------------------
def diff(img_1,img_2):
    # Calcula el histograma de la resta de las imgs
    h= ImageChops.difference(img_1,img_2).histogram()
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(img_1.size[0]) * img_1.size[1]))

# Devuelve el nombre del archivo
def path_file(path):
    head, tail = os.path.split(path)
    return tail

# ------------------------
# Iterar archivos de las carpetas
# ------------------------
lista_1=[]
lista_2=[]
lista_iguales_2 =[]
try:
    for filenames_1 in os.listdir(carpeta_1):
        file_1 = os.path.join(carpeta_1,filenames_1)
        img_1 = Image.open(file_1)
        lista_1.append(path_file(file_1))
         
    for filenames_2 in os.listdir(carpeta_2):
        file_2 = os.path.join(carpeta_2,filenames_2)
        img_2 = Image.open(file_2)
        lista_2.append(path_file(file_2))
        for filenames_1 in os.listdir(carpeta_1):
            file_1 = os.path.join(carpeta_1,filenames_1)
            img_1 = Image.open(file_1)

            resultado= diff(img_1,img_2)
            if resultado < 10: 
                lista_iguales_2.append(path_file(file_2))
# ------------------------
# Copiar archivos a resultados
# ------------------------
    copiar_lista_2 = list (set(lista_2)-set(lista_iguales_2))
        
    for files in lista_1:
        file = os.path.join(carpeta_1, files)
        try:
            shutil.copy(file,carpeta_result)
        except TypeError:
            carpeta_result=os.path.join(path, "Resultados")
            shutil.copy(file,carpeta_result)
    for files in copiar_lista_2:
        file = os.path.join(carpeta_2, files)
        try:
            shutil.copy(file,carpeta_result)
        except TypeError:
            carpeta_result=os.path.join(path, "Resultados")
            shutil.copy(file,carpeta_result)
    print ("---------Finalizado---------")

except IOError:
    print ("ERROR: no se encuentra alguno de los directorios.")
