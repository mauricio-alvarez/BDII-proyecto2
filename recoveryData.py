import json
from datetime import time
import time
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')


class Recovery:
    # Constructor de clase
    def __init__(self, query, dictWords, dictDocs):
        self.query = query
        self.dictWords = dictWords
        self.dictDocs = dictDocs

    # Desglozar la query
    def recovery_query(self):
        result = {}
        query = self.query.split()
        stop_words = set(stopwords.words('english'))
        stop_words.discard('no')
        stop_words.discard('don´t')
        stop_words.discard('doesn´t')
        stop_words.discard('didn´t')
        stop_words.discard('dont')
        stop_words = [*stop_words]
        exceptions = ['no', 'don´t', 'doesn´t', 'didn´t', 'dont']
        query_evaluate = [x for x in query if x not in stop_words]
        if len(query_evaluate) == 0:
            raise Exception('this query does not require any information')
        x = 0
        stemmer = SnowballStemmer("english")
        while x < (len(query_evaluate)):
            if query_evaluate[x] not in exceptions:
                result[stemmer.stem(query_evaluate[x])] = True
                x = x + 1
            else:
                result[stemmer.stem(query_evaluate[x + 1])] = False
                x = x + 2
        # Retorna la query desenpaquetada
        return result

    def getDocuments(self, pos):
        file = open('indexData/' + str(pos) + '.txt')
        text = file.read()
        result = text.split(',')
        return result[:-1]

    def search_document(self, query_read):
        Yes_documents = []
        No_documents = []
        for key, value in query_read.items():
            if value:
                try:
                    temp = self.getDocuments(self.dictWords[key][0])
                    Yes_documents += temp
                except:
                    continue
            else:
                try:
                    temp = self.getDocuments(self.dictWords[key][0])
                    No_documents += temp
                except:
                    continue
        result = [int(x) for x in Yes_documents if x not in No_documents]
        # devuelve que documentos debemos

        return list(set(result))

    # Sacar Tfidf de los documentos los cuales debemos mostrar
        def sort_document(self, indices, k):
        documents = []
        titles = []
        for x in indices:
            temp = self.dictDocs[str(x)][1]
            # arxiv-metadata-oai-snapshot.json
            file = open('arxiv-metadata-oai-snapshot.json', 'rb')
            file.seek(temp + 2) if temp != 0 else file.seek(temp)
            contenido = file.readline().decode('utf-8')
            contenido = contenido.replace('\n', ' ').replace('\\', ' ')
            contenido = self.tojson(contenido)
            
            try:
                titles.append(contenido["title"])
                documents.append(contenido['authors'] + contenido['title'] + ' ' + contenido['abstract'] + contenido['comments'])
            except:
                print("Error tipo 1 ")
                pass


        model_fit = TfidfVectorizer()
        tf_idf_vector = model_fit.fit_transform(documents)
        tf_ = model_fit.transform([self.query])
        cosine_similary = cosine_similarity(tf_idf_vector, tf_)
        cosine_similary_final = []
        cosine_similary_temp = []
        for i in range(len(titles)):
            cosine_similary_temp.append((cosine_similary[i][0], titles[i]))
        cosine_similary_temp.sort(key=lambda x: x[0], reverse=True)
        for i in range(int(k)):
            try:
                cosine_similary_final.append(cosine_similary_temp[i])
            except:

                break
        return cosine_similary_final
    def tojson(self, contenido):
        keysToFind = {
            0: ("id", 5), 1: ("submitter", 12), 2: ("authors", 10),3: ("title", 8),
            4: ("comments", 11),5: ("journal-ref", 14),6: ("doi", 6),7: ("report-no", 12),
            8: ("categories", 13),9: ("license", 10),
            10: ("abstract", 11),11: ("versions", 11),
            12: ("update_date", 14),13: ("authors_parsed", 17)
        }
        patrones = [
            '"authors":', '"title":', '"comments":',
            '"journal-ref":','"abstract":', '"versions":']
        newDict = dict()
        expresion_regular = "|".join(patrones)
        coincidencias = re.finditer(expresion_regular, contenido)
        posiciones = [coincidencia.start() for coincidencia in coincidencias]
        if (len(patrones) == len(posiciones)):
            #Agregar authors
            newDict['authors'] = contenido[posiciones[0] + keysToFind[0][1]:posiciones[1] - 2]
            #Agregar title
            newDict['title'] = contenido[posiciones[1] + keysToFind[1][1]:posiciones[2] - 2]
            #Agregar comments
            newDict['comments'] = contenido[posiciones[2] + keysToFind[2][1]:posiciones[3] - 2]
            #Agregar abstract
            newDict['abstract'] = contenido[posiciones[4] + keysToFind[4][1]:posiciones[5] - 2]
        else:
            print(posiciones)
            try:return json.load(contenido)
            except:
                print("Some error 2 Uppss!!!")
                newDict['authors'] = ""
                newDict['title'] = ""
                newDict['comments'] = ""
                newDict['abstract'] = ""
        return newDict
        
    def Recovery_data(self, k):
        start = time.time()
        temp = self.recovery_query()
        aux = self.search_document(temp)
        result = self.sort_document(aux, k)
        end = time.time()
        return result, end - start
