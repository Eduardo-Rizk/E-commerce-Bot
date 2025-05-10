from dotenv import load_dotenv

load_dotenv()


import graph.chain.tools.helper.fetch_conversation_from_json as fetch_conversation
import os 
import pytest
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage
from graph.chain.intention_chain import GradedIntention, intetion_grader
from graph.consts import Intent
from graph.state import GraphState
from graph.nodes.help_active_order import help_active_order



from graph.nodes.execute_tool_node import execute_tool_node


from graph.chain.order_status_chain import order_status_chain

from graph.nodes.tool_call_order_status import order_status_tool_call

from graph.nodes.seller_node import seller_node

from graph.nodes.fallback_node import fallback_node


def test_intention():


    conversation_mock: list[BaseMessage] = [
        HumanMessage(content="Olá, tudo bem? Comprei um produto há duas semanas e não chegou ainda."),
        AIMessage(content="Entendi! Pode me fornecer o número do seu pedido, por favor?"),
        HumanMessage(content="Claro, o número do meu pedido é #98765. Consegue me dizer onde ele está agora?")
    ]
    
    result = intetion_grader.invoke({"conversation": conversation_mock})
    

    assert result.intention == Intent.ORDER_STATUS, f"Esperado: {Intent.ORDER_STATUS}, obtido: {result.intention}"


def test_help_active_order_should_ask_for_order_number():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "order_info": "",
        "order_number": False,
        "catalog_store": ""
    }

    updated_state = help_active_order(state)


    print("AI PERGUNTANDO O NUMERO DO PEDIDO: ", updated_state["conversation"][-1])

    
    assert isinstance(updated_state["conversation"][-1], AIMessage)




def test_order_status_chain_toolCall_orderStatus():
    state: GraphState = {
        "conversation": [
            HumanMessage(content="Oi, gostaria de saber onde está meu pedido."),
            AIMessage(content="Claro! Pode me informar o número do pedido?"),
            HumanMessage(content="Sim, é o pedido ABC12345.")
        ],
        "intention": Intent.ORDER_STATUS,
        "historical_conversation": [],
        "captured_histoical_conversation": False,
        "order_info": "132dsadw313",
        "order_number": True,
        "catalog_store": ""
    }

    order_status_chain_result = order_status_chain.invoke({"order_number": state["order_number"], "order_information": state["order_info"], "conversation": state["conversation"],"historical_conversation": state["historical_conversation"]})


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
        "order_info": "",
        "order_number": "",
        "catalog_store": ""
    }

    result = seller_node(state)
    tool_call = result["conversation"][-1] 




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
        "order_info": "",
        "order_number": "",
        "catalog_store": ""
    }

    updated_state = execute_tool_node(state)
    last_message = updated_state["conversation"][-1]



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
        "order_info": "",
        "order_number": "",
        "catalog_store": '{"products":[{"name":"Camiseta","price":59.9}]}'
    }

    result = seller_node(state)
    last_message = result["conversation"][-1]



    assert isinstance(last_message, AIMessage)
    assert "Camiseta" in last_message.content




# Teste para verificar o fluxo completo de execução do nó de Fallback

def test_fallback_node_with_cancellation_asks_the_reason():
    # Simula a conversa onde o cliente já forneceu número do pedido e quer cancelar
    conversation_mock: list[BaseMessage] = [
        HumanMessage(content="Olá, estou com um problema no meu pedido."),
        AIMessage(content="Claro! Pode me informar o número do pedido?"),
        HumanMessage(content="Sim, é o pedido #98765."),
        AIMessage(content="Obrigado. Como posso te ajudar com esse pedido?"),
        HumanMessage(content="Eu gostaria de cancelar o pedido."),
    ]

    state: GraphState = {
        "conversation": conversation_mock,
        "intention": Intent.CANCEL, 
        "historical_conversation": [],
        "captured_histoical_conversation": True,
        "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
        "order_number": "98765",
        "catalog_store": ""
    }

    result = fallback_node(state)


    print("Last message: Resposta da AI", result["conversation"][-1])
    assert isinstance(result["conversation"][-1], AIMessage)
    




