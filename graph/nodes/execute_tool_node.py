from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from graph.consts import Intent
from graph.state import GraphState
from graph.chain.tools.check_status import check_status 
from graph.chain.tools.fetch_catalog_store import fetch_catalog
from graph.chain.tools.fallback_notification import fallback_notification



tool_node = ToolNode(tools=[check_status, fetch_catalog,fallback_notification])


def execute_tool_node(state: GraphState) -> GraphState:
    """
    Node responsável por executar chamadas de ferramentas (tools) detectadas na conversa.

    Este nó utiliza o ToolNode do LangGraph para:
    - Identificar automaticamente tool calls geradas pela LLM (como `check_status` ou `fetch_catalog`).
    - Executar as ferramentas registradas com base nas chamadas detectadas.
    - Adicionar as respostas das ferramentas como ToolMessages na conversa.

    Args:
        state (GraphState): O estado atual do grafo, contendo o histórico de conversa.

    Returns:
        GraphState: O estado atualizado, com a conversa estendida com as respostas das ferramentas.
    """



    print("-- EXECUTING TOOL NODE --")

    updated_conversation = tool_node.invoke(state["conversation"])
    state["conversation"] = updated_conversation

    return state



