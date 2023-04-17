from enum import Enum


class TransactionNameEnum(str, Enum):
    """Название транзакции"""

    PAYMENT = 'payment'
    REFUND = 'refund'
