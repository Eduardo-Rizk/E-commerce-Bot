from graph.state import GraphState
from graph.chain.tools.helper.fetch_conversation_from_json import fetch_conversation_from_json
from typing import Any, Dict

def load_historical_conversation(state: GraphState) -> Dict[str, any]:
    """
    Carrega o histórico de conversas (mock) de um arquivo JSON
    e atualiza state['historical_conversation'] apenas na primeira vez.
    """


    print(" --- CARREGANDO O HISTÓRICO ---")
    filepath = "graph/conversation_history.json"
    historical_messages = fetch_conversation_from_json(filepath)

  

    
    return {"historical_conversation": historical_messages, "captured_histoical_conversation": True}   
