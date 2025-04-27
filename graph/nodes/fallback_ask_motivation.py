from graph.state import GraphState
from typing import Any, Dict
from graph.chain.fallback_ask_motivation import fallback_ask_reason

def fallback_ask_motivation(state: GraphState) -> Dict[str, Any]:
    print(" --- FALLBACK ASK MOTIVATION ---")

    fallback_chain_result = fallback_ask_reason.invoke({
        "order_information": state.get("order_info", ""),
        "messages": state.get("messages", []),
    })

    return {"messages": [fallback_chain_result], "captured_motivation": True}