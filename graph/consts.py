from enum import Enum

class Intent(Enum):
    EXCHANGE = "exchange"
    CANCEL = "cancelation"
    DEVOLUTION = "devolution"
    ORDER_STATUS = "order_status"
    PRODUCT_INFO = "product_info"
    GENERIC = "generic"


class status(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    IN_TRANSIT = "in_transit"
    CANCELLED = "cancelled"
    

RETRIEVE_HISTORICAL_CONVERSATION = "RETRIEVE_HISTORICAL_CONVERSATION"
INTENTION = "INTENTION"

EXECUTE_TOOL = "EXECUTE_TOOL"
HELP_ACTIVE_ORDER = "HELP_ACTIVE_ORDER"
LOAD_ORDER_INFO = "LOAD_ORDER_INFO"

FALLBACK_ANSWER = "FALLBACK_ANSWER"
FALLBACK_ASK_MOTIVATION = "FALLBACK_ASK_MOTIVATION"
ORDER_STATUS_ANSWER = "ORDER_STATUS_ANSWER"
ORDER_STATUS = "ORDER_STATUS"
FALLBACK = "FALLBACK"
SELLER = "SELLER"
SELLER_ANSWER = "SELLER_ANSWER"