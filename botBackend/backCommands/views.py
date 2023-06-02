from rest_framework.response import Response
from rest_framework import views, parsers
from .utils import handle_errors
from .interpretation import interpret_text_answer, interpret_image_answer
from .models import Profile, Message, Image
import os
# Create your views here.



class OperateBotCommandsView(views.APIView):

    ALLOWED_FIELDS = [
        'id', 'message'
    ]

    def post(self, request):
        data = request.data

        # Handle possible errors (if request is made through API)
        handle_errors(data, self.ALLOWED_FIELDS)

        username = data['id']
        message = data['message']

        user = Profile.objects.filter(username=username).first()
        if not user:
            user = Profile.objects.create(username=username)

        user_response = interpret_text_answer(message)

        message = Message.objects.create(
                user=user,
                user_message=message,
                user_response=user_response,
            )

        bot_answer = message.bot_answer
        return Response({'response': bot_answer})


class ImageUploadView(views.APIView):
    parser_classes = [parsers.MultiPartParser]

    ALLOWED_FIELDS = [
        'id', 'image'
    ]

    def post(self, request):
        data = request.data

        # Handle possible errors (if request is made through API)
        handle_errors(data, self.ALLOWED_FIELDS)

        username = data['id']
        image_file = data.get('image')

        user = Profile.objects.filter(username=username).first()

        # In rare case if user did not previously use /start command
        if not user:
            user = Profile.objects.create(username=username)

        user_message = 'IMAGE'
        image = Image.objects.create(related_image=image_file)
        user_response = interpret_image_answer(image.related_image)

        message = Message.objects.create(
            user=user,
            user_message=user_message,
            user_response=user_response,
            image=image
        )

        bot_answer = message.bot_answer

        return Response({'response': bot_answer})











