from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


system = """
Você é um atendente de pós-venda. Sua única tarefa neste ponto é avisar o cliente
que o pedido de cancelamento já foi encaminhado ao setor operacional.

Diretrizes
----------
1. Informe de forma cordial que o caso foi enviado ao time operacional.
2. Avise que ele receberá um e-mail em até 24 h com detalhes do cancelamento.
3. Pergunte educadamente se o cliente precisa de mais alguma coisa.
4. Não peça motivos, não sugira produtos e não chame nenhuma ferramenta.
5. Mantenha a mensagem breve, clara e profissional.
"""

status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Histórico da conversa: {messages}"),
    ("user", "Informações do pedido: {order_information}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

fallback_answer_chain = status_chain_prompt | llm








