import json
from langchain_core.tools import tool

@tool
def fallback_notification(product_info: str,conversation_summary: str,reason_contact_support: str) -> str:
    """
    Notifies a human agent about the customer's needs.
    
    This tool receives:
      - product_info: Info about the product involved
      - conversation_summary: A summary of the conversation so far
      - reason_contact_support: Reason the customer is contacting support

    It organizes all of this in a JSON-like structure and (conceptually) sends it 
    to a human agent or support system. Returns a success message for confirmation.
    
    Args:
        product_info (str): The product information.
        conversation_summary (str): Summary of the conversation so far.
        reason_contact_support (str): Reason the customer is contacting support.

    Returns:
        str: A confirmation message indicating the agent was notified.
    """

    # Simulate sending the data to a human agent or support system
    data_to_notify = {
        "product_info": product_info,
        "conversation_summary": conversation_summary,
        "reason_contact_support": reason_contact_support
    }


    return (
        "Human agent has been notified successfully!\n"
        f"Payload:\n{json.dumps(data_to_notify, ensure_ascii=False, indent=2)}"
    )
