import random
import string
import time
import sys
import pickle
import json
import nltk
import struct
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *

def saveDict(diccionario, nombre_archivo, formato):
    try:
        if formato == "texto":
            with open(nombre_archivo, "w") as archivo:
                for clave, valor in diccionario.items():
                    linea = f"{clave}: {valor}\n"
                    archivo.write(linea)
        elif formato == "binario":
            with open(nombre_archivo, "wb") as archivo:
                pickle.dump(diccionario, archivo)
        else:
            print("Formato no válido. Debe ser 'texto' o 'binario'.")
            return

        print("Diccionario guardado exitosamente en el archivo:", nombre_archivo)
    except IOError:
        print("Error al guardar el diccionario en el archivo:", nombre_archivo)
def loadDict(nombre_archivo, formato):
    try:
        if formato == "texto":
            with open(nombre_archivo, "r") as archivo:
                diccionario = {}
                for linea in archivo:
                    clave, valor = linea.strip().split(":")
                    diccionario[clave.strip()] = valor.strip()
        elif formato == "binario":
            with open(nombre_archivo, "rb") as archivo:
                diccionario = pickle.load(archivo)
        else:
            print("Formato no válido. Debe ser 'texto' o 'binario'.")
            return None

        print("Diccionario cargado exitosamente desde el archivo:", nombre_archivo)
        return diccionario
    except IOError:
        print("Error al cargar el diccionario desde el archivo:", nombre_archivo)
        return None
def preProcessing(texto):
    #Tokenizar
    texto = ' '.join(texto)
    list = nltk.word_tokenize(texto.lower())

    #Filtrar stopwords
    with open("stoplist-en.txt", "r", encoding="utf-8") as file:
        stoplist = [line.rstrip() for line in file.readlines()]
    signos = [".", ",", ";", ":", "(", ")", "=", "@", "+", "-", "_", "*", "¿", "?", "/", "&", "%", "!"]
    list = [x for x in list if x not in stoplist]
    list = [x for x in list if x not in signos]

    #Reducir palabras
    stemmer = SnowballStemmer("english")
    list = [stemmer.stem(palabra) for palabra in list]

    return list

def indexNewDocuments(file, dictDoc, dictWord):
    counter=0
    with open(file, 'r') as file:
        for line in file:
            article = json.loads(line)
            inicio = time.time()
            counter+=1
            keyWord = preProcessing(   [  article['title'],   article['abstract']   ]  )
            dictDoc[article['id']] = len(dictDoc)+1
            ite = set(keyWord)
            for word in list(ite):
                if(word in dictWord):
                    #La palabra ya existe en el diccionario
                    #Se actualiza la frecuencia de documento
                    current = dictWord[word]
                    dictWord[word] = (current[0], (current[1]++1))
                    nameFile = "indexData/" + str(current[0]) + ".txt"
                    try:

                        indexFile = open(nameFile, "a")
                        tf = sum(1 for item in keyWord if item == word)
                        data = struct.pack("II", len(dictDoc) + 1, tf)
                        indexFile.write(str(len(dictDoc) + 1) + " " + str(tf))
                        indexFile.close()
                    except IOError:
                        print("Error al abrir el archivo:", "indexData/"+str(current[0])+".txt")
                else:
                    #La palabra es nueva en el diciconario
                    #Se anade un nuevo valor al diccionario
                    dictWord[word] = (len(dictWord) + 1, 1)
                    nameFile = "indexData/" + str(len(dictWord) + 1) + ".txt"
                    try:

                        indexFile = open(nameFile, "w")
                        tf = sum(1 for item in keyWord if item == word)
                        data = struct.pack("II", len(dictDoc) + 1, tf)
                        indexFile.write(str(len(dictDoc) + 1) + " " + str(tf))
                        indexFile.close()
                    except IOError:
                        print("Error al crear el archivo:", nameFile)
            fin = time.time()
            tiempo_ejecucion = fin - inicio
            print(f"Se ha cargado: '{article['id']}, correctamente en {tiempo_ejecucion:.6f} segundos. #{counter}")

    file.close()


dictWords = {}
dictDocs = {}
saveDict(dictWords, "dictWord.txt", "texto")
saveDict(dictDocs, "dictDocs.txt","texto")

dictWords = loadDict("dictWord.txt","texto")
dictDocs = loadDict("dictDocs.txt","texto")


indexNewDocuments('arxiv-metadata-oai-snapshot.json',dictDocs, dictWords)
saveDict(dictWords, "dictWord.txt","texto")
saveDict(dictDocs, "dictDocs.txt","texto")