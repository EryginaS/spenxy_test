from abc import abstractmethod
from email.mime.multipart import MIMEMultipart


class ExternalInterface:
    """Взаимодействие с внешними сервисами"""

    @abstractmethod
    async def create_file_in_s3(self, content: bytes, file_name: str) -> bytes:
        """Создание файла в S3 хранилище"""

    @abstractmethod
    async def send_email_to_user(self, message: MIMEMultipart) -> None:
        """Отправка письма пользователю"""
