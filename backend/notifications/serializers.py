from rest_framework import serializers

from .models import (
    Trigger,
    NotificationTemplate,
    PushSubscription,
)


class NotificationTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class TriggerSerializer(serializers.ModelSerializer):

    templates = NotificationTemplateSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Trigger
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "templates",
            "created_at",
        ]


class PushSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PushSubscription
        fields = "__all__"