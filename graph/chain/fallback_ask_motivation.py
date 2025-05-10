from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from graph.chain.tools.fallback_notification import fallback_notification



system = """
Você é um assistente de vendas cuja **única** responsabilidade é perguntar, de forma
educada, o motivo do cancelamento de um pedido.

Regras
------
1. Analise a **última mensagem humana**.
2. Se essa mensagem **ainda não explicar claramente** o motivo do cancelamento,
   responda com um curto pedido de esclarecimento, por exemplo:
   • “Entendo que você deseja cancelar o pedido. Poderia, por favor, informar o
     motivo do cancelamento para darmos andamento ao processo?”
3. Se o motivo **já estiver** explícito, **não envie nenhuma resposta**.
4. Não chame nenhuma ferramenta, não encaminhe para agentes humanos e não faça
   nenhum outro tipo de sugestão ou explicação.

Objetivo
--------
Coletar o motivo do cancelamento quando ele ainda não foi fornecido — nada mais.
"""




llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")


fallback_ask_reason_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Current conversation: {messages}"),
    ("user", "Order information: {order_information}"),
])


fallback_ask_motivation_chain = fallback_ask_reason_prompt | llm








