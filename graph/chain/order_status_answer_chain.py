from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


system = """
Você é um assistente de suporte ao cliente ajudando os usuários com suas perguntas pós-compra.
O seu cliente está perguntando sobre o status do pedido.
Você tem acesso a informações sobre o pedido e o número do pedido dele, Você deve usar essas informações  Se nescessário para responder a pergunta dele.
Você também tem acesso a conversa atual com o cliente, siga um linha de raciocínio lógica para responder a pergunta dele, levando em consideração o que já foi falado na conversa atual.
Responda de forma clara com educação e empatia, como se você fosse um humano.

Você deve usar a informação sobre o status do pedido que já está na conversa atual como uma tool message. Use esssa informação para responder a pergunta do cliente, sobre qual é o status do pedido dele.
"""

status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Order information: {order_information}"),
    ("user", "If the order number is already in the conversation the value will be TRUE, otherwise it will be FALSE: {order_number}"),
])


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

order_status_answer_chain = status_chain_prompt | llm
