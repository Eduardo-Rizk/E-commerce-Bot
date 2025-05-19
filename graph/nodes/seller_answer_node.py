from graph.state import GraphState
from graph.chain.seller_answer_chain import seller_answer_chain
from typing  import Dict, Any

def seller_answer_node(state: GraphState) -> Dict[str, Any]:
    """
    Responde dúvidas / faz recomendações usando o catálogo.
    """
    print(" --- SELLER ANSWER NODE ---")

    # print("Mensagens", state.get("messages", []))

    result = seller_answer_chain.invoke({
        "catalog_store":         state.get("catalog_store", ""),
        "messages":          state.get("messages", []),
    })


    return {"messages": [result]}
