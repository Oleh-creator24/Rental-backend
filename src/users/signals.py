from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.conf import settings
from config.logging_setup import logger


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_user_group(sender, instance, created, **kwargs):
    """
    Автоматически добавляет нового пользователя в группу Guest,
    если он не принадлежит ни к одной из существующих (Tenant/Landlord/Guest).
    """
    if created:
        if not instance.groups.exists():
            guest_group, _ = Group.objects.get_or_create(name="Guest")
            instance.groups.add(guest_group)
            logger.info(f"[USERS] 👤 User '{instance.username}' added to group 'Guest'")
        else:
            groups = list(instance.groups.values_list('name', flat=True))
            logger.info(f"[USERS] 👥 User '{instance.username}' created with groups: {groups}")
