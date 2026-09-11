from django.urls import path

from .views import (
    onesignal_worker,
    home,
    login_page,
    logout_page,
    admin_dashboard,
    login_user,
    logout_user,
)

urlpatterns = [
    path("OneSignalSDKWorker.js", onesignal_worker, name="onesignal_worker"),
    path("", home, name="home"),
    path("login/", login_page, name="login_page"),
    path("logout-page/", logout_page, name="logout_page"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),

    path("api/login/", login_user, name="login_api"),
    path("api/logout/", logout_user, name="logout_api"),
]