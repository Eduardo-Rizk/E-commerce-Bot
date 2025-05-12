from graph.state import GraphState
from langgraph.prebuilt import ToolNode
from graph.chain.tools.check_status           import check_status
from graph.chain.tools.fetch_catalog_store    import fetch_catalog
from graph.chain.tools.fallback_notification  import fallback_notification

tool_node = ToolNode(tools=[check_status, fetch_catalog, fallback_notification])

def execute_tool_node(state: GraphState) -> GraphState:
    """
    Executa tool-calls encontradas na última AIMessage e
    insere ToolMessages na conversa.
    """
    print("-- EXECUTING TOOL NODE --")

    conversation = state.get("messages", [])
    updated_conversation = tool_node.invoke(conversation)

    print("Updated conversation: ", updated_conversation)
    return {"messages": updated_conversation}
