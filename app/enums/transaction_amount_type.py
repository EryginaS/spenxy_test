from enum import Enum


class TransactionAmountTypeEnum(str, Enum):
    """Тип суммы транзакции"""

    AMOUNT = 'amount'
    FEE = 'fee'
    COMMISSION = 'commission'
    TAX = 'tax'
    DISCOUNT = 'discount'
    BONUS = 'bonus'
    CREDIT = 'credit'
    DEPOSIT = 'deposit'
    CASHBACK = 'cashback'
