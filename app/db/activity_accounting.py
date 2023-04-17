from __future__ import annotations

import uuid

from fastapi import Depends
from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, Float, String, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base, get_session
from app.enums import (
    OperationStatusEnum,
    PaymentDirectionEnum,
    PaymentMethodEnum,
    ProductsEnum,
    TransactionAmountTypeEnum,
    TransactionNameEnum,
    TransactionTypeEnum,
)
from app.models.activity_accounting import ActivityAccountingFilter


class ActivityAccounting(Base):
    __tablename__ = "activity_accounting"

    # general specifications
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    admin = Column(String, nullable=True, index=True)
    user = Column(String, nullable=False, index=True)
    user_email = Column(String, nullable=True, index=True)
    wallet = Column(String, nullable=False, index=True)
    original_id = Column(String, nullable=True, index=True)
    type = Column(Enum(TransactionNameEnum), nullable=False)
    product = Column(Enum(ProductsEnum), nullable=False)
    status = Column(Enum(OperationStatusEnum), nullable=True)
    level = Column(Enum(TransactionTypeEnum), nullable=False)
    method = Column(Enum(PaymentMethodEnum), nullable=True)
    direction = Column(Enum(PaymentDirectionEnum), nullable=True)
    amount = Column(Float, nullable=False, server_default="0")
    billing_amount = Column(Float, nullable=True)
    currency = Column(String, nullable=False, server_default="USD")
    billing_currency = Column(String, nullable=True)
    amount_type = Column(Enum(TransactionAmountTypeEnum), nullable=False)
    description = Column(String, nullable=False)

    # balances specifications
    total_balance_debit = Column(Float, nullable=True)
    total_balance_credit = Column(Float, nullable=True)
    available_balance_debit = Column(Float, nullable=True)
    available_balance_credit = Column(Float, nullable=True)
    reserved_balance_debit = Column(Float, nullable=True)
    reserved_balance_credit = Column(Float, nullable=True)

    # wallet balances specifications
    total_balance = Column(Float, nullable=False, server_default="0")
    available_balance = Column(Float, nullable=False, server_default="0")
    reserved_balance = Column(Float, nullable=False, server_default="0")
    total_deposit = Column(Float, nullable=False, server_default="0")
    incoming_balance = Column(Float, nullable=False, server_default="0")
    pending_balance = Column(Float, nullable=False, server_default="0")
    total_spend = Column(Float, nullable=False, server_default="0")
    total_fee = Column(Float, nullable=False, server_default="0")
    return_balance = Column(Float, nullable=False, server_default="0")
    decline_balance = Column(Float, nullable=False, server_default="0")
    rolling_balance = Column(Float, nullable=False, server_default="0")

    # card specifications
    card = Column(String, nullable=True, index=True)
    card_memo = Column(String, nullable=True, index=True)
    bank_card_memo = Column(String, nullable=True)
    card_number = Column(String, nullable=True)
    card_opening_balance = Column(Float, nullable=True)
    card_topup_balance = Column(Float, nullable=True)
    card_available_balance = Column(Float, nullable=True)
    card_pending_balance = Column(Float, nullable=True)
    card_incoming_balance = Column(Float, nullable=True)
    card_withdrawal_balance = Column(Float, nullable=True)
    card_spend = Column(Float, nullable=True)
    card_fees = Column(Float, nullable=True)

    # control
    turnover_control = Column(Boolean, nullable=True)
    balances_control = Column(Boolean, nullable=False)
    cards_control = Column(Boolean, nullable=True)

    async def filter_by_options(
        self, form_filter: ActivityAccountingFilter, db_session: AsyncSession = Depends(get_session)
    ) -> list[ActivityAccounting]:
        query = await db_session.query(ActivityAccounting)

        for field, value in form_filter:
            if value is not None:
                query = _filter_operations[field](query, value)
        return query.order_by(ActivityAccounting.date.desc()).all()

    async def get_by_email(
        self, email: str, db_session: AsyncSession = Depends(get_session)
    ) -> list[ActivityAccounting]:
        return await db_session.query(ActivityAccounting).filter(ActivityAccounting.user_email == email).all()


_filter_operations = {
    'start_date': lambda query, value: query.filter(ActivityAccounting.date >= value),
    'end_date': lambda query, value: query.filter(ActivityAccounting.date <= value),
    'user_email': lambda query, value: query.filter(ActivityAccounting.user_email == value),
    'admin': lambda query, value: query.filter(ActivityAccounting.admin == value),
    'status': lambda query, value: query.filter(ActivityAccounting.status == value),
    'type': lambda query, value: query.filter(ActivityAccounting.type == value),
    'original_id': lambda query, value: query.filter(ActivityAccounting.original_id == value),
}
