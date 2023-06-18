# BDII-proyecto2
## ***Integrantes:***
- Mauricio Alvarez
- Aaron Santamaria
- Rodo Vilcarromero
- Ronaldo Flores

## ***Introducción:***
Para el presente proyecto usamos las librerías NLTK importando tokenize, corpus para los stopwords y stem snowball, sklearn importando TfidVectorizer, CountVectorizer, cosine y similarity, y PyQt6 (QtCore, QtGui y QtWidgets) para la interfaz, usando algoritmos de busqueda y recuperación de la información.
![Imagen de WhatsApp 2023-06-16 a las 17 19 08](https://github.com/mauricio-alvarez/BDII-proyecto2/assets/85258014/45be809c-fc34-4764-9462-2a1e2256164b)

## ***Desarrollo del proyecto:***

- GUI (Mauricio)


- Proyecto2.sql
Presenta el código para poder levantar la base de datos con las tablas “articles” , “versions” y “authors_parsed”.
- dictDocs.txt
Contiene un diccionario que asocia el id de documento con la posición en el archivo
- dictWord.txt
Contiene un diccionario que asocia cada keyword con su id y cuantas veces se repite en el documento
-main.py
Contiene la clase SPIMI, con la siguiente estructura:
init: llama a loadStopList.
saveDict: Tras crear el indice en memoria secundaria, se guarda el diccionario de palabras y documentos en memoria. Esta función sólo se ejecuta antes de crear el índice invertido.
. loadDict: 
Para realizar consultas, necesitamos cargar los diccionarios de palabras y documentos en memoria principal.
. loadStopList: 
Se escogio una lista standar de terminos muy repetidos del ingles para filtrar los docuemntos
. indexNewDocuments:
Para indexar el archivo de artículos se procesa uno a la vez. Aplicamos el preprocesamiento para extraer solo las palabras relevantes y raiz. Cada palabra nueva se le asigna un id y el numero de documentos en los que aparece, luego se crea un archivo en memoria secundaria que contendra el indice para la palabra. Si la palabra ya estaba indexada se agrega al indice, y se abre el archivo asociado a la palabra y se agrega el nuevo documento.
Cada documento se mapea en un diccionario. Para acceder facilmente el registro .
- postgresIndex.py
Contiene la clase Postgre:
. connectToDB: conecta la base de datos.
. loadData:
Procesamos los articulos uno a la vez para rellenar cada registro en las tablas de la base de datos. 
. createIndex:
Esta funcion recibe una lista con los elementos de los articulos que queremos indexar. Ya que solo estamos indexando el titulo y el abstract, solo recibe esos paramentros. En postgresql se asigna relevancia con las letras A,B,C,D entonces para los 4 primeros elementos de la lista se asigna una letra.
Posteriorme se crea un columna tsvector y se llena con los datos del title y abstract, vease que se puso con mas importante al titulo.
. process_text:
La funcion to_tsquery de postgresql recibe como parametro una consulta preprocesada donde cada keyword se debe separar por un operador booleano, entonces se identifica algunos terminos del ingles asociados a algunos operadores y se los reemplaza en la query consultQuery: Forzamos la busqueda con el indice de los top-k resultados los cuales almacenamos en una lista que se mostrara en la GUI
	
- recoveryData.py
De acuerdo a la consulta procesada se identifican los keywords los cuales se buscan en el diccionario de palabras para asociarlos con su id y recuperar el índice en memoria secundaria. 
- stoplist-en.txt
Documento con los   
- part1.json
Muestra para el proyecto con un tamaño de 1 millon de datos
