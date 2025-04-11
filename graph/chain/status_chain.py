from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI



system = """Você é funcionário que está ajudando com suporte ao cliente, sua tarefa é a partir da conversa atual, o histórico de conversas e informações sobre o produto, responder a pergunta do cliente."""

status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {conversation}"),
    ("user", "Historical conversation: {historical_conversation}"),
    ("user", "Product information: {product_information}"),
])

