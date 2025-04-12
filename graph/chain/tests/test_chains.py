from dotenv import load_dotenv

load_dotenv()


import graph.chain.tools.fetch_conversation_fromFile as fetch_conversation
import os 
import pytest
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from graph.chain.intention_chain import GradedIntention, intetion_grader
from graph.consts import Intent
from graph.state import GraphState
from graph.nodes.help_atctive_order import help_active_order



from graph.nodes.execute_tool_node import execute_tool_node


from graph.chain.order_status_chain import order_status_chain

from graph.nodes.order_status import order_status_node


def test_intention():


    conversation_mock: list[BaseMessage] = [
        HumanMessage(content="Olá, tudo bem? Comprei um produto há duas semanas e não chegou ainda."),
        AIMessage(content="Entendi! Pode me fornecer o número do seu pedido, por favor?"),
        HumanMessage(content="Claro, o número do meu pedido é #98765. Consegue me dizer onde ele está agora?")
    ]
    
    result = intetion_grader.invoke({"conversation": conversation_mock})
    

    assert result.intention == Intent.ORDER_STATUS, f"Esperado: {Intent.ORDER_STATUS}, obtido: {result.intention}"


def test_help_active_order_should_ask_for_order_number_when_info_empty():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "infoProduto": "",
        "numeroPedido": ""
    }

    updated_state = help_active_order(state)



    # Verifica se a mensagem da AI foi adicionada
    assert isinstance(updated_state["conversation"][-1], AIMessage)

def test_help_active_order_InfoProduto_completo():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "infoProduto": "132dsadw313",
        "numeroPedido": "123456789"
    }

    updated_state = help_active_order(state)



    # Verifica se não houve adição de mensagem da AI
    assert len(updated_state["conversation"]) == 1, "A conversa não deve ter mudado."
    assert isinstance(updated_state["conversation"][-1], HumanMessage)



def test_order_status_chain_toolCall_orderStatus():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "infoProduto": "132dsadw313",
        "numeroPedido": "ABC12345"
    }

    order_status_chain_result = order_status_chain.invoke({"order_number": state["numeroPedido"], "order_information": state["infoProduto"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})


    assert isinstance(order_status_chain_result, AIMessage)
    assert order_status_chain_result.tool_calls and order_status_chain_result.tool_calls[0]["name"] == "check_status"


    
def test_order_status_node_with_final_response():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "infoProduto": "132dsadw313",
        "numeroPedido": "ABC12345"
    }

    updated_state = order_status_node(state)

    print("Primeiro State:", updated_state)

    updated_state2 = execute_tool_node(updated_state)

    print("Segundo State:", updated_state2)

    updated_state_final_response = order_status_node(updated_state2)

    print("State Final:", updated_state_final_response)

    assert isinstance(updated_state_final_response["conversation"][-1], AIMessage)

    



