from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import User, Tip, CustomGroup

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'manual_can_downvote', 'manual_can_delete', 'get_members')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {
            'fields': (
                'manual_can_downvote',
                'manual_can_delete',
                'permissions',
            ),
        }),
    )

    def get_members(self, obj):
        members = User.objects.filter(groups__id=obj.id)
        return format_html(
            '<br>'.join(
                '<a href="{}">{}</a>'.format(
                    reverse('admin:ex_user_change', args=[member.id]),
                    member.username
                )
                for member in members
            )
        ) if members.exists() else 'No members'
    get_members.short_description = 'Group Members'

class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': (
            'reputation', 
            'can_downvote_by_reputation', 
            'can_delete_by_reputation',
            'manual_can_downvote',
            'manual_can_delete'
        )}),
    )
    readonly_fields = ('reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation')
    list_display = ('username', 'email', 'reputation', 'can_downvote_by_reputation', 
                   'can_delete_by_reputation', 'manual_can_downvote', 'manual_can_delete')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from .utils import update_user_reputation
        update_user_reputation(obj)

admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tip)

