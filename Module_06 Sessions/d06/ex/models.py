from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    reputation = models.IntegerField(default=0)
    can_downvote_by_reputation = models.BooleanField(default=False)
    can_delete_by_reputation = models.BooleanField(default=False)
    manual_can_downvote = models.BooleanField(default=False, verbose_name="Can Downvote (Manual)")
    manual_can_delete = models.BooleanField(default=False, verbose_name="Can Delete (Manual)")

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote tips from other users"),
            ("can_delete", "Can delete tips from other users"),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def can_downvote(self):
        return (self.has_perm('ex.can_downvote') or 
                self.can_downvote_by_reputation or 
                self.manual_can_downvote)

    def can_delete(self):
        return (self.has_perm('ex.can_delete') or 
                self.can_delete_by_reputation or 
                self.manual_can_delete)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name='upvoted_tips')
    downvote = models.ManyToManyField(User, related_name='downvoted_tips')

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username}"