def test_fallback_node_with_cancellation_calls_tool():
    conversation_mock: list[BaseMessage] = [
        HumanMessage(content="Olá, estou com um problema no meu pedido."),
        AIMessage(content="Claro! Pode me informar o número do pedido?"),
        HumanMessage(content="Sim, é o pedido #98765."),
        AIMessage(content="Obrigado. Como posso te ajudar com esse pedido?"),
        HumanMessage(content="Eu gostaria de cancelar o pedido."),
        AIMessage(content="Entendo. Pode me dizer o motivo do cancelamento?"),
        HumanMessage(content="Porque demorou muito para chegar e não preciso mais.")
    ]

    state: GraphState = {
        "conversation": conversation_mock,
        "intention": Intent.CANCEL, 
        "historical_conversation": [],
        "captured_histoical_conversation": True,
        "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
        "order_number": "98765",
        "catalog_store": ""
    }

    result = fallback_node(state)

    print("Last message: Resposta da AI", result["conversation"][-1])
    assert isinstance(result["conversation"][-1], AIMessage)


    from graph.chain.tools.fallback_notification import fallback_notification

def test_fallback_notification_tool_response():
    conversation_mock = [HumanMessage(content="Olá, estou com um problema no meu pedido."),
        AIMessage(content="Claro! Pode me informar o número do pedido?"),
        HumanMessage(content="Sim, é o pedido #98765."),
        AIMessage(content="Obrigado. Como posso te ajudar com esse pedido?"),
        HumanMessage(content="Eu gostaria de cancelar o pedido."),
        AIMessage(content="Entendo. Pode me dizer o motivo do cancelamento?"),
        HumanMessage(content="Porque demorou muito para chegar e não preciso mais."),

        AIMessage(
        content="",
        tool_calls=[
            {
                "name": "fallback_notification",
                "args": {
                    "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
                    "conversation_summary": (
                        "O cliente informou que gostaria de cancelar o pedido #98765 "
                        "porque demorou muito para chegar e não precisa mais."
                    ),
                    "reason_contact_support": "Cancelamento do pedido devido à demora na entrega."
                },
                "id": "call_123",
                "type": "tool_call"
            }])]
    
    state: GraphState = {
        "conversation": conversation_mock,
        "intention": Intent.CANCEL, 
        "historical_conversation": [],
        "captured_histoical_conversation": True,
        "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
        "order_number": "98765",
        "catalog_store": ""
    }

    updated_state = execute_tool_node(state)
    last_message = updated_state["conversation"][-1]
    print("Last message: Resposta da AI", last_message)
    print("Toda a conversa: Resposta da AI", updated_state["conversation"])

    assert isinstance(last_message, ToolMessage)
    assert last_message.name == "fallback_notification"


def test_fallback_notification_final_response():
    conversation_mock = [HumanMessage(content="Olá, estou com um problema no meu pedido."),
    AIMessage(content="Claro! Pode me informar o número do pedido?"),
    HumanMessage(content="Sim, é o pedido #98765."),
    AIMessage(content="Obrigado. Como posso te ajudar com esse pedido?"),
    HumanMessage(content="Eu gostaria de cancelar o pedido."),
    AIMessage(content="Entendo. Pode me dizer o motivo do cancelamento?"),
    HumanMessage(content="Porque demorou muito para chegar e não preciso mais."),

    AIMessage(
    content="",
    tool_calls=[
        {
            "name": "fallback_notification",
            "args": {
                "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
                "conversation_summary": (
                    "O cliente informou que gostaria de cancelar o pedido #98765 "
                    "porque demorou muito para chegar e não precisa mais."
                ),
                "reason_contact_support": "Cancelamento do pedido devido à demora na entrega."
            },
            "id": "call_123",
            "type": "tool_call"
        }]),
    
    ToolMessage(content='Human agent has been notified successfully!\nPayload:\n{\n  "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",\n  "conversation_summary": "O cliente informou que gostaria de cancelar o pedido #98765 porque demorou muito para chegar e não precisa mais.",\n  "reason_contact_support": "Cancelamento do pedido devido à demora na entrega."\n}', name='fallback_notification', tool_call_id='call_123')]


    state: GraphState = {
        "conversation": conversation_mock,
        "intention": Intent.CANCEL, 
        "historical_conversation": [],
        "captured_histoical_conversation": True,
        "order_info": "Pedido #98765: Camiseta Básica, cor branca, tamanho M.",
        "order_number": "98765",
        "catalog_store": ""
    }

    result = fallback_node(state)
    

    print("Last message: Resposta da AI", result)

    assert isinstance(result["conversation"][-1], AIMessage)












