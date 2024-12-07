from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    class Meta:
        ordering = ['timestamp']

class UserStatus(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='status',
        primary_key=True
    )
    is_online = models.BooleanField(default=False)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'chat_userstatus'

    def __str__(self):
        return f"{self.user.username}'s status"

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    """Create UserStatus for new users only"""
    if created and not hasattr(instance, 'status'):
        UserStatus.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_status(sender, instance, **kwargs):
    if not hasattr(instance, 'status'):
        UserStatus.objects.create(user=instance)