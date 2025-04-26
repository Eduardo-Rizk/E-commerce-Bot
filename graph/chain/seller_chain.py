from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from graph.chain.tools.fetch_catalog_store import fetch_catalog

system = """
You are a system assistant responsible only for retrieving the clothing store catalog when needed.

Instructions:
1. You must use the "fetch_catalog" tool to retrieve the store's catalog.
2. You should not engage in conversation, answer questions, or make product recommendations.
3. Your only job is to retrieve the full catalog to be used by another part of the system.

Reminder:
- Do not generate customer-facing text.
- Do not suggest products.
- Do not explain anything.

Only focus on retrieving and returning the catalog data using the fetch_catalog tool.
"""



status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Historical conversation: {historical_conversation}")
])

tools = [fetch_catalog]

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0).bind_tools(tools)

seller_chain = status_chain_prompt | llm