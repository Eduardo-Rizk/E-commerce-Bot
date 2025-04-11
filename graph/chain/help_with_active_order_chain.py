from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI



system = """You are a polite and helpful customer support representative. The customer has contacted you about an issue related to their order. Your role is to assist them, but first you need the customer’s order number to proceed. Kindly request the order number, and explain that it is required to provide the proper support and resolution."""

order_number_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {conversation}"),
])

help_with_order_chain = order_number_prompt | ChatOpenAI(temperature=0, model="gpt-4o-mini")





