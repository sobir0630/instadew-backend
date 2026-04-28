from django.db.models.signals import post_delete, post_save
from django.db.models import F
from django.dispatch import receiver
from posts.models import Post
from comments.models import Comment


@receiver(post_save, sender=Comment)
def increase_comment_count(sender, instance, created, **kwargs):
    if created:
        Post.objects.filter(id=instance.post.id).update(
            comments_count=F("comments_count") + 1
        )


@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    Post.objects.filter(id=instance.post.id).update(
        comments_count=F("comments_count") - 1
    )