import os
from langchain_xai import ChatXAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def ask_grok(question, calls_df):
    if not os.getenv("XAI_API_KEY"):
        return "Missing XAI_API_KEY"

    summary = calls_df.head(10).to_string(index=False)

    llm = ChatXAI(model="grok-beta", api_key=os.getenv("XAI_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior telecom NOC engineer."),
        ("human", "Question: {question}\n\nRecent Calls:\n{data}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "question": question,
        "data": summary
    })
