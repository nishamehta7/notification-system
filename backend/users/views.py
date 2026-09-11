from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response

from notifications.models import PushSubscription
from notifications.services import fire_notification_trigger


def home(request):
    return render(request, "home.html")


def login_page(request):
    from django.conf import settings
    return render(request, "login.html", {
        "onesignal_app_id": settings.ONESIGNAL_APP_ID,
    })


def onesignal_service_worker(request):
    """Serve the OneSignal service worker from the site root."""
    worker = '''importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");'''
    return HttpResponse(worker, content_type="application/javascript")


def logout_page(request):
    return render(request, "logout.html")


@ensure_csrf_cookie
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({
            "success": False,
            "message": "Username and password are required."
        })

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            "success": False,
            "message": "Invalid username or password."
        })

    login(request, user)

    subscription_id = request.data.get("subscription_id")
    if subscription_id:
        PushSubscription.objects.filter(
            subscription_id=subscription_id
        ).update(user=user)

    notification_result = fire_notification_trigger(
        trigger_name="Login",
        email=user.email,
        phone_number=request.data.get("phone_number"),
        subscription_id=subscription_id
    )

    return Response({
        "success": True,
        "message": "Login successful.",
        "username": user.username,
        "notifications": notification_result
    })


@api_view(["POST"])
def logout_user(request):
    from django.contrib.auth import logout

    logout(request)

    notification_result = fire_notification_trigger(
        trigger_name="Logout",
        email=request.data.get("email"),
        phone_number=request.data.get("phone_number"),
        subscription_id=request.data.get("subscription_id")
    )

    return Response({
        "success": True,
        "message": "Logout successful.",
        "notifications": notification_result
    })


def onesignal_worker(request):
    return HttpResponse(
        'importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");\n',
        content_type="application/javascript"
    )
