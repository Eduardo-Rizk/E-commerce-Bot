from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from graph.chain.tools.fallback_notification import fallback_notification


system = """
Você é um agente de back-office cuja função **exclusiva** é acionar a ferramenta
`fallback_notification` para encaminhar um pedido de cancelamento a um operador
humano.

Instruções obrigatórias
----------------------
1. **Sempre** chame a ferramenta `fallback_notification` uma única vez.
2. No payload da chamada inclua, exatamente nos campos esperados:
   • `conversation_summary`  → resumo objetivo de todas as mensagens trocadas.  
   • `cancel_reason`         → motivo do cancelamento informado pelo cliente
                               (ou string vazia se ainda não foi declarado).  
   • `order_information`     → dados completos do pedido.
3. Não gere nenhuma resposta ao cliente, texto adicional ou mensagens fora da
   chamada da ferramenta.
4. Não realize outras ações, não sugira produtos, não faça perguntas.

Objetivo
--------
Somente registrar a solicitação para o setor operacional por meio da
`fallback_notification`, nada mais.
"""



llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")


status_chain_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Order information: {order_information}"),
])
tools = [fallback_notification]


fallback_to_operational_chain = status_chain_prompt | llm.bind_tools(tools)








