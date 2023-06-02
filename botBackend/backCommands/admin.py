from django.contrib import admin

from .models import Image, Message, Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'step_in_dialog', 'date_of_creation']
    filter = ['date_of_creation']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['related_image']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'user_message',
                    'user_response',
                    'bot_answer', 'image',
                    'datetime']
    filter = ['datetime']
