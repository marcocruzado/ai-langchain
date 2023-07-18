store_db = store()
retriever_pg = store_db.as_retriever(search_kwargs={"k": 1})

func_retriever = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=retriever_pg,
    input_key="input",
)
##############################################


tools = [
    Tool(
        name="promociones",
        func=db_agent.run,
        description="useful for when you need to answer about promociones of restaurants in miraflores",
    ),
    
]

prefix = """Have a conversation with a human, answering the following questions as best you can in spanish. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)


memory = ConversationBufferMemory(memory_key="chat_history",input_key="input")

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)


agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)

while True:
    question = str(input("Question: "))
    if question == "quit":
        break
    print(agent_chain.run(input=question))
