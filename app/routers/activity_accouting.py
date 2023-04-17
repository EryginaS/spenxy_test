from fastapi import BackgroundTasks, Body, Depends, Response
from fastapi.routing import APIRouter

from app.models.activity_accounting import ActivityAccountingFilter
from app.service.api.report import ReportApiService

router = APIRouter()


@router.post(
    "/generate-report/{email: EmailStr}",
    status_code=201,
    response_description="Report generation started",
)
async def generate_report_endpoint(
    email: str,
    background_tasks: BackgroundTasks,
    report_api_service: ReportApiService = Depends(ReportApiService),
    filter_form: ActivityAccountingFilter = Body(...),
) -> Response:
    return await report_api_service.get_report(
        filter_form=filter_form, recipient=email, background_tasks=background_tasks
    )
