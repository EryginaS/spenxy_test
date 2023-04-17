from fastapi import BackgroundTasks, Depends, HTTPException, Response

from app.db.activity_accounting import ActivityAccounting
from app.models.activity_accounting import ActivityAccountingFilter
from app.service.background.report import ReportBackgroundService


class ReportApiService:
    _activity_accounting: ActivityAccounting
    _report_background_service: ReportBackgroundService

    def __init__(
        self,
        activity_accounting: ActivityAccounting = Depends(ActivityAccounting),
        report_background_service: ReportBackgroundService = Depends(ReportBackgroundService),
    ) -> None:
        self._activity_accounting = activity_accounting
        self._report_background_service = report_background_service

    async def get_report(
        self, filter_form: ActivityAccountingFilter, recipient: str, background_tasks: BackgroundTasks
    ) -> Response:
        await self._check_email(recipient)
        # run background task or celery task
        background_tasks.add_task(self._report_background_service.create_report_background_task, filter_form, recipient)
        return Response(201)

    async def _check_email(self, email: str) -> None:
        user = await self._activity_accounting.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail='User with this email does not exist')
