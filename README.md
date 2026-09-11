# Notification Management System

A Django-based notification management system that supports multiple notification channels with trigger-based notifications.

## Features

- Trigger-based notification system
- Admin dashboard for managing notification templates
- Enable/disable notification templates
- Test notifications from the dashboard
- WhatsApp notifications using WhatsApp Cloud API
- Email notifications using Brevo
- Web Push notifications using OneSignal
- User login and logout triggers

## Notification Channels

### WhatsApp
Sends notifications through the WhatsApp Cloud API.

### Email
Sends transactional emails using the Brevo API.

### Web Push
Sends browser push notifications using OneSignal.

## Notification Triggers

The system currently supports triggers such as:

- Login
- Logout

Each trigger can have notification templates for WhatsApp, Email, and Web Push.

## Admin Dashboard

The admin dashboard allows users to:

- View available notification triggers
- Create and edit notification templates
- Enable or disable channels
- Test notifications
- Manage notification settings

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite
- WhatsApp Cloud API
- Brevo Email API
- OneSignal Web Push
- Gunicorn
- Render
- Vercel

## Project Structure

```text
notification-system/
│
├── backend/
│   ├── config/
│   ├── notifications/
│   ├── users/
│   ├── templates/
│   ├── manage.py
│   └── requirements.txt
│
├── OneSignalSDKWorker.js
├── .gitignore
└── README.md
