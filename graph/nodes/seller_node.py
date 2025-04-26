from graph.state import GraphState
from graph.chain.seller_chain import seller_chain
from typing  import Dict, Any

def seller_node(state: GraphState) -> Dict[str, Any]:
    """
    Recupera as informações sobre o catálogo
    """
    print(" --- Seller Node ---")

    result = seller_chain.invoke({
        "messages":          state.get("messages", []),
        "historical_conversation": state.get("historical_conversation", []),
    })

    return {"messages": [result]}
