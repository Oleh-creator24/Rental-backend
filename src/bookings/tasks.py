from celery import shared_task
from django.core.mail import send_mail
from config.logging_setup import logger


@shared_task
def send_booking_email(to_email, subject, message):
    """Отправка уведомления арендатору о статусе брони."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[to_email],
            fail_silently=False,
        )
        logger.info(f"[EMAIL]  Email sent to {to_email} — {subject}")
    except Exception as e:
        logger.error(f"[EMAIL]  Failed to send to {to_email}: {e}")
