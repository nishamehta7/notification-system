# Notification Management System - Fixed Version

## Main fix
The login page now initializes OneSignal Web SDK v16 correctly and uses a root-scoped service worker at:

`/OneSignalSDKWorker.js`

The service worker is served by Django, so no separate static-file server is required for local development.

## Run locally

1. Open a terminal in the `backend` folder.
2. Create/activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Make sure `.env` contains your existing API credentials.
5. Run migrations if needed:

   `python manage.py migrate`

6. Start Django:

   `python manage.py runserver`

7. Open:

   `http://127.0.0.1:8000/login/`

8. Wait a few seconds for OneSignal to initialize.
9. Click **Enable Web Push Notifications** and allow browser notifications.
10. The OneSignal Subscription ID should automatically appear in the field.
11. Enter username/password and click **Login**.

## Verify the service worker
Open this URL in the browser:

`http://127.0.0.1:8000/OneSignalSDKWorker.js`

You should see the OneSignal `importScripts(...)` line.

## Important
The supplied `.env` contains API credentials. Do not commit it to GitHub or share it publicly. Use `.env.example` as the template for new environments.
