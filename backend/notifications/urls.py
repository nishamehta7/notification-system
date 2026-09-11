from django.urls import path
from .views import (
    trigger_list,
    trigger_detail,
    create_template,
    template_detail,
    toggle_template,
    test_notification,
    subscribe_push,
)

urlpatterns = [
    path("triggers/", trigger_list),
    path("triggers/<int:pk>/", trigger_detail),
    path("templates/", create_template),
    path("templates/<int:pk>/", template_detail),
    path("templates/<int:pk>/toggle/", toggle_template),
    path("test/", test_notification),
    path("push/subscribe/", subscribe_push),
]