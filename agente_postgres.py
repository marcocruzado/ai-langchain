from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from langchain import OpenAI

# mudulos propios
from functions.embeddings_demo import store

import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY", "")


# Loading Embeddings
llm = OpenAI(temperature=0.9)

# my store
store_db = store()
vector_store = store_db

# config vectorstore
vectorstore_info = VectorStoreInfo(
    name="reglas_de_transito",
    description="Reglas de transito 2023",
    vectorstore=vector_store,
)

# config toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# config agent
agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit,verbose=True)

#inicializar agente
while True:
    query = str(input("Ingrese su consulta: "))
    if query == "exit":
        break
    else:
        response = agent_executor.run(query)
    
    print("*"*12,"RESPUESTA","*"*12)
    print(response)
    print("*"*35)