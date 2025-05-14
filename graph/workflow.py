from dotenv import load_dotenv




from graph.state import GraphState
from langchain_core.messages import AIMessage


from langgraph.graph import END, StateGraph


from graph.consts import RETRIEVE_HISTORICAL_CONVERSATION, INTENTION, FALLBACK, HELP_ACTIVE_ORDER, LOAD_ORDER_INFO, ORDER_STATUS, SELLER, EXECUTE_TOOL, ORDER_STATUS_ANSWER,SELLER_ANSWER, FALLBACK_ANSWER, FALLBACK_ASK_MOTIVATION

from graph.nodes.load_historical_conversation import load_historical_conversation
from graph.nodes.IntentionGrader import intention_node
from graph.nodes.help_active_order import help_active_order
from graph.nodes.load_order_info import load_order_info_node
from graph.nodes.tool_call_order_status import order_status_tool_call
from graph.nodes.fallback_node import fallback_node
from graph.nodes.fallback_ask_motivation import fallback_ask_motivation
from graph.nodes.fallback_answer import fallback_answer


from graph.nodes.execute_tool_node import execute_tool_node
from graph.nodes.seller_node import seller_node
from langgraph.prebuilt import tools_condition
from graph.nodes.order_status_answer import order_status_answer
from graph.nodes.seller_answer_node import seller_answer_node
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()


from graph.consts import Intent, status

def conditional_entry_point(state: GraphState):
    print(" --- CONDITIONAL ENTRY POINT ---")
    if state.get("captured_histoical_conversation", False):
        print(" --INTENTION---")
        return INTENTION
    else:
        print("--RETRIEVE HISTÓRICAL CONVERSATION---")
        return RETRIEVE_HISTORICAL_CONVERSATION

def Intention_redirector(state: GraphState):
    print(" --- INTENTION REDIRECTOR ---")
    intent        = state.get("intention", Intent.GENERIC)
    order_number  = state.get("order_number", False)
    has_orderinfo = bool(state.get("order_info"))
    has_motivation = state.get("captured_motivation", False)
    catalog_store = state.get("catalog_store", "")


    if intent == Intent.ORDER_STATUS:
        if order_number:
            return ORDER_STATUS if has_orderinfo else LOAD_ORDER_INFO
        return HELP_ACTIVE_ORDER


    elif intent in (Intent.EXCHANGE, Intent.DEVOLUTION, Intent.CANCEL):
        if order_number:
            if has_orderinfo:
                if has_motivation:
                    return FALLBACK
                else:
                    return FALLBACK_ASK_MOTIVATION
            else:
                return LOAD_ORDER_INFO
        return HELP_ACTIVE_ORDER

    elif intent == Intent.GENERIC or intent == Intent.PRODUCT_INFO:
        if catalog_store != "":
            return SELLER_ANSWER
    return SELLER

def Order_Info_Status_Fallback(state: GraphState):
    print(" --- ORDER INFO -> STATUS or FALLBACK ---")
    intent = state.get("intention", Intent.GENERIC)
    if intent == Intent.ORDER_STATUS:
        return ORDER_STATUS
    else:
        if state.get("captured_motivation", False):
            return FALLBACK_ANSWER
        else:
            return FALLBACK_ASK_MOTIVATION




def Execute_Tool_Redirector(state: GraphState):
    print(" --- TOOL REDIRECTOR ---")
    messages = state.get("messages", [])
    last_tool_name = None


    # varre do fim para o começo, pois a mensagem mais recente está no fim
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            tool_calls = msg.additional_kwargs.get("tool_calls", [])
            if tool_calls:
                last_tool_name = tool_calls[-1]["function"]["name"]
                break


    if   last_tool_name == "check_status":
        return ORDER_STATUS_ANSWER
    elif last_tool_name == "fallback_notification":
        return FALLBACK_ANSWER
    elif last_tool_name == "fetch_catalog":
        return SELLER_ANSWER
    else:
        return FALLBACK

graph = StateGraph(GraphState)


graph.add_node(RETRIEVE_HISTORICAL_CONVERSATION, load_historical_conversation)
graph.add_node(INTENTION, intention_node)
graph.add_node(HELP_ACTIVE_ORDER, help_active_order)
graph.add_node(LOAD_ORDER_INFO, load_order_info_node)

graph.add_node(ORDER_STATUS, order_status_tool_call)
graph.add_node(ORDER_STATUS_ANSWER, order_status_answer)


graph.add_node(FALLBACK, fallback_node)
graph.add_node(FALLBACK_ASK_MOTIVATION, fallback_ask_motivation)
graph.add_node(FALLBACK_ANSWER, fallback_answer)


graph.add_node(EXECUTE_TOOL, execute_tool_node)


graph.add_node(SELLER, seller_node)
graph.add_node(SELLER_ANSWER, seller_answer_node)
from langchain_core.messages import HumanMessage, AIMessage




graph.set_conditional_entry_point(conditional_entry_point,
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
        FALLBACK_ASK_MOTIVATION: FALLBACK_ASK_MOTIVATION,
        HELP_ACTIVE_ORDER: HELP_ACTIVE_ORDER,
        LOAD_ORDER_INFO: LOAD_ORDER_INFO,
        SELLER: SELLER,
        SELLER_ANSWER: SELLER_ANSWER,
    },
)


graph.add_edge(HELP_ACTIVE_ORDER,LOAD_ORDER_INFO)


graph.add_conditional_edges(
    LOAD_ORDER_INFO,Order_Info_Status_Fallback,
    {
        ORDER_STATUS: ORDER_STATUS,
        FALLBACK: FALLBACK,
        FALLBACK_ASK_MOTIVATION: FALLBACK_ASK_MOTIVATION,
    }


)

graph.add_conditional_edges(
    ORDER_STATUS,
    tools_condition,
    {
        "tools": EXECUTE_TOOL,
        END: ORDER_STATUS_ANSWER,
    },
)
graph.add_conditional_edges(
    FALLBACK,
    tools_condition,
    {
        "tools": EXECUTE_TOOL,
        END: FALLBACK_ANSWER,
    },
)
graph.add_conditional_edges(
    SELLER,
    tools_condition,
    {
        "tools": EXECUTE_TOOL,
        END: SELLER_ANSWER,
    },
)


graph.add_edge(FALLBACK_ASK_MOTIVATION, FALLBACK)

graph.add_conditional_edges(
    EXECUTE_TOOL,
    Execute_Tool_Redirector,
    {
        ORDER_STATUS_ANSWER: ORDER_STATUS_ANSWER,
        FALLBACK_ANSWER          : FALLBACK_ANSWER,
        SELLER_ANSWER            : SELLER_ANSWER,
    },
)

memory = MemorySaver()
app = graph.compile(
        checkpointer   = memory,
        interrupt_after= [SELLER_ANSWER, ORDER_STATUS_ANSWER, FALLBACK_ANSWER, HELP_ACTIVE_ORDER, FALLBACK_ASK_MOTIVATION],
)



# app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# print(app.get_graph().draw_ascii())

thread = {"configurable": {"thread_id": "777"}}        


while True:
    user = input("Você: ").strip()
    if user.lower() in {"sair", "exit"}:
        break
    state = app.invoke(
        {"messages": [HumanMessage(content=user)]},   # <- mudou aqui
        thread
    )
    # pega a última resposta do bot (caso não seja call de ferramenta)
    last_ai = next(
        (m for m in reversed(state["messages"]) if isinstance(m, AIMessage)),
        None,
    )
    if last_ai:                    
        print(f"Bot : {last_ai.content}\n")
