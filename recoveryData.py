import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import main

nltk.download('stopwords')
nltk.download('punkt')


class Recovery:
    # Constructor de clase
    def __init__(self, query):
        self.query = query

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
        query_evaluate = [x for x in query if x not in stop_words]
        if len(query_evaluate) == 0:
            raise Exception('this query does not require any information')
        x = 0
        stemmer = SnowballStemmer("english")
        while x < (len(query_evaluate)):
            if query_evaluate[x] != 'no':

                result[stemmer.stem(query_evaluate[x])] = True
                x = x + 1
            else:
                result[stemmer.stem(query_evaluate[x + 1])] = False
                x = x + 2
        # Retorna la query desenpaquetada
        return result

    def getDocuments(self, pos):
        file = open('indexData/' + str(pos) + '.txt')
        text = file.readline()
        result = text.split(',')
        return result[:-1]

    def serach_document(self, query_read):
        Yes_documents = []
        No_documents = []
        for key, value in query_read.items():
            if value:
                try:
                    temp = self.getDocuments(main.dictWords[key][0])
                    Yes_documents += temp
                except:
                    continue
            else:
                try:
                    temp = self.getDocuments(main.dictWords[key][0])
                    No_documents += temp
                except:
                    continue
        result = [int(x) for x in Yes_documents if x not in No_documents]
        # devuelve que documentos debemos

        return result

    # Sacar Tfidf de los documentos los cuales debemos mostrar
    def sort_document(self, indices):
        documents = []
        jsonpos = []
        for x in indices:
            temp = main.dictDocs[str(x)][1]
            jsonpos.append(temp)
            file = open('part1.json', 'rb')
            file.seek(temp + 1) if x != 0 else file.seek(temp)
            contenido = str(file.readline().decode('utf-8'))
            documents.append(contenido)
        model_fit = TfidfVectorizer()
        tf_idf_vector = model_fit.fit_transform(documents)
        tf_ = model_fit.transform([self.query])
        cosine_similary = cosine_similarity(tf_idf_vector, tf_)
        cosine_similary_final = []
        for i in range(len(indices)):
            cosine_similary_final.append((cosine_similary[i][0], jsonpos[i]))
        cosine_similary_final.sort(key=lambda x: x[0], reverse=True)
        return cosine_similary_final

    def Recovery_data(self):
        temp = self.recovery_query()
        aux = self.serach_document(temp)
        result = self.sort_document(aux)
        return result
