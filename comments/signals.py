from django.db.models.signals import post_save, post_delete
from django.db.models import F
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from comments.models import Comments
from posts.models import Post
from video.models import Video


@receiver(post_save, sender=Comments)
def increase_comment_count(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.content_type == ContentType.objects.get_for_model(Post):
        Post.objects.filter(id=instance.object_id).update(
            comments_count=F("comments_count") + 1
        )

    elif instance.content_type == ContentType.objects.get_for_model(Video):
        Video.objects.filter(id=instance.object_id).update(
            comments_count=F("comments_count") + 1
        )


@receiver(post_delete, sender=Comments)
def decrease_comment_count(sender, instance, **kwargs):

    if instance.content_type == ContentType.objects.get_for_model(Post):
        Post.objects.filter(id=instance.object_id).update(
            comments_count=F("comments_count") - 1
        )

    elif instance.content_type == ContentType.objects.get_for_model(Video):
        Video.objects.filter(id=instance.object_id).update(
            comments_count=F("comments_count") - 1
        )