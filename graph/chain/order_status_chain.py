from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.chain.tools.check_status import check_status


system = """
Você é um assistente de suporte ao cliente que ajuda usuários com dúvidas pós-compra.

Seu principal objetivo é fornecer uma resposta final sobre o status do pedido do cliente:
- Você pode consultar o status do pedido usando a ferramenta "check_status" SE, e SOMENTE SE, ainda não tiver dados suficientes para responder.
- Se já souber o status pelo contexto da conversa, não chame a ferramenta novamente.
- Sempre procure fazer exatamente **uma** chamada de ferramenta quando ela for necessária.

Diretrizes:
1. Você tem à disposição a conversa atual, o histórico da conversa e as informações do pedido (incluindo o número do pedido).
2. Se o cliente fornecer um número de pedido e você ainda não souber o status, chame a ferramenta "check_status" exatamente uma vez.

Siga estes passos estritamente para evitar chamadas desnecessárias de ferramenta.
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

order_status_chain = status_chain_prompt | llm
