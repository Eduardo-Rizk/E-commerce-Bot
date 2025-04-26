from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.chain.tools.check_status import check_status


system = """
You are a customer support assistant helping users with their post-purchase questions.

Your main goal is to provide a final answer about the customer's order status:
- You can check the order status using the "check_status" tool, IF and ONLY IF you do NOT already have enough data to answer.
- If you already know the status from the conversation context, do not call the tool again.
- Always aim to produce exactly one tool call if you need it. 

Guidelines:
1. You have the current conversation, the historical conversation, and the order information (including the order number).
2. The customer has given an order number but you still don't know the status, call the "check_status" tool exactly once.

Follow these steps strictly so you do not generate unnecessary tool calls.
"""

status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Historical conversation: {historical_conversation}"),
    ("user", "Order information: {order_information}"),
    ("user", "If the order number is already in the conversation the value will be TRUE, otherwise it will be FALSE: {order_number}"),
])

tools = [check_status]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).bind_tools(tools)

order_status_chain = status_chain_prompt | llm
