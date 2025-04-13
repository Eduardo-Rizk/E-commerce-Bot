from dotenv import load_dotenv

load_dotenv()


import graph.chain.tools.helper.fetch_conversation_from_json as fetch_conversation
import os 
import pytest
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage
from graph.chain.intention_chain import GradedIntention, intetion_grader
from graph.consts import Intent
from graph.state import GraphState
from graph.nodes.help_atctive_order import help_active_order



from graph.nodes.execute_tool_node import execute_tool_node


from graph.chain.order_status_chain import order_status_chain

from graph.nodes.order_status import order_status_node

from graph.nodes.seller_node import seller_node


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
        "product_info": "",
        "order_number": ""
    }

    updated_state = help_active_order(state)



    # Verifica se a mensagem da AI foi adicionada
    assert isinstance(updated_state["conversation"][-1], AIMessage)

def test_help_active_order_product_info_filled():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "product_info": "132dsadw313",
        "order_number": "123456789"
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
        "product_info": "132dsadw313",
        "order_number": "ABC12345"
    }

    order_status_chain_result = order_status_chain.invoke({"order_number": state["order_number"], "order_information": state["product_info"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})


    assert isinstance(order_status_chain_result, AIMessage)
    assert order_status_chain_result.tool_calls and order_status_chain_result.tool_calls[0]["name"] == "check_status"



# Teste para verificar o fluxo completo de execução do nó de SELLER
# São os 3 testes abaixo



def test_seller_node_tool_call_created():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber quais produtos vocês vendem.")
        ],
        "intention": Intent.PRODUCT_INFO,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "product_info": "",
        "order_number": "",
        "catalog_store": ""
    }

    result = seller_node(state)
    tool_call = result["conversation"][-1] 



    print("Tool call: ", tool_call)



    assert hasattr(tool_call, "tool_calls")
    assert tool_call.tool_calls[0]["name"] == "fetch_catalog"

def test_execute_tool_node_returns_tool_message():

    tool_call_message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "fetch_catalog",
                "args": {},
                "id": "call_123",
                "type": "tool_call"
            }
        ]
    )

    state: GraphState = {
        "conversation": [tool_call_message],
        "intention": Intent.PRODUCT_INFO,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "product_info": "",
        "order_number": "",
        "catalog_store": ""
    }

    updated_state = execute_tool_node(state)
    last_message = updated_state["conversation"][-1]

    print("Last message: Respota da tool", last_message)


    assert isinstance(last_message, ToolMessage)
    assert last_message.name == "fetch_catalog"




def test_seller_node_final_response_after_tool():
    tool_result = ToolMessage(
        content='{"products":[{"name":"Camiseta","price":59.9}]}',
        name="fetch_catalog",
        tool_call_id="call_123"
    )

    state: GraphState = {
        "conversation": [tool_result],
        "intention": Intent.PRODUCT_INFO,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "product_info": "",
        "order_number": "",
        "catalog_store": '{"products":[{"name":"Camiseta","price":59.9}]}'
    }

    result = seller_node(state)
    last_message = result["conversation"][-1]

    print("Last message: Reposta da AI", last_message)


    assert isinstance(last_message, AIMessage)
    assert "Camiseta" in last_message.content







    



