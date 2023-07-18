from langchain.agents import create_sql_agent
from langchain.agents import Tool, AgentType, initialize_agent, AgentExecutor
from functions.embeddings_demo import store
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, SerpAPIWrapper, LLMChain,SQLDatabase, SQLDatabaseChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import (
    LLMSingleActionAgent,
    AgentOutputParser,
)

from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
import os

#Otra forma desde una URL
from langchain.chat_models import ChatOpenAI


from dotenv import load_dotenv
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
print(os.environ["OPENAI_API_KEY"])

####FUENTES DE INFORMACION"#####################

# tiene que buscar en google y devolver el primer resultado todas las busquedas sera en Peru y en español
search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPAPI_API_KEY"], params={
                        "engine": "google", "google_domain": "google.com", "gl": "pe", "hl": "es-419"})

#-------------------------------------------------
#postgresql+psycopg2://pguser:password@localhost:5433/doc_search
input_db = SQLDatabase.from_uri('postgresql+psycopg2://postgres:root@localhost:5432/postgres')
llm = ChatOpenAI(temperature=0)
db_agent = SQLDatabaseChain(llm = llm,
                            database = input_db,
                            verbose=True,
                            input_key="input",
)

#-------------------------------------------------

tools = [
    Tool(
        name="Search in Database",
        func=db_agent.run,
        description="cuando necesites saber sobre promociones de los establecimientos que el club el comercio tiene convenio",
    ),
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
]

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)


while True:
    user_input = str(input("User: ")+"responde en español ")
    agent_output = agent.run(input=user_input)
    print(agent_output)