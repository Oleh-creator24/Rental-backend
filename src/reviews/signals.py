from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from config.logging_setup import logger
from .models import Review
from listings.models import Listing


def update_listing_rating(listing):
    """Пересчитывает средний рейтинг объявления."""
    avg_rating = Review.objects.filter(listing=listing).aggregate(Avg("rating"))["rating__avg"]
    new_rating = round(avg_rating or 0, 2)
    listing.rating = new_rating
    listing.save(update_fields=["rating"])
    return new_rating


@receiver(post_save, sender=Review)
def update_rating_on_save(sender, instance, **kwargs):
    """После добавления или изменения отзыва."""
    new_rating = update_listing_rating(instance.listing)
    logger.info(
        f"[REVIEWS] ⭐ Review added/updated by {instance.user.username} "
        f"for '{instance.listing.title}'. New rating: {new_rating}"
    )


@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    """После удаления отзыва."""
    new_rating = update_listing_rating(instance.listing)
    logger.info(
        f"[REVIEWS] ❌ Review deleted for '{instance.listing.title}'. "
        f"New rating: {new_rating}"
    )
