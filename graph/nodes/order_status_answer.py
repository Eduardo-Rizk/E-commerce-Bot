from graph.state import GraphState
from graph.chain.order_status_answer_chain import order_status_answer_chain
from typing  import Dict, Any

def order_status_answer(state: GraphState) -> Dict[str, Any]:
    print(" --- ORDER STATUS NODE ANSWER ---")

    order_number = state.get("order_number")                
    order_info = state.get("order_info", "")
    messages = state.get("messages", [])
    hist_conv = state.get("historical_conversation", [])

    result = order_status_answer_chain.invoke({
        "order_number":         order_number,
        "order_information":    order_info,
        "messages":         messages,
        "historical_conversation": hist_conv,
    })

    return {"messages": [result]}