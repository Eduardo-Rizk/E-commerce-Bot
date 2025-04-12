from langchain_core.tools import tool

from graph.consts import status

@tool
def check_status(number_of_order: str) -> status:
    """
    Check the status of an order based on the order number provided.
    Args:
        number_of_order (str): The order number to check the status of.
    """
    if number_of_order == "ABC12345":
        return status.DELIVERED
    

