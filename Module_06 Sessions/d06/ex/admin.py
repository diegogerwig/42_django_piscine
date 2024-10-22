from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tip

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

admin.site.register(User, UserAdmin)
admin.site.register(Tip)

