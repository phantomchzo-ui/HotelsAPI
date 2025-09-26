
import smtplib
from pathlib import Path

from PIL import Image

from app.config import settings
from app.tasks.email_templates import create_confirmation
from app.tasks.worker import celery


@celery.task
def process_picture(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000,500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")


@celery.task
def send_info_email(email_to: str):
    content = create_confirmation(email_to)

    with smtplib.SMTP_SSL(settings.GM_HOST, settings.GM_PORT) as server:
        server.login(settings.GM_USER, settings.GM_PASSWORD)
        server.send_message(content)


