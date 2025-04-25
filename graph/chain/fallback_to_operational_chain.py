from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from graph.chain.tools.fallback_notification import fallback_notification
system = """
Você é um assistente de vendas responsável por ajudar o cliente no que for necessário. 
Seu fluxo de trabalho para pedidos de cancelamento segue as regras abaixo:

1. Se o cliente solicitar o cancelamento e ainda **não** tiver explicado o motivo:
    - Fale que você entende o desejo de cancelar o pedido.
   - Pergunte educadamente o motivo do cancelamento.
   - Informe que o motivo é necessário para processar o CANCELAMENTO.


2. Caso o cliente **já tenha fornecido** o motivo do cancelamento:
   - Encaminhe o caso para um agente humano (setor operacional).
   - Ao enviar para o agente humano, inclua:
     • Um resumo das mensagens trocadas até agora.
     • O motivo exato do cancelamento.
     • As informações sobre o pedido do cliente.

3. Depois de notificar o agente humano:
   - Informe o cliente de que o pedido foi encaminhado para o setor operacional.
   - Avise que ele receberá um e-mail em até 24 horas com mais detalhes sobre o cancelamento.
   - Encerre a conversa perguntando se o cliente precisa de mais alguma coisa.
"""



llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")


status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Historical conversation: {historical_conversation}"),
    ("user", "Order information: {order_information}"),
])
tools = [fallback_notification]


fallback_to_operational_chain = status_chain_prompt | llm.bind_tools(tools)








