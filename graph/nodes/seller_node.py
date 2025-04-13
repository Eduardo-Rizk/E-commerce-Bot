from graph.state import GraphState
from graph.chain.seller_chain import seller_chain
from langchain_core.messages import BaseMessage

def seller_node(state: GraphState) :
    """
    Node que executa a seller_chain para responder dúvidas ou fazer recomendações
    com base no catálogo e na conversa atual. Retorna apenas novas mensagens,
    permitindo que LangGraph faça o append automaticamente via `add_messages`.
    """
    print(" --- Seller Node ---")

    seller_chain_result = seller_chain.invoke({
        "catalog_store": state["catalog_store"],
        "conversation": state["conversation"],
        "historical_conversation": state["historical_conversation"]
    })

    return {"conversation": [seller_chain_result]}
