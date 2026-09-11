from django.contrib import admin
from .models import Trigger, NotificationTemplate, PushSubscription


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "trigger",
        "channel",
        "is_enabled",
        "updated_at",
    )
    list_filter = ("channel", "is_enabled")


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscription_id",
        "player_id",
        "created_at",
    )