from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser


system = """Você é um representante de atendimento ao cliente educado e prestativo. O cliente entrou em contato sobre um problema relacionado ao pedido dele. Seu papel é ajudá-lo, mas primeiro você precisa do número do pedido para prosseguir. Solicite gentilmente o número do pedido, explicando que ele é necessário para continuar com o suporte."""

order_number_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
])

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0,)


help_with_order_chain = order_number_prompt | llm 





