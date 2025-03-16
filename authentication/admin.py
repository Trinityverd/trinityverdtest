from django.contrib import admin
from authentication.models import UserProfile, SubCounty


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(SubCounty)
class SubCountyAdmin(admin.ModelAdmin):
    list_display = ('name',)