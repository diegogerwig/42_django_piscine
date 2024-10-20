from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation')}),
    )
    readonly_fields = ('reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_reputation_permissions()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tip)

