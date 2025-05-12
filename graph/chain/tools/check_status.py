from langchain_core.tools import tool

from graph.consts import status

@tool
def check_status(order_number: str) -> str:
    """
    Check the status of an order based on the order number provided.
    Args:
        order_number (str): The order number to check the status of.
    """
    if order_number == "ABC12345":
        return f"O status do pedido {order_number} é: de {status.DELIVERED.value}"
    return f"O status do pedido {order_number} é: de {status.DELIVERED.value}"
    

