from graph.state import GraphState
from typing import Any, Dict
from graph.chain.fallback_answer import fallback_answer_chain

def fallback_answer(state: GraphState) -> Dict[str, Any]:
    print(" --- FALLBACK ANSWER NODE---")

    fallback_chain_result = fallback_answer_chain.invoke({
        "order_information": state.get("order_info", ""),
        "messages": state.get("messages", []),
    })

    return {"messages": [fallback_chain_result]}