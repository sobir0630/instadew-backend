from django.db.models.signals import post_delete, post_save
from django.db.models import F
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from follows.models import Follow


User = get_user_model()

# FOLLOW
@receiver(post_save, sender=Follow)
def increase_follow(sender, instance, created, **kwargs):
    if created:
        follower = instance.follower      # follow qilgan (Alijon)
        following = instance.following    # follow qilingan (Sobir)

        # Alijon kimnidir follow qildi
        follower.following_count += 1
        follower.save()

        # Sobirni followerlari oshdi
        following.followers_count += 1
        following.save()


# UNFOLLOW
@receiver(post_delete, sender=Follow)
def decrease_follow(sender, instance, **kwargs):
    follower = instance.follower
    following = instance.following

    follower.following_count = max(0, follower.following_count - 1)
    follower.save()

    following.followers_count = max(0, following.followers_count - 1)
    following.save()

    print("Follower:", follower.username)
    print("Following:", following.username)