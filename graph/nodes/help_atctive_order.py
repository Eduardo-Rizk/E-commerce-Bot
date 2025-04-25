from graph.state import GraphState
from typing import Dict
from graph.chain.help_with_active_order_chain import help_with_order_chain
from langchain_core.messages import AIMessage


def help_active_order(state: GraphState) -> GraphState:
    """
    Se order_number for FALSE, chama a chain que solicita o número do pedido
    e adiciona a resposta ao histórico de conversa como uma AIMessage.
    """
    print(" --- HELP ACTIVE ORDER NODE ---")

 
    result = help_with_order_chain.invoke({"conversation": state["conversation"]})

    return {
        "conversation": [result],
        "order_number": True,
    }


