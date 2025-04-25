from graph.state import GraphState
from typing import Any, Dict
from graph.chain.fallback_to_operational_chain import fallback_to_operational_chain

def fallback_node(state: GraphState) -> Dict[str, Any]:
    print(" --- HELP FALLBACK NODE ---")

    # leitura segura com defaults
    fallback_chain_result = fallback_to_operational_chain.invoke({
        "order_information":      state.get("order_info", ""),
        "messages":           state.get("messages", []),
        "historical_conversation": state.get("historical_conversation", []),
    })

    # sempre devolva as chaves que você alterou/adicionou
    return {"messages": [fallback_chain_result]}
