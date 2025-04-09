from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from consts import Intent

class GradedIntention(BaseModel):
    """
    Class to represent the intention of the graph.
    """
    intention: Intent = Field(description="I want you to define the intention of the user based on the conversation."
    "If the person has the intention to check the order status, return an object Intent.ORDER_STATUS."
    "If the intention is to exchange the product, return an object Intent.EXCHANGE."
    "If the intention is to inquire about product information, return an object Intent.PRODUCT_INFO."
    "If the intention is still not well defined, return an object Intent.GENERIC.")


llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
structured_llm_grader = llm.with_structured_output(GradedIntention)

system = """You are a conversation analyzer, that analyzes the conversation and defines the intention of the user, ALWAYS return the current intention"""

intetion_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {conversation}"),
])

intetion_grader = intetion_prompt | structured_llm_grader