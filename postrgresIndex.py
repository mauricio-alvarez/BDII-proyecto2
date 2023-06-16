import psycopg2
import json
import nltk
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


    def process_text(self, text):
        operators = ['and', 'or', 'not', 'also', 'too', 'either']
        operator_map = {'and': '&', 'or': '|', 'not': '!', 'also': '&', 'too': '&', 'either': '|'}
        default_operator = '|'
        stop_words = set(stopwords.words('english'))
        words = text.split()
        processed_words = []
        for i, word in enumerate(words):
            if word.lower() in operators:
                if word.lower() == 'not':
                    if processed_words and processed_words[-1] not in operator_map.values():
                        processed_words.append('&')
                    processed_words.append(operator_map[word.lower()])
                elif word.lower() != 'not' and (i == 0 or words[i-1].lower() != 'not'):
                    processed_words.append(operator_map[word.lower()])
            elif word.lower() not in stop_words:
                if i > 0 and words[i-1].lower() not in operators and words[i-1].lower() not in stop_words:
                    processed_words.append(default_operator)
                processed_words.append(word.lower())
        return ' '.join(processed_words)

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
processed_text = postgre.process_text("human rights and politics not also in uk")
list = postgre.consultQuery(processed_text,10)
print(list)'''