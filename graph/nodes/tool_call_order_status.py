from graph.state import GraphState
from graph.chain.order_status_chain import order_status_chain
from typing  import Dict, Any

def order_status_tool_call(state: GraphState) -> Dict[str, Any]:
    print(" --- ORDER STATUS NODE ---")

    order_number = state.get("order_number")                
    order_info = state.get("order_info", "")
    messages = state.get("messages", [])
    hist_conv = state.get("historical_conversation", [])

    result = order_status_chain.invoke({
        "order_number":         order_number,
        "order_information":    order_info,
        "messages":         messages,
        "historical_conversation": hist_conv,
    })

    print(" O resultado da chamada é: ", result)

    return {"messages": [result]}
