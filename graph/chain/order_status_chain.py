from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.chain.tools.check_status import check_status


system = """
O seu único objetivo é verificar o status de um pedido com base no número do pedido
fornecido.
Você deve usar a ferramenta `check_status` para verificar o status do pedido.
"""


status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Historical conversation: {historical_conversation}"),
    ("user", "Order information: {order_information}"),
    ("user", "Order number is present {order_number}"),
])

tools = [check_status]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).bind_tools(tools)

order_status_chain = status_chain_prompt | llm.bind_tools(tools)
