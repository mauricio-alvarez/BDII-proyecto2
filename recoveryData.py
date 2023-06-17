import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')
diccio_deindices = {}


# Desglozar la query
def recovery_data(query):
    result = {}
    query = query.split()
    stop_words = set(stopwords.words('english'))
    stop_words.discard('no')
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
def serach_document(query_read):
    Yes_documents = []
    No_documents = []
    for key, value in query_read.items():
        if value:
            Yes_documents.append(dictWords[key][0])
        else:
            No_documents.append(dictWords[key][0])
    result = [x for x in Yes_documents if x not in No_documents]
    # devuelve que documentos debemos
    return result


# Sacar Tfidf de los documentos los cuales debemos mostrar
def sort_document(indices, query):
    documents = []
    print(indices)
    print(indices)
    for x in indices:
        temp = dictDocs[x][1]
        file = open('part1.json', 'rb')
        file.seek(x + 1) if x != 0 else file.seek(x)
        contenido = str(file.readline().decode('utf-8'))
        documents.append(contenido)
    print(documents)
    model_fit = TfidfVectorizer()
    aux = TfidfVectorizer()
    model_fit.fit(documents)
    tf_idf_vector = aux.fit_transform(documents)
    tf_ = model_fit.transform([query])
    cosine_similary = cosine_similarity(tf_, tf_idf_vector)
    cosine_similary_final = []
    for i in range(len(indices)):
        cosine_similary_final.append((cosine_similary[i], indices[i]))
    sorted(cosine_similary_final, reverse=True)
    return cosine_similary_final
