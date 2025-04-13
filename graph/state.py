from typing import List, TypedDict,Dict, Annotated
from langchain_core.messages import BaseMessage
from graph.consts import Intent
from langgraph.graph.message import add_messages



class GraphState(TypedDict):
    """State of the graph.

        conversation : List[BaseMessage] : List of the current conversation
        intention: str: Intention of the graph.
        result: str: Result of the graph.

    """

    conversation : Annotated[List[BaseMessage], add_messages]
    intention: Intent
    historical_conversation: List[BaseMessage]
    captured_histoical_conversation: bool
    product_info: str
    order_number: str
    catalog_store: str

    



