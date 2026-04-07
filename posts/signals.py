from django.db.models.signals import post_delete, post_save
from django.db.models import F
from django.dispatch import receiver
from posts.models import Post


@receiver(post_save, sender=Post)
def increase_post_count(sender, instance, created, **kwargs):
    if created:
        instance.user.posts_count = F("posts_count") + 1
        instance.user.save()


@receiver(post_delete, sender=Post)
def decrease_post_count(sender, instance, **kwargs):
    if instance.user.posts_count > 0:
        instance.user.posts_count = F("posts_count") - 1
        instance.user.save()