from graph.state import GraphState
from typing import Any, Dict
from graph.chain.intention_chain import intetion_grader

def intention_node(state: GraphState) -> Dict[str, any]:
    print(" --- INTENTION NODE ---")

    result = intetion_grader.invoke({
        "messages": state.get("messages", []),
    })

    return {"intention": result.intention}
