import os
from typing import List, Tuple
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
print(os.environ["OPENAI_API_KEY"])

path="./data/Reglamento-Nacional-de-Transito.txt"

def documents_loader(path: str) -> List[Tuple[str, str]]:
    # Loading Documents
    loader = TextLoader(path, encoding="utf-8")

    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=0,
        length_function=len,
    )
    docs = text_splitter.split_documents(documents)

    return docs

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


# name of the collection in the database
collection_name = "reglas_de_transito"


def save_database(collection_name: str, connection_string: str, docs: List[Document], embeddings: OpenAIEmbeddings) -> str:
    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=collection_name,
        connection_string=connection_string,
    )
    return "Database created and populated"

def store():
    storedb = PGVector(
        collection_name=collection_name,
        connection_string=connection_string,
        embedding_function=embeddings,
    )
    print(storedb,type(storedb))
    return storedb
