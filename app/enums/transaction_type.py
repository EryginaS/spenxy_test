from enum import Enum


class TransactionTypeEnum(str, Enum):
    """Типы транзакций"""

    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
