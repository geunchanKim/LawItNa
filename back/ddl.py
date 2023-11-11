instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
db_user = "postgres"
db_pass = "pgvectorwjdfo"
db_name = "pgvector"

import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from transformers import AutoModel, AutoTokenizer

def get_KoSimCSE():
    model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
    tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

    print(type(model))
    print(type(tokenizer))

    return model, tokenizer

model, tokenizer = get_KoSimCSE()

connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=IPTypes.PUBLIC,
    )
    return conn

pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS vector with schema public"
    )
    )
    db_conn.commit()

import json
with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm with schema public"
    )
    )
db_conn.commit()

try :
    with pool.connect() as db_conn:
        db_conn.execute(
            sqlalchemy.text("drop table JUDGE")
        )
        db_conn.commit()
except :
    print("table not in schema")

# create table
with pool.connect() as db_conn:
    db_conn.execute(
    sqlalchemy.text(
        """
        CREATE TABLE JUDGE(
        info VARCHAR(1000),
        v vector(768),
        content VARCHAR(32767)
        )
        """
    )
    )
    db_conn.commit()

#insert table
file_path = 'C:/Users/wjdfo/OneDrive/바탕 화면/lectureitna/LawItNa/output.json'
data = json.load(open(file_path, 'r', encoding = 'utf-8'))

i = 1
with pool.connect() as db_conn:
    for key in data.keys():
        insert_stmt = sqlalchemy.text(
            "INSERT INTO JUDGE VALUES (:info, :v, :content)"
        )

        inputs = tokenizer(key, padding = True, truncation = True, return_tensors = "pt")

        embeddings, _ = model(**inputs, return_dict = False)
        embedding_arr = embeddings[0][0].detach().numpy()
        embedding_str = ",".join(str(x) for x in embedding_arr)
        embedding_str = "["+embedding_str+"]"

        db_conn.execute(
            insert_stmt,
            parameters = {
                "info" : key, "v" : embedding_str, "content" : data[key]
            }
        )

        print("%s, insert %d-tuple clear" %(key, i))
        i += 1

    db_conn.commit()
db_conn.close()