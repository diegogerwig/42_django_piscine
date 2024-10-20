from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip, Upvote, Downvote

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Tip)
admin.site.register(Upvote)
admin.site.register(Downvote)

