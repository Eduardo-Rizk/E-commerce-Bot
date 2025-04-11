from graph.state import GraphState
from graph.chain.tools.fetch_conversation_fromFile import get_json_as_string
def load_order_info_node(state: GraphState) -> GraphState:
    """
    Lê um arquivo JSON, converte para string e salva em state["infoProduto"].
    """
    filepath = "graph/infoPedido.json"
    
    order_info_str = get_json_as_string(filepath)
    state["infoProduto"] = order_info_str

    return state
