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
nltk.download('punkt')

class Spimi():
    def __init__(self):
        self.dictDoc = self.dictWord = self.stoplist = {}
        self.stoplist = self.loadStopList("stoplist-en.txt")

    def saveDict(self, diccionario, nombre_archivo, formato):
        try:
            if formato == "texto":
                with open(nombre_archivo, 'w') as f:
                    json.dump(diccionario, f)
            elif formato == "binario":
                with open(nombre_archivo, 'wb') as f:
                    json.dump(diccionario, f)
            else:
                print("Formato no válido. Debe ser 'texto' o 'binario'.")
                return

            print("Diccionario guardado exitosamente en el archivo:", nombre_archivo, "len: ", len(diccionario))
        except IOError:
            print("Error al guardar el diccionario en el archivo:", nombre_archivo)

    def loadDict(self, nombre_archivo, formato):
        try:
            if formato == "texto":
                with open(nombre_archivo, 'r') as f:
                    diccionario = json.load(f)
            elif formato == "binario":
                with open(nombre_archivo, 'rb') as f:
                    diccionario = json.load(f)
            else:
                print("Formato no válido. Debe ser 'texto' o 'binario'.")
                return None
            print("Diccionario cargado exitosamente desde el archivo:", nombre_archivo)
            return diccionario
        except IOError:
            print("Error al cargar el diccionario desde el archivo:", nombre_archivo)
            return None

    def loadStopList(self, archivo):
        stoplist = dict()
        with open(archivo, "r", encoding="utf-8") as file:
            for palabra in file:
                palabra = palabra.strip()  # Eliminar espacios en blanco y saltos de línea adicionales
                stoplist[palabra] = True
        return stoplist

    def preProcessing(self, texto):
        # Tokenizar
        texto = ' '.join(texto)
        list = nltk.word_tokenize(texto.lower())

        stemmer = SnowballStemmer("english")
        result = []
        # Filtrar stopwords
        for x in list:
            if (x not in self.stoplist and len(x) > 3):
                try:
                    float(stemmer.stem(x))
                    pass
                except ValueError:
                    result.append(stemmer.stem(x))

        return result

    def getFrecuency(self, lista):
        conteo = {}
        for palabra in lista:
            if palabra in conteo:
                conteo[palabra] += 1
            else:
                conteo[palabra] = 1
        return conteo

    def indexNewDocuments(self, file):
        with open(file, 'r', encoding="utf-8") as file:
            errores = 0
            terminosProcesados = 0
            position = 0
            for counter, line in enumerate(file):
                article = json.loads(line)
                # print("Pos: ", posicion)
                inicio = time.time()
                keyWord = self.preProcessing([article['title'], article['abstract']])
                # dictDoc[article['id']] = len(dictDoc)+1

                self.dictDoc[len(self.dictDoc) + 1] = (article['id'], position)
                frecuencias = self.getFrecuency(keyWord)
                terminosProcesados += len(keyWord)
                ite = set(keyWord)
                # Guardar cada Keyword en el memoria secundaria
                for word in list(ite):
                    if (word in self.dictWord):
                        # La palabra ya existe en el diccionario
                        # Se actualiza la frecuencia de documento
                        current = self.dictWord[word]
                        self.dictWord[word] = (current[0], (current[1] + 1))
                        nameFile = "indexData/" + str(current[0]) + ".txt"
                        try:
                            indexFile = open(nameFile, "a")
                            indexFile.write(str(len(self.dictDoc)) + ",")
                            indexFile.close()
                        except IOError:
                            errores += 1
                            print("Error al abrir el archivo:", nameFile)
                    else:
                        # La palabra es nueva en el diciconario
                        # Se anade un nuevo valor al diccionario
                        self.dictWord[word] = (len(self.dictWord) + 1, 1)
                        nameFile = "indexData/" + str(len(self.dictWord)) + ".txt"
                        try:
                            indexFile = open(nameFile, "w")
                            indexFile.write(str(len(self.dictDoc)) + ",")
                            indexFile.close()
                        except IOError:
                            errores += 1
                            print("Error al crear el archivo:", nameFile)
                tiempo_ejecucion = time.time() - inicio
                # print(f"Se ha cargado: '{article['id']}, correctamente en {tiempo_ejecucion:.6f} segundos. #{counter}")
                position += len(line)
                # print("Pos: ", position)
                if (counter == 1000000):
                    print("Se termino de procesar")
                    break

        print(f"Se ha procesado: {terminosProcesados} palabras durante esta indexacion.")
        print(f"Durante la ejecuccion se anoto: {errores} errores.")
'''
dictWords = {}
dictDocs = {}
saveDict(dictWords, "dictWord.txt", "texto")
saveDict(dictDocs, "dictDocs.txt", "texto")

dictWords = loadDict("dictWord.txt", "texto")
dictDocs = loadDict("dictDocs.txt", "texto")

indexNewDocuments('part1.json', dictDocs, dictWords)
saveDict(dictWords, "dictWord.txt", "texto")
saveDict(dictDocs, "dictDocs.txt", "texto")
'''
# test("part1.json")
