from graph.state import GraphState

from graph.chain.order_status_chain import order_status_chain
def order_status_node(state: GraphState) -> GraphState:

    print(" --- ORDER STATUS NODE ---")
    
    order_number = state["order_number"]

    order_status_chain_result = order_status_chain.invoke({"order_number": order_number, "order_information": state["product_info"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})


   
    
    return {"conversation": [order_status_chain_result]}
