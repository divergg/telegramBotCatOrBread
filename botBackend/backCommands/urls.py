from django.urls import path

from . import views

urlpatterns = [
    path('bot', views.OperateBotCommandsView.as_view(), name='bot'),
    path('bot/image', views.ImageUploadView.as_view(), name='image')
]
