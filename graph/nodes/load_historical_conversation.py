
from graph.state import GraphState
from graph.chain.tools.helper.fetch_conversation_from_json import fetch_conversation_from_json
from typing  import Dict, Any

def load_historical_conversation(state: GraphState) -> Dict[str, Any]:
    """
    Carrega o histórico mock de um JSON.  Sempre devolve as chaves-alvo,
    mas nunca lê com [] para evitar KeyError.
    """
    print(" --- CARREGANDO O HISTÓRICO ---")
    filepath = "graph/conversation_history.json"
    historical_messages = fetch_conversation_from_json(filepath)

    return {
        "historical_conversation": historical_messages,
        "captured_histoical_conversation": True,
    }
