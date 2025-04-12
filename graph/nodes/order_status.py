from graph.state import GraphState

from graph.chain.order_status_chain import order_status_chain
def order_status_node(state: GraphState) -> GraphState:

    print(" --- ORDER STATUS NODE ---")
    
    order_number = state["numeroPedido"]

    order_status_chain_result = order_status_chain.invoke({"order_number": order_number, "order_information": state["infoProduto"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})


    state["conversation"].append(order_status_chain_result)
    
    return state