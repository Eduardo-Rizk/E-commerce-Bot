from graph.state import GraphState
from typing import Any, Dict
from graph.chain.fallback_ask_motivation import get_fallback_ask_motivation_chain

def fallback_ask_motivation(state: GraphState) -> Dict[str, Any]:
    print(" --- FALLBACK ASK MOTIVATION ---")

    intent = state.get("intention")
    fallback_chain = get_fallback_ask_motivation_chain(intent)
    
    fallback_chain_result = fallback_chain.invoke({
        "order_information": state.get("order_info", ""),
        "messages": state.get("messages", []),
    })

    return { "messages": [fallback_chain_result], "captured_motivation": True }
