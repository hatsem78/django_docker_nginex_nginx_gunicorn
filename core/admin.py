from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        (_("Personal info"), {"fields": (
            "name", "last_name")
        }),
    )


class MeetupAdmin(admin.ModelAdmin):
    model = models.Meetup
    list_display = (
        "id",
        "name",
        "date",
        "description",
        "count_beer",
        "maximum_temperature",
        "count_participants",
        "direction"
    )
    search_fields = ("name", "date", "description", "direction")
    list_filter = ("name",)
    ordering = ("-name",)


class MeetupEnrollInviteUsersAdmin(admin.ModelAdmin):
    model = models.MeetupEnrollInviteUsers
    list_display = (
        "id",
        "user",
        "meetup",
        "user_check_in",
    )
    search_fields = ("user", "meetup", "user_check_in")
    list_filter = ("user",)
    ordering = ("-user",)


class NotificationAdmin(admin.ModelAdmin):
    model = models.MeetupEnrollInviteUsers
    list_display = (
        "id",
        "user",
        "text",
        "date",
        "is_seen",
        "is_read"
    )
    search_fields = ("user", "date", "text")
    list_filter = ("user",)
    ordering = ("-user",)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Meetup, MeetupAdmin)
admin.site.register(models.MeetupEnrollInviteUsers, MeetupEnrollInviteUsersAdmin)
admin.site.register(models.Notification, NotificationAdmin)


