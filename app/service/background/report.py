import io
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from fastapi import Depends

from app import settings
from app.db.activity_accounting import ActivityAccounting
from app.external.external_facade import ExternalFacade
from app.models.activity_accounting import ActivityAccountingFilter


class ReportBackgroundService:
    """
    This class only for demonstration, because we need async boto3, async smtp client and etc.
    Also we can use temp dir for saving excel file, but I am tired)
    Of course we need to template for our message and may be it's better to use celery for background tasks
    And build message  is other service which needs to be in Depends
    """
    _external_facade: ExternalFacade
    _activity_accounting: ActivityAccounting
    s3_bucket = settings.AWS_S3_BUCKET_NAME
    s3_folder = settings.AWS_S3_FOLDER
    s3_key = settings.AWS_S3_KEY

    def __init__(
        self,
        external_facade: ExternalFacade = Depends(ExternalFacade),
        activity_accounting: ActivityAccounting = Depends(ActivityAccounting),
    ) -> None:
        self._activity_accounting = activity_accounting
        self._external_facade = external_facade

    async def create_report_background_task(self, filter_form: ActivityAccountingFilter, recipient: str) -> None:
        query_results = await self._activity_accounting.get_activity_accounting_by_filter(filter_form)
        excel_file = await self._create_report(query_results)
        await self._external_facade.create_file_in_s3(excel_file, os.path.join(self.s3_folder, self.s3_key))
        message = await self._build_message(recipient, excel_file)
        await self._external_facade.send_email_to_user(message)

    async def _create_report(self, query_results: list[ActivityAccounting]) -> io.BytesIO:
        df = pd.DataFrame(query_results)
        excel_file = io.BytesIO()
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=settings.SHEET_NAME, index=False)
        writer.save()
        excel_file.seek(0)
        return excel_file

    async def _build_message(self, recipient: str, content: bytes) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg['From'] = settings.CORPARATION_EMAIL
        msg['To'] = recipient
        msg['Subject'] = 'Отчет по выборке'
        body = 'Отчет доступен по ссылке: https://{0}.s3.amazonaws.com/{1}/{2}'.format(
            self.s3_bucket, self.s3_folder, self.s3_key
        )
        msg.attach(MIMEText(body, 'plain'))
        attachment = MIMEApplication(content, _subtype='xlsx')
        attachment.add_header('content-disposition', 'attachment', filename='report.xlsx')
        msg.attach(attachment)
        return msg
