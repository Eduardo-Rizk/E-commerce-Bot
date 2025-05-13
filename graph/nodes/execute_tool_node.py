from graph.state import GraphState
from langgraph.prebuilt import ToolNode
from graph.chain.tools.check_status           import check_status
from graph.chain.tools.fetch_catalog_store    import fetch_catalog
from graph.chain.tools.fallback_notification  import fallback_notification
from typing import Any, Dict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage


tool_node = ToolNode(tools=[check_status, fetch_catalog, fallback_notification])

def execute_tool_node(state: GraphState) -> Dict[str, Any] :
    """
    Executa tool-calls encontradas na última AIMessage e
    insere ToolMessages na conversa.
    """
    print("-- EXECUTING TOOL NODE --")

    conversation = state.get("messages", [])
    updated_conversation = tool_node.invoke(conversation)


    content = None
    last_tool_name = None
    # varre do fim para o começo; para quando achar o fetch_catalog
    for msg in reversed(updated_conversation):
        if isinstance(msg, ToolMessage):
            content = getattr(msg, "content", None)
            last_tool_name = getattr(msg, "name", None)
            break
    if last_tool_name == "fetch_catalog":
        return {"messages": updated_conversation, "catalog_store": content}
    
    return {"messages": updated_conversation}
