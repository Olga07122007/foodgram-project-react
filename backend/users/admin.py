from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class UsersAdmin(UserAdmin):
    list_display = (
        "id",
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    
    fieldsets = ((
        "User",
        {"fields": (
            'username', 'password', 'email',
            'first_name', 'last_name', 'last_login', 
            'date_joined', 'role', 'is_active', 
            'is_superuser', 'is_staff'
        )}
    ),)
    

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    

admin.site.register(User, UsersAdmin)
admin.site.register(Subscription, SubscribeAdmin)
    

