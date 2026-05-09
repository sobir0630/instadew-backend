from django.db.models.signals import post_save, post_delete
from django.db.models import F
from django.dispatch import receiver

from .models import Video, Like
from comments.models import Comments


@receiver(post_save, sender=Comments)
def increase_comments_count(sender, instance, created, **kwargs):
    if created:
        obj = instance.content_object

        if isinstance(obj, Video):
            Video.objects.filter(id=obj.id).update(comments_count=F("comments_count") + 1)

@receiver(post_delete, sender=Comments)
def decrease_comments_count(sender, instance, **kwargs):
    obj = instance.content_object

    if isinstance(obj, Video) and obj.comments_count > 0:
        Video.objects.filter(id=obj.id).update(comments_count=F("comments_count") - 1)
 

@receiver(post_save, sender=Like)
def increase_likes_count(sender, instance, created, **kwargs):
    if created:
        video = instance.video
        Video.objects.filter(id=video.id).update(likes_count=F("likes_count") + 1)

@receiver(post_delete, sender=Like) 
def decrease_likes_count(sender, instance, **kwargs):
    obj = instance

    if isinstance(obj, Video) and obj.likes_count > 0:
        Video.objects.filter(id=obj.id).update(likes_count=F("likes_count") - 1)
    