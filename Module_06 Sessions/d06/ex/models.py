from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def update_reputation(self):
        upvotes = sum(tip.upvote.count() for tip in self.tip_set.all())
        downvotes = sum(tip.downvote.count() for tip in self.tip_set.all())
        self.reputation = upvotes * 5 - downvotes * 2
        self.save()

    def can_downvote(self):
        return self.reputation >= 15 or self.has_perm('ex.can_downvote')

    def can_delete(self):
        return self.reputation >= 30 or self.has_perm('ex.can_delete')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_permissions()

    def update_user_permissions(self):
        content_type = ContentType.objects.get_for_model(Tip)
        can_downvote = Permission.objects.get(
            codename='can_downvote',
            content_type=content_type,
        )
        can_delete = Permission.objects.get(
            codename='can_delete',
            content_type=content_type,
        )
        
        if self.reputation >= 15:
            self.user_permissions.add(can_downvote)
        else:
            self.user_permissions.remove(can_downvote)
        
        if self.reputation >= 30:
            self.user_permissions.add(can_delete)
        else:
            self.user_permissions.remove(can_delete)

class Upvote(models.Model):
    voted_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Downvote(models.Model):
    voted_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    upvote = models.ManyToManyField(Upvote)
    downvote = models.ManyToManyField(Downvote)

    class Meta:
        permissions = [
            ("can_delete", "Can delete tips from other users"),
            ("can_downvote", "Can downvote tips from other users"),
        ]

    def upvoteForUser(self, user):
        if not self.upvote.filter(voted_user=user).exists():
            new_upvote = Upvote(voted_user=user)
            new_upvote.save()
            self.upvote.add(new_upvote)
            self.downvote.filter(voted_user=user).delete()
            self.author.update_reputation()

    def downvoteForUser(self, user):
        if not self.downvote.filter(voted_user=user).exists():
            new_downvote = Downvote(voted_user=user)
            new_downvote.save()
            self.downvote.add(new_downvote)
            self.upvote.filter(voted_user=user).delete()
            self.author.update_reputation()

    def remove_votes(self):
        self.upvote.all().delete()
        self.downvote.all().delete()
        self.author.update_reputation()

    def user_has_upvoted(self, user):
        return self.upvote.filter(voted_user=user).exists()

    def user_has_downvoted(self, user):
        return self.downvote.filter(voted_user=user).exists()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username} (rep: {self.author.reputation})"

