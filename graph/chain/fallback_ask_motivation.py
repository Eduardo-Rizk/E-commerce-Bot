from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.consts import Intent

def get_system_prompt(intent: Intent) -> str:
    
    action_map = { Intent.CANCEL: "cancelamento", Intent.EXCHANGE: "troca", Intent.DEVOLUTION: "devolução" }
    action = action_map.get(intent, "cancelamento")
    
    return f"""
                Você é um assistente de vendas cuja **única** responsabilidade é perguntar, de forma
                educada, o motivo da {action} de um pedido.
                Regras
                ------
                1. Analise a **última mensagem humana**.
                2. Se essa mensagem **ainda não explicar claramente** o motivo da {action},
                responda com um curto pedido de esclarecimento, por exemplo:
                • "Entendo que você deseja fazer a {action} do pedido. Poderia, por favor, informar o
                    motivo da {action} para darmos andamento ao processo?"
                3. Se o motivo **já estiver** explícito, **não envie nenhuma resposta**.
                4. Não chame nenhuma ferramenta, não encaminhe para agentes humanos e não faça
                nenhum outro tipo de sugestão ou explicação.
                Objetivo
                --------
                Coletar o motivo da {action} quando ele ainda não foi fornecido — nada mais.
            """

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

def create_fallback_ask_reason_prompt(intent: Intent):
    return ChatPromptTemplate.from_messages([
        ("system", get_system_prompt(intent)),
        ("user", "Current conversation: {messages}"),
        ("user", "Order information: {order_information}"),
    ])

def get_fallback_ask_motivation_chain(intent: Intent):
    prompt = create_fallback_ask_reason_prompt(intent)
    return prompt | llm