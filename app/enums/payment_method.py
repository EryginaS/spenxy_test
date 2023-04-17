from enum import Enum


class PaymentMethodEnum(str, Enum):
    """Способы оплаты"""

    CASH = 'cash'
    CASHLESS = 'cashless'
