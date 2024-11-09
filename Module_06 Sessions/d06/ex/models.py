from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomGroup(Group):
    manual_can_downvote = models.BooleanField(default=False, verbose_name="Can Downvote (Group)")
    manual_can_delete = models.BooleanField(default=False, verbose_name="Can Delete (Group)")

    class Meta:
        verbose_name = 'Custom Group'
        verbose_name_plural = 'Custom Groups'

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

    def get_group_permissions_status(self):
        """Obtiene los permisos de los grupos del usuario"""
        can_downvote = False
        can_delete = False
        for group in self.groups.all():
            try:
                custom_group = CustomGroup.objects.get(id=group.id)
                if custom_group.manual_can_downvote:
                    can_downvote = True
                if custom_group.manual_can_delete:
                    can_delete = True
            except CustomGroup.DoesNotExist:
                continue
        return can_downvote, can_delete

    def can_downvote(self):
        group_can_downvote, _ = self.get_group_permissions_status()
        return (self.has_perm('ex.can_downvote') or 
                self.can_downvote_by_reputation or 
                self.manual_can_downvote or 
                group_can_downvote)

    def can_delete(self):
        _, group_can_delete = self.get_group_permissions_status()
        return (self.has_perm('ex.can_delete') or 
                self.can_delete_by_reputation or 
                self.manual_can_delete or
                group_can_delete)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name='upvoted_tips')
    downvote = models.ManyToManyField(User, related_name='downvoted_tips')

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username}"

