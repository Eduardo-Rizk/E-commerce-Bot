from enum import Enum

class Intent(Enum):
    EXCHANGE = "exchange"
    ORDER_STATUS = "order_status"
    PRODUCT_INFO = "product_info"
    GENERIC = "generic"


class status(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    IN_TRANSIT = "in_transit"
    CANCELLED = "cancelled"
    
