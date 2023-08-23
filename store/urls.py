from django.urls import path

from . import views

urlpatterns = [
    path("update/<str:session_id>/", views.update_session),
]
