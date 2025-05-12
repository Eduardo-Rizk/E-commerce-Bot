
from graph.state import GraphState
from typing import Dict
from graph.chain.help_with_active_order_chain import help_with_order_chain

def help_active_order(state: GraphState) -> Dict[str, any]:
    print(" --- HELP ACTIVE ORDER NODE ---")

    result = help_with_order_chain.invoke({\
        "messages": state.get("messages", []),
    })

    return {
        "messages": [result],
        "order_number": True,               
    }



