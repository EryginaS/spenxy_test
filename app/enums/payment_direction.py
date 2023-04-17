from enum import Enum


class PaymentDirectionEnum(str, Enum):
    """Направление платежа"""

    INCOME = 'income'
    OUTCOME = 'outcome'
