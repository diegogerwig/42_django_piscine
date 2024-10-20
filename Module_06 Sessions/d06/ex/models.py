from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)
    can_downvote_by_reputation = models.BooleanField(default=False)
    can_delete_by_reputation = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote tips from other users"),
            ("can_delete", "Can delete tips from other users"),
        ]

    def can_downvote(self):
        return self.has_perm('ex.can_downvote') or self.can_downvote_by_reputation

    def can_delete(self):
        return self.has_perm('ex.can_delete') or self.can_delete_by_reputation

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(CustomUser, related_name='upvoted_tips')
    downvote = models.ManyToManyField(CustomUser, related_name='downvoted_tips')

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username}"

