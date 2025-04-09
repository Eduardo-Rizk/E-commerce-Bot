from graph.state import GraphState
from chain.fetch_conversation_fromFile import fetch_conversation_from_json

def load_historical_conversation(state: GraphState) -> GraphState:
    """
    Carrega o histórico de conversas (mock) de um arquivo JSON
    e atualiza state['historical_conversation'] apenas na primeira vez.
    """
    if state["captured_histoical_conversation"]:
        # Se já foi carregado, não faz nada
        print("[load_historical_conversation_if_needed] Histórico já carregado.")
        return state

    print(" --- CARREGANDO O HISTÓRICO ---")
    filepath = "conversation_history.json"
    historical_messages = fetch_conversation_from_json(filepath)

    state["historical_conversation"] = historical_messages
    state["captured_histoical_conversation"] = True

    
    return state
