from enum import Enum

class Intent(Enum):
    EXCHANGE = "exchange"
    ORDER_STATUS = "order_status"
    PRODUCT_INFO = "product_info"
    GENERIC = "generic"
