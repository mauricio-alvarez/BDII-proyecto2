import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('punkt')
diccio_deindices = {}


# Desglozar la query
def recovery_data(query):
    result = {}
    stop_words = set(stopwords.words('english'))
    stop_words.discard('no')
    stop_words = [*stop_words]
    query_evaluate = [x for x in query if x not in stop_words]
    if len(query_evaluate) == 0:
        raise Exception('this query does not require any information')
    x = 0
    while x <= (len(query_evaluate)):
        if x != 'no':
            result[query_evaluate[x]] = True
            x = x + 1
        else:
            result[query_evaluate[x + 1]] = False
            x = x + 2
    # Retorna la query desenpaquetada
    return result


# Rescatar que documentos si y cuales no se mostraran
def serach_document(query_read):
    Yes_documents = []
    No_documents = []
    for key, value in query_read:
        if value:
            Yes_documents.append(diccio_deindices[key])
        else:
            No_documents.append(diccio_deindices[key])
    result = [x for x in Yes_documents if x not in No_documents]
    # devuelve que documentos debemos
    return result


# Sacar Tfidf de los documentos los cuales debemos mostrar
def sort_document(documents):
    tr_idf_model = TfidfVectorizer()
    tf_idf_vector = tr_idf_model.fit_transform(documents)
    return tf_idf_vector
