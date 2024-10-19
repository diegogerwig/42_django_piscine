from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Upvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Downvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Tip(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=150)
    date = models.DateTimeField(default=timezone.now)
    upvote = models.ManyToManyField(Upvote)
    downvote = models.ManyToManyField(Downvote)

    def upvoteForUser(self, username):
        votes = self.upvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Upvote(voted_user=username)
            newvote.save()
            self.upvote.add(newvote)

            downvotes = self.downvote.all()
            for index in downvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def downvoteForUser(self, username):
        votes = self.downvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Downvote(voted_user=username)
            newvote.save()
            self.downvote.add(newvote)

            upvotes = self.upvote.all()
            for index in upvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def __str__(self):
        return str(self.date.strftime('%Y-%m-%d %H:%M:%S')) + ' ' + self.content + ' by ' + self.author \
               + ' upvotes : ' + str(len(self.upvote.all())) \
               + ' downvotes : ' + str(len(self.downvote.all()))

    def get_author(self):
        return self.author

    def user_has_upvoted(self, username):
        return self.upvote.filter(voted_user=username).exists()

    def user_has_downvoted(self, username):
        return self.downvote.filter(voted_user=username).exists()

