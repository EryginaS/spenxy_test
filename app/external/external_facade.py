from email.mime.multipart import MIMEMultipart

from fastapi import Depends

from app.exceptions.send_email import SendEmailException
from app.exceptions.upload_file import S3SendFileException
from app.external.external_interface import ExternalInterface
from app.external.service.s3 import S3Service, get_s3_service
from app.external.service.smtp import SmtpService, get_smtp_service


class ExternalFacade(ExternalInterface):
    _s3_service: S3Service
    _smtp_service: SmtpService

    def __init__(
        self, s3_service: S3Service = Depends(get_s3_service), smtp_service: SmtpService = Depends(get_smtp_service)
    ) -> None:
        self._s3_service = s3_service
        self._smtp_service = smtp_service

    async def create_file_in_s3(self, content: bytes, file_name: str) -> None:
        try:
            return self._s3_service.upload_file(content=content, file_name=file_name)
        except S3SendFileException:
            """We need do something with it but now I have no idea what to do"""
            pass

    async def send_email_to_user(self, message: MIMEMultipart) -> None:
        try:
            return self._smtp_service.send(message=message)
        except SendEmailException:
            """Same)"""
            pass
