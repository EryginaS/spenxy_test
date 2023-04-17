from datetime import datetime
from typing import Optional

from app.models.utils import ApiModel


class ActivityAccountingFilter(ApiModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_email: Optional[str] = None
    admin: Optional[bool] = None
    status: Optional[str] = None
    type: Optional[str] = None
    original_id: Optional[int] = None
