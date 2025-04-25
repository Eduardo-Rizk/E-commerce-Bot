from dotenv import load_dotenv


from graph.state import GraphState

from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE_HISTORICAL_CONVERSATION, INTENTION, FALLBACK, HELP_ACTIVE_ORDER, LOAD_ORDER_INFO, ORDER_STATUS, SELLER, EXECUTE_TOOL

from graph.nodes.load_historical_conversation import load_historical_conversation
from graph.nodes.IntentionGrader import intention_node
from graph.nodes.help_atctive_order import help_active_order
from graph.nodes.load_order_info import load_order_info_node
from graph.nodes.order_status import order_status_node
from graph.nodes.fallback_node import fallback_node
from graph.nodes.execute_tool_node import execute_tool_node
from graph.nodes.seller_node import seller_node
from langgraph.prebuilt import tools_condition

from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

from graph.consts import Intent, status


def condional_entry_point(state: GraphState):
    print(" --- CONDITIONAL ENTRY POINT ---")

    if state["captured_histoical_conversation"]:
        print(" --INTENTION---")
        return INTENTION
    else:
        print("--RETRIEVE HISTORICAL CONVERSATION---")
        return RETRIEVE_HISTORICAL_CONVERSATION
    

def Intention_redirector(state: GraphState):
    print(" --- INTENTION REDIRECTOR ---")
    if state["intention"] == Intent.ORDER_STATUS:
        if state["order_number"]:
            if state["order_info"] != "" or None:
                return ORDER_STATUS
            else:
                return LOAD_ORDER_INFO
        else:
            return HELP_ACTIVE_ORDER
        
    elif state["intention"] == Intent.EXCHANGE or state["intention"] == Intent.DEVOLUTION or state["intention"] == Intent.CANCEL:
        if state["order_number"]:
            if state["order_info"] != "" or None:
                return FALLBACK
            else:
                return LOAD_ORDER_INFO
        else:
            return HELP_ACTIVE_ORDER
        
    else:
        return SELLER
    
def Order_Info_Status_Fallback(state: GraphState):
    print(" --- ORDER INFO STATUS FALLBACK ---")
    if state["intention"] == Intent.ORDER_STATUS:
        return ORDER_STATUS
    else:
        return FALLBACK


graph = StateGraph(GraphState)

graph.add_node(RETRIEVE_HISTORICAL_CONVERSATION, load_historical_conversation)
graph.add_node(INTENTION, intention_node)
graph.add_node(HELP_ACTIVE_ORDER, help_active_order)
graph.add_node(LOAD_ORDER_INFO, load_order_info_node)
graph.add_node(ORDER_STATUS, order_status_node)
graph.add_node(FALLBACK, fallback_node)
graph.add_node(EXECUTE_TOOL, execute_tool_node)
graph.add_node(SELLER, seller_node)

graph.set_conditional_entry_point(condional_entry_point,
                                  {
                                      INTENTION: INTENTION,
                                      RETRIEVE_HISTORICAL_CONVERSATION: RETRIEVE_HISTORICAL_CONVERSATION,
                                  })

graph.add_edge(RETRIEVE_HISTORICAL_CONVERSATION, INTENTION)
graph.add_conditional_edges(
    INTENTION,
    Intention_redirector,
    {
        ORDER_STATUS: ORDER_STATUS,
        FALLBACK: FALLBACK,
        HELP_ACTIVE_ORDER: HELP_ACTIVE_ORDER,
        LOAD_ORDER_INFO: LOAD_ORDER_INFO,
        SELLER: SELLER,
    },
)

graph.add_edge(HELP_ACTIVE_ORDER,LOAD_ORDER_INFO)

graph.add_conditional_edges(
    LOAD_ORDER_INFO,Order_Info_Status_Fallback,
    {
        ORDER_STATUS: ORDER_STATUS,
        FALLBACK: FALLBACK,
    }

)


graph.add_conditional_edges(
    ORDER_STATUS,
    tools_condition,
    {
        EXECUTE_TOOL: EXECUTE_TOOL,
    },
)
graph.add_conditional_edges(
    FALLBACK,
    tools_condition,
    {
        EXECUTE_TOOL: EXECUTE_TOOL,
    },
)
graph.add_conditional_edges(
    LOAD_ORDER_INFO,
    tools_condition,
    {
        EXECUTE_TOOL: EXECUTE_TOOL,
    },
)
graph.add_conditional_edges(
    SELLER,
    tools_condition,
    {
        EXECUTE_TOOL: EXECUTE_TOOL,
    },
)

graph.add_edge(EXECUTE_TOOL, SELLER)
graph.add_edge(EXECUTE_TOOL, FALLBACK)
graph.add_edge(EXECUTE_TOOL, ORDER_STATUS)
graph.add_edge(EXECUTE_TOOL, LOAD_ORDER_INFO)




from langchain.schema import AIMessage

# 1)  compile
memory = MemorySaver()
app = graph.compile(
        checkpointer   = memory,
        interrupt_after= [SELLER, ORDER_STATUS, FALLBACK]
)

thread = {"configurable": {"thread_id": "777"}}         # 1 por conversa

while True:
    user = input("Você: ").strip()
    if user.lower() in {"sair", "exit"}:
        break

    state = app.invoke(
        {"user_message": user},
        thread)

    # 3) pega a última mensagem da IA
    from langchain_core.messages import AIMessage
    last_ai = next(
        (m for m in reversed(state["conversation"]) if isinstance(m, AIMessage)),
        None,
    )

    if last_ai and not last_ai.additional_kwargs.get("tool_calls"):
        print(f"Bot : {last_ai.content}\n")













