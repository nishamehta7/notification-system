from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Trigger,
    NotificationTemplate,
    PushSubscription
)

from .serializers import (
    TriggerSerializer,
    NotificationTemplateSerializer,
    PushSubscriptionSerializer
)

from .services import (
    send_whatsapp,
    send_email,
    send_web_push
)


# =====================================================
# TRIGGERS
# =====================================================

@api_view(["GET", "POST"])
def trigger_list(request):

    if request.method == "GET":

        triggers = Trigger.objects.all().order_by("-created_at")

        serializer = TriggerSerializer(
            triggers,
            many=True
        )

        return Response(serializer.data)


    serializer = TriggerSerializer(
        data=request.data
    )

    if serializer.is_valid():

        trigger = serializer.save()

        return Response(
            TriggerSerializer(trigger).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(["GET", "PUT", "DELETE"])
def trigger_detail(request, pk):

    trigger = get_object_or_404(
        Trigger,
        pk=pk
    )


    if request.method == "GET":

        return Response(
            TriggerSerializer(trigger).data
        )


    if request.method == "PUT":

        serializer = TriggerSerializer(
            trigger,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    trigger.delete()

    return Response({
        "message": "Trigger deleted successfully."
    })



# =====================================================
# CREATE TEMPLATE
# =====================================================

@api_view(["POST"])
def create_template(request):

    serializer = NotificationTemplateSerializer(
        data=request.data
    )


    if serializer.is_valid():

        template = serializer.save()

        return Response(
            NotificationTemplateSerializer(template).data,
            status=status.HTTP_201_CREATED
        )


    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



# =====================================================
# TEMPLATE DETAIL
# GET / PUT / DELETE
# =====================================================

@api_view(["GET", "PUT", "DELETE"])
def template_detail(request, pk):

    template = get_object_or_404(
        NotificationTemplate,
        pk=pk
    )


    # GET TEMPLATE

    if request.method == "GET":

        serializer = NotificationTemplateSerializer(
            template
        )

        return Response(
            serializer.data
        )


    # UPDATE TEMPLATE

    if request.method == "PUT":

        serializer = NotificationTemplateSerializer(
            template,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE TEMPLATE

    template.delete()

    return Response({
        "message": "Template deleted successfully."
    })



# =====================================================
# TOGGLE TEMPLATE
# =====================================================

@api_view(["POST"])
def toggle_template(request, pk):

    template = get_object_or_404(
        NotificationTemplate,
        pk=pk
    )


    template.is_enabled = not template.is_enabled

    template.save()


    return Response({

        "message": "Template status updated.",

        "is_enabled": template.is_enabled

    })



# =====================================================
# TEST NOTIFICATION
# =====================================================

@api_view(["POST"])
def test_notification(request):

    channel = request.data.get("channel")

    template_id = request.data.get("template_id")


    template = get_object_or_404(
        NotificationTemplate,
        pk=template_id
    )


    if not template.is_enabled:

        return Response({
            "success": False,
            "message": "This channel is disabled."
        })


    # WHATSAPP

    if channel == "whatsapp":

        phone = request.data.get("phone")


        if not phone:

            return Response({
                "success": False,
                "message": "Phone number is required."
            })


        return Response(
            send_whatsapp(
                phone,
                template.body
            )
        )


    # EMAIL

    if channel == "email":

        email = request.data.get("email")


        if not email:

            return Response({
                "success": False,
                "message": "Email is required."
            })


        return Response(
            send_email(
                email,
                template.subject,
                template.body
            )
        )


    # WEB PUSH

    if channel == "web_push":

        subscription_id = request.data.get(
            "subscription_id"
        )


        if not subscription_id:

            return Response({
                "success": False,
                "message": "Subscription ID is required."
            })


        return Response(
            send_web_push(
                subscription_id,
                template.title,
                template.body
            )
        )


    return Response(
        {
            "success": False,
            "message": "Invalid channel."
        },
        status=status.HTTP_400_BAD_REQUEST
    )



# =====================================================
# PUSH SUBSCRIPTION
# =====================================================

@api_view(["POST"])
def subscribe_push(request):

    serializer = PushSubscriptionSerializer(
        data=request.data
    )


    if serializer.is_valid():

        subscription = serializer.save()

        return Response(
            PushSubscriptionSerializer(
                subscription
            ).data,
            status=status.HTTP_201_CREATED
        )


    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )