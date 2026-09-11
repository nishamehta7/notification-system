import requests
from django.conf import settings
from .models import Trigger


def send_whatsapp(phone_number, message):
    if not settings.WHATSAPP_ACCESS_TOKEN:
        return {
            "success": False,
            "message": "WhatsApp credentials are not configured."
        }

    url = f"https://graph.facebook.com/v25.0/{settings.PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "jaspers_market_order_confirmation_v1",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": "Nisha"},
                        {"type": "text", "text": "123456"},
                        {"type": "text", "text": "Sep 10, 2026"}
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    try:
        response_data = response.json()
    except ValueError:
        response_data = {"raw_response": response.text}

    return {
        "success": response.ok,
        "status_code": response.status_code,
        "response": response_data
    }


def send_email(to_email, subject, body):
    if not settings.BREVO_API_KEY:
        return {
            "success": False,
            "message": "Brevo API key is not configured."
        }

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY,
    }

    data = {
        "sender": {
            "email": settings.BREVO_FROM_EMAIL,
            "name": "Notification Management System",
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "textContent": body,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    try:
        response_data = response.json()
    except ValueError:
        response_data = {"raw_response": response.text}

    return {
        "success": response.ok,
        "status_code": response.status_code,
        "response": response_data
    }


def send_web_push(subscription_id, title, body):
    if not settings.ONESIGNAL_REST_API_KEY:
        return {
            "success": False,
            "message": "OneSignal credentials are not configured."
        }

    url = "https://api.onesignal.com/notifications"

    headers = {
        "Authorization": f"Key {settings.ONESIGNAL_REST_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "app_id": settings.ONESIGNAL_APP_ID,
        "include_subscription_ids": [subscription_id],
        "headings": {"en": title},
        "contents": {"en": body},
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    try:
        response_data = response.json()
    except ValueError:
        response_data = {"raw_response": response.text}

    return {
        "success": response.ok,
        "status_code": response.status_code,
        "response": response_data
    }


def fire_notification_trigger(
    trigger_name,
    email=None,
    phone_number=None,
    subscription_id=None
):
    try:
        trigger = Trigger.objects.get(
            name=trigger_name,
            is_active=True
        )
    except Trigger.DoesNotExist:
        return {
            "success": False,
            "message": f"Trigger '{trigger_name}' not found or inactive."
        }

    results = []

    templates = trigger.templates.filter(is_enabled=True)

    for template in templates:

        if template.channel == "whatsapp":
            if phone_number:
                result = send_whatsapp(
                    phone_number,
                    template.body
                )
            else:
                result = {
                    "success": False,
                    "message": "Phone number not provided."
                }

        elif template.channel == "email":
            if email:
                result = send_email(
                    email,
                    template.subject,
                    template.body
                )
            else:
                result = {
                    "success": False,
                    "message": "Email not provided."
                }

        elif template.channel == "web_push":
            if subscription_id:
                result = send_web_push(
                    subscription_id,
                    template.title,
                    template.body
                )
            else:
                result = {
                    "success": False,
                    "message": "Push subscription ID not provided."
                }

        else:
            result = {
                "success": False,
                "message": f"Unknown channel: {template.channel}"
            }

        results.append({
            "channel": template.channel,
            "result": result
        })

    return {
        "success": True,
        "trigger": trigger.name,
        "results": results
    }