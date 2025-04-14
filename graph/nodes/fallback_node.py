from graph.state import GraphState
from typing import Any, Dict
from graph.chain.fallback_to_operational_chain import fallback_to_operational_chain
def fallback_node(state: GraphState) -> Dict[str, Any]:

    print(" --- HELP FALLBACK NODE ---")
    
    fallback_chain_result = fallback_to_operational_chain.invoke({"order_information": state["product_info"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})
       
    return {"conversation": [fallback_chain_result]}