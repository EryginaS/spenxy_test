from enum import Enum


class OperationStatusEnum(str, Enum):
    """Статусы операций"""

    SUCCESS = 'success'
    FAILED = 'failed'
