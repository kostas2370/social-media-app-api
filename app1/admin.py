from django.contrib import admin
from .models import User, Message, FriendRequest
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User

    fieldsets = (*UserAdmin.fieldsets,
                 ('Other Personal info',
                  {'fields': ('date_of_birth', 'friends')})
                 )


admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(FriendRequest)
