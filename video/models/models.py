from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Video(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    video          = models.FileField(upload_to="videos/", blank=True, null=True)
    caption        = models.TextField(blank=True)
    likes_count    = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    location       = models.CharField(max_length=250, null=True, blank=True)
    tags           = models.CharField(max_length=250, null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    is_active      = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.caption[:20]}" 

class Like(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_likes")
    video      = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} liked {self.video}"