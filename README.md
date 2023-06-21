# BDII-proyecto2
## ***Integrantes:***
- Mauricio Alvarez
- Aaron Santamaria
- Rodo Vilcarromero
- Ronaldo Flores

-[Video de presentación:](https://drive.google.com/drive/folders/1BHmU0a5xmGE4y1shGJd6BG4lsvnW6ZKw)

## ***Introducción:***
Para el presente proyecto usamos las librerías NLTK importando tokenize, corpus para los stopwords y stem snowball, sklearn importando TfidVectorizer, CountVectorizer, cosine y similarity, y PyQt6 (QtCore, QtGui y QtWidgets) para la interfaz, usando algoritmos de busqueda y recuperación de la información.


## ***Dominio de datos:***
La base de datos usada en este proyecto consiste de registros de publicaciones académicas por parte de la universidad de Cornell, donde encontramos campos como autores, títulos de artículos, categorías, abstracts y id's para poder ubicarlos en la página de la universidad.

## **GUI** (Frontend)
![Imagen de WhatsApp 2023-06-16 a las 17 19 08](https://github.com/mauricio-alvarez/BDII-proyecto2/assets/85258014/45be809c-fc34-4764-9462-2a1e2256164b)
![Captura de pantalla 2023-06-18 225646](https://github.com/mauricio-alvarez/BDII-proyecto2/assets/85258014/37e33140-9159-46e2-af76-f318ded6be89)
![Captura de pantalla 2023-06-18 225714](https://github.com/mauricio-alvarez/BDII-proyecto2/assets/85258014/4ecfb397-0901-4a48-8b21-fb9872c7c743)
![Imagen de WhatsApp 2023-06-18 a las 23 17 43](https://github.com/mauricio-alvarez/BDII-proyecto2/assets/85258014/1be1fc8e-0a01-4746-bcc8-b6ed1bb24060)

## ***Dominio de datos:*** (Backend)
- **Proyecto2.sql**
Presenta el código para poder levantar la base de datos con las tablas “articles” , “versions” y “authors_parsed”.
- **dictDocs.txt**
Contiene un diccionario que asocia el id de documento con la posición en el archivo
- **dictWord.txt**
Contiene un diccionario que asocia cada keyword con su id y cuantas veces se repite en el documento
- **main.py**
Contiene la clase SPIMI, con la siguiente estructura:
    - init: llama a loadStopList.
    - saveDict: Tras crear el indice en memoria secundaria, se guarda el diccionario de palabras y documentos en memoria. Esta función sólo se ejecuta antes de crear el índice invertido.
    - loadDict: Para realizar consultas, necesitamos cargar los diccionarios de palabras y documentos en memoria principal.
    - loadStopList: Se escogio una lista standar de terminos muy repetidos del ingles para filtrar los docuemntos.
    - indexNewDocuments:
Para indexar el archivo de artículos se procesa uno a la vez. Aplicamos el preprocesamiento para extraer solo las palabras relevantes y raiz. Cada palabra nueva se le asigna un id y el numero de documentos en los que aparece, luego se crea un archivo en memoria secundaria que contendra el indice para la palabra. Si la palabra ya estaba indexada se agrega al indice, y se abre el archivo asociado a la palabra y se agrega el nuevo documento.
Cada documento se mapea en un diccionario. Para acceder facilmente el registro .

- **postgresIndex.py**
Contiene la clase Postgre:
    - connectToDB: conecta la base de datos.
    - loadData: Procesamos los articulos uno a la vez para rellenar cada registro en las tablas de la base de datos. 
    - createIndex:
Esta funcion recibe una lista con los elementos de los articulos que queremos indexar. Ya que solo estamos indexando el titulo y el abstract, solo recibe esos paramentros. En postgresql se asigna relevancia con las letras A,B,C,D entonces para los 4 primeros elementos de la lista se asigna una letra.
Posteriorme se crea un columna tsvector y se llena con los datos del title y abstract, vease que se puso con mas importante al titulo.
    - process_text:
La funcion to_tsquery de postgresql recibe como parametro una consulta preprocesada donde cada keyword se debe separar por un operador booleano, entonces se identifica algunos terminos del ingles asociados a algunos operadores y se los reemplaza en la query consultQuery: Forzamos la busqueda con el indice de los top-k resultados los cuales almacenamos en una lista que se mostrara en la GUI.
	
- **recoveryData.py**
    - recovery_query: Desglozamos la query para agregarlo a una lista, creamos los stopwords(lista) en query y agregamos  el 'no', 'don´t', 'doesn´t', 'didn´t', 'dont', filtramos por si la  query no es valida, si no es una negacion( lo que agregamos al stopword) lo va a agregar como un true, caso contrario lo agregará como false el query que le sigue al exceptions.

    - serach_document:
Un for en la query desempaquetada, si el valor es verdadero en la palabra, obtendremos todos los documentos de aquella y lo agregamos a Yes_documents, caso contrario lo añadimos en No_documents. y retornamos una diferencia de conjuntos entre Yes_document y No_document.

    - sort_document: 
Itera sobre la lista de indices, abrimos el archivo y luego movemos el puntero en la posicion de bits correspondiente, despues añadimos a documents, posteriormente convertimos el json en un diccionario, para finalizar en titles agregamos el titulo.
Creamos una variable a un vector luego sacamos el tfidf a los documentos, luego sacamos el tfidf de la query, termiando sacando la similitud de coseno entre ellos.
Un ultimo for para el topk con el coseno de similitud con título
    - recoveryDara:Llamamos a todo.
- **stoplist-en.txt**
Documento con los stopwords.

- **Archivos generados por el desarrollo del backend:**
[Descargar archivos](https://drive.google.com/drive/folders/1a20unbmjfS_bZHMhosFUuWpFwGwLTRIz)
