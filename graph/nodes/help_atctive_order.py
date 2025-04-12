from graph.state import GraphState
from typing import Dict
from graph.chain.help_with_active_order_chain import help_with_order_chain
from langchain_core.messages import AIMessage


def help_active_order(state: GraphState) -> GraphState:
    """
    Se numeroPedido estiver vazio, chama a chain que solicita o número do pedido
    e adiciona a resposta ao histórico de conversa como uma AIMessage.
    Caso contrário, retorna o state sem alteração
    """
    print(" --- HELP ACTIVE ORDER NODE ---")

    if not state.get("numeroPedido"):  
        result = help_with_order_chain.invoke({"conversation": state["conversation"]})

        ai_response = AIMessage(content=str(result))

        state["conversation"].append(ai_response)

        return state

    return state
