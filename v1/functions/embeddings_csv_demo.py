import os 
from typing import List, Tuple
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


path_directory ="./v1/data"
path_file = "datos_gastronomia.csv"

path = os.path.join(path_directory, path_file)
print(path)

loader = CSVLoader(path, encoding="utf-8")
pages = loader.load()
# Loading Embeddings
embeddings = OpenAIEmbeddings()

# Loading Database
connection_string = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5433")),
    database=os.environ.get("PGVECTOR_DATABASE", "doc_search"),
    user=os.environ.get("PGVECTOR_USER", "pguser"),
    password=os.environ.get("PGVECTOR_PASSWORD", "password"),
)

collection_name = "promociones"

def save_database(collection_name: str, connection_string: str, docs: List[Document], embeddings: OpenAIEmbeddings) -> str:
    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=collection_name,
        connection_string=connection_string,
    )
    return "Database created and populated"

print(save_database(collection_name, connection_string, pages, embeddings))