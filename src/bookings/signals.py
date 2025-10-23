from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from config.logging_setup import logger
from .models import Booking


def _get_tenant(booking: Booking):
    """
    Унифицированно достаём арендатора:
    поддерживает booking.user и booking.tenant.
    """
    tenant = getattr(booking, "tenant", None)
    if tenant is None:
        tenant = getattr(booking, "user", None)
    return tenant


def _send(to_email: str | None, subject: str, message: str):
    """
    Безопасная отправка письма с логированием.
    """
    if not to_email:
        logger.warning(f"[EMAIL] Пропуск отправки: пустой email получателя. subject='{subject}'")
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER),
        recipient_list=[to_email],
        fail_silently=False,
    )
    logger.info(f"[EMAIL] ✔ '{subject}' -> {to_email}")


@receiver(post_save, sender=Booking)
def booking_email_notifications(sender, instance: Booking, created: bool, **kwargs):
    """
    Уведомления по email:
    - created=True: арендатору (создано) + арендодателю (новая бронь)
    - created=False: по изменению статуса – обеим сторонам
    """
    try:
        tenant = _get_tenant(instance)
        tenant_email = getattr(tenant, "email", None) if tenant else None

        listing = instance.listing
        owner = getattr(listing, "owner", None)
        owner_email = getattr(owner, "email", None) if owner else None


        if created:
            # Арендатору
            _send(
                tenant_email,
                subject=" Бронирование создано",
                message=(
                    f"Здравствуйте, {getattr(tenant, 'username', 'пользователь')}!\n\n"
                    f"Вы забронировали объект «{listing.title}» "
                    f"на даты {instance.start_date} — {instance.end_date}.\n"
                    f"Статус: {instance.status}.\n"
                    f"Ожидайте подтверждения арендодателя."
                ),
            )
            # Арендодателю
            _send(
                owner_email,
                subject=" Новое бронирование вашего объекта",
                message=(
                    f"Здравствуйте, {getattr(owner, 'username', 'арендодатель')}!\n\n"
                    f"Поступила новая бронь на «{listing.title}» "
                    f"от {getattr(tenant, 'username', 'пользователя')}.\n"
                    f"Даты: {instance.start_date} — {instance.end_date}.\n"
                    f"Текущий статус: {instance.status}."
                ),
            )
            return

        # ----- при изменении существующей брони (по статусу) -----


        status = instance.status

        if status == "approved":
            # Арендатору
            _send(
                tenant_email,
                subject=" Бронирование подтверждено",
                message=(
                    f"Здравствуйте, {getattr(tenant, 'username', 'пользователь')}!\n\n"
                    f"Ваше бронирование «{listing.title}» подтверждено.\n"
                    f"Даты: {instance.start_date} — {instance.end_date}."
                ),
            )
            # Арендодателю
            _send(
                owner_email,
                subject=" Вы подтвердили бронирование",
                message=(
                    f"Здравствуйте, {getattr(owner, 'username', 'арендодатель')}!\n\n"
                    f"Вы подтвердили бронирование «{listing.title}» "
                    f"для {getattr(tenant, 'username', 'пользователя')}.\n"
                    f"Даты: {instance.start_date} — {instance.end_date}."
                ),
            )

        elif status == "rejected":
            _send(
                tenant_email,
                subject=" Бронирование отклонено",
                message=(
                    f"Здравствуйте, {getattr(tenant, 'username', 'пользователь')}!\n\n"
                    f"К сожалению, бронирование «{listing.title}» отклонено.\n"
                    f"Даты: {instance.start_date} — {instance.end_date}."
                ),
            )
            _send(
                owner_email,
                subject=" Вы отклонили бронирование",
                message=(
                    f"Здравствуйте, {getattr(owner, 'username', 'арендодатель')}!\n\n"
                    f"Вы отклонили бронирование «{listing.title}» "
                    f"для {getattr(tenant, 'username', 'пользователя')}.\n"
                    f"Даты: {instance.start_date} — {instance.end_date}."
                ),
            )

        elif status == "canceled":
            _send(
                tenant_email,
                subject=" Бронирование отменено",
                message=(
                    f"Здравствуйте, {getattr(tenant, 'username', 'пользователь')}!\n\n"
                    f"Ваше бронирование «{listing.title}» отменено."
                ),
            )
            _send(
                owner_email,
                subject=" Бронирование отменено пользователем",
                message=(
                    f"Здравствуйте, {getattr(owner, 'username', 'арендодатель')}!\n\n"
                    f"Бронирование «{listing.title}» было отменено "
                    f"{getattr(tenant, 'username', 'пользователем')}."
                ),
            )

        # Для прочих статусов письма не шлём
    except Exception as e:
        logger.error(f"[BOOKINGS][EMAIL] Ошибка при обработке сигнала: {e}", exc_info=True)

@receiver(post_save, sender=Booking)
def handle_booking_status(sender, instance, created, **kwargs):
    """При подтверждении бронирования — отклонить все остальные заявки на тот же объект."""
    if instance.status == "approved":
        # Отклоняем все остальные pending-бронирования для того же объявления
        other_bookings = Booking.objects.filter(
            listing=instance.listing,
            status="pending"
        ).exclude(id=instance.id)

        for booking in other_bookings:
            booking.status = "rejected"
            booking.save()

            # Отправляем уведомление об отклонении
            send_mail(
                "Ваше бронирование отклонено",
                f"К сожалению, объект '{instance.listing.title}' уже забронирован другим пользователем.",
                settings.DEFAULT_FROM_EMAIL,
                [booking.tenant.email],
                fail_silently=True,
            )