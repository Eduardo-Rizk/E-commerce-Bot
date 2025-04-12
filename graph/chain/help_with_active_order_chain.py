from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser


system = """You are a polite and helpful customer support representative. The customer has contacted you about an issue related to their order. Your role is to assist them, but first you need the customer’s order number to proceed. Kindly request the order number, and explain that it is required to provide the proper support and resolution."""

order_number_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {conversation}"),
])

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0,)


help_with_order_chain = order_number_prompt | llm | StrOutputParser()





