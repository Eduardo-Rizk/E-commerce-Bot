from graph.state import GraphState
from graph.chain.tools.helper.fetch_json_string import get_json_as_string


def load_order_info_node(state: GraphState) -> GraphState:
    """
    Lê um arquivo JSON, converte para string e salva em state["order_info"].
    """
    filepath = "graph/infoPedido.json"
    
    order_info_str = get_json_as_string(filepath)
    state["order_info"] = order_info_str

    return state
