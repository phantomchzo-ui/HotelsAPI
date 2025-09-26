from email.message import EmailMessage

from app.config import settings


def create_confirmation(email_to: str):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = settings.GM_USER
    email["To"] = email_to
    email.set_content(
        f"""
        <h1>Booking confirmation</h1>
        <p>Your booking details:</p>
        """,
        subtype="html"
    )
    return email