from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article


@receiver(post_save, sender=Article)
def notify_new_article(sender, instance, created, **kwargs):
    if created:
        from .tasks import send_article_notification
        send_article_notification(instance)
