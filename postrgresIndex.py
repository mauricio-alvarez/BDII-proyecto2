import psycopg2
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import time
from nltk.corpus import stopwords
nltk.download('stopwords')


class Postgre():
    def __init__(self):
        # Configuración base de datos
        self.conn = self.cur = 0

    def connectToDB(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="articulos",
            user="postgres",
            password="1234"
        )
        self.cur = self.conn.cursor()
    
    def closeConnection(self):
        self.conn.close()
        self.cur.close()

    def loadData(self, file):
        self.connectToDB()
        n=0
        with open('arxiv-metadata-oai-snapshot.json', 'r') as f:
            for line in f:
                if n<1000000:
                    article = json.loads(line)
                    self.cur.execute(
                        """
                        INSERT INTO articles (id, submitter, authors, title, comments, journal_ref, doi, report_no, categories, license, abstract, update_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (article['id'], article['submitter'], article['authors'], article['title'], article['comments'],
                        article['journal-ref'], article['doi'], article['report-no'], article['categories'],
                        article['license'], article['abstract'], article['update_date'])
                    )
                    for version in article['versions']:
                        self.cur.execute(
                            """
                            INSERT INTO versions (article_id, version, created)
                            VALUES (%s, %s, %s)
                            """,
                            (article['id'], version['version'], version['created'])
                        )

                    for author in article['authors_parsed']:
                        self.cur.execute(
                            """
                            INSERT INTO authors_parsed (article_id, last_name, first_name, middle_name)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (article['id'], author[0], author[1], author[2])
                        )
                else:
                    break
                n+=1
            self.conn.commit()
            self.closeConnection()

    def createIndex(self, columns):
        self.connectToDB()
        if not columns or not isinstance(columns, list) or len(columns) > 12:
            raise ValueError("columns must be a list of 1 to 12 column names")

        weights = ['A', 'B', 'C', 'D']
        setweight_strs = []
        for i, col in enumerate(columns):
            weight = weights[i] if i < 4 else 'D'
            setweight_strs.append(f"setweight(to_tsvector('english', COALESCE({col},'')), '{weight}')")

        setweight_str = ' || '.join(setweight_strs)
        self.cur.execute(
            f"""
            ALTER TABLE articles ADD COLUMN weighted_tsv tsvector;

            UPDATE articles SET 
                weighted_tsv = x.weighted_tsv
            FROM ( 
                SELECT id,
                    {setweight_str}
                    AS weighted_tsv
                FROM articles
            ) AS x
            WHERE x.id = articles.id;

            CREATE INDEX weighted_tsv_idx ON articles USING GIN (weighted_tsv);
            """
        )
        self.conn.commit()
        self.closeConnection()
        # run this with this command 
        # createIndex(["title", "abstract"])
    def loadStopList(archivo):
        stoplist = dict()
        with open(archivo, "r", encoding="utf-8") as file:
            for palabra in file:
                palabra = palabra.strip()  # Eliminar espacios en blanco y saltos de línea adicionales
                stoplist[palabra] = True
        return stoplist


    def process_text(text, stopwords):
        booleanTerms = {"and": "&", "also": "&", "as well as": "&", "in adtition": "&", "moreover": "&", "furthermore": "&", "likewise": "&", "too":"&", "additionally":"&",
        "not": "! &", "no":"! &", "neither": "! &", "nor":"! &"}
        queryResult = ""
        stemmer = SnowballStemmer("english")
        text = text.lower()
        for word in text.split():
            if (word in stopwords and word in booleanTerms):
                queryResult+= stemmer.stem(word) + " "
            elif (word not in stopwords or word in booleanTerms):
                queryResult+= stemmer.stem(word) + " "
        text = queryResult
        queryResult = ""
        stemmer = SnowballStemmer("english")
        for i, word in enumerate(text.split()):
            if(word not in booleanTerms):
                if(i != len(text.split()) - 1): 
                    queryResult+= word + " | " 
                else: queryResult+= word
            else:
              if(queryResult[-2:-1] == "|" and i != len(text.split()) - 1):
                  queryResult = queryResult[:-2] + booleanTerms[word] + " "
              else: queryResult+= word
        #Proecesamiento de stopwords
    
        return queryResult

    def consultQuery(self, query, k):
        start_time = time.time()
        self.connectToDB()
        self.cur.execute(
            f"""            
                set enable_seqscan=false;
                select title, ts_rank_cd(weighted_tsv, query) as rank
                from articles, to_tsquery('english','{query}')  query
                WHERE query @@ weighted_tsv
                ORDER BY rank DESC
                LIMIT {k};
            """
        )
        results = self.cur.fetchall()
        self.conn.commit()
        self.closeConnection()
        end_time = time.time()
        results_list = [list(result) for result in results]
        return results_list, end_time-start_time

'''postgre = Postgre()
postgre.loadData("s")
postgre.createIndex(['title', 'abstract'])
processed_text = postgre.process_text("human rights and politics not also in uk", loadStopList("stoplist-en.txt"))
list = postgre.consultQuery(processed_text,10)
print(list)'''
