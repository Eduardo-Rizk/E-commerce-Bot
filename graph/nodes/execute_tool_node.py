from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from graph.consts import Intent
from graph.state import GraphState
from graph.chain.tools.check_status import check_status 





tool_node = ToolNode(tools=[check_status])


def execute_tool_node(state: GraphState) -> GraphState:
    print("-- EXECUTING TOOL NODE --")

    # Aqui, invocamos o tool_node passando a conversa atual.
    # O ToolNode se encarrega de achar o tool_calls, executar a tool
    # e retornar a conversa atualizada com os resultados.
    updated_conversation = tool_node.invoke(state["conversation"])

    # Substituímos a conversa anterior pela nova
    state["conversation"] = updated_conversation

    return state

