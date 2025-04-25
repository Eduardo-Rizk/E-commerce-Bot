from graph.state import GraphState
from graph.chain.tools.helper.fetch_json_string import get_json_as_string
from typing import Dict, Any

def load_order_info_node(state: GraphState) -> Dict[str, Any]:
    """
    Lê o arquivo JSON do pedido, converte para string
    e devolve um diff que atualiza `order_info`.
    (Não acessa o state com [] para evitar KeyError.)
    """
    filepath = "graph/infoPedido.json"
    order_info_str = get_json_as_string(filepath)

    return {"order_info": order_info_str}

