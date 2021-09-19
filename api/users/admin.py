from django.contrib import admin

from api.users.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_of_join',)


admin.site.register(User, UserAdmin)