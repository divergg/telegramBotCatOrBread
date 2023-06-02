from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from ..models import Profile, Message, Image
from ..views import OperateBotCommandsView, ImageUploadView
from ..const import ANSWER_0, ANSWER_1_YES, ANSWER_UNKNOWN
import tempfile
import PIL
import os


class OperateBotCommandsViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = OperateBotCommandsView.as_view()
        self.username = 'test_user'
        self.message = '/start'


    def test_operate_bot_commands_view(self):
        request = self.factory.post('/bot', data={'id': self.username, 'message': self.message})
        response = self.view(request)
        expected_bot_answer = ANSWER_0

        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.data)
        self.assertEqual(response.data['response'], expected_bot_answer)

        # Additional assertions to check the database state
        user = Profile.objects.filter(username=self.username).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.step_in_dialog, 1)

        message = Message.objects.filter(user=user, user_message=self.message).first()
        self.assertIsNotNone(message)

        #send second message
        second_message = 'да'
        expected_bot_answer = ANSWER_1_YES
        request = self.factory.post('/bot', data={'id': self.username, 'message': second_message})
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.data)
        self.assertEqual(response.data['response'], expected_bot_answer)


class ImageUploadViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImageUploadView.as_view()
        self.username = 'test_user'
        self.image_file = self.create_test_image()  # Helper function to create a test image file

    def create_test_image(self):
        image = PIL.Image.new('RGB', (100, 100), color='red')

        # Create a temporary file to save the test image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            image.save(f, 'JPEG')
            return f.name

    def test_image_upload_view(self):
        with open(self.image_file, 'rb') as file:
            request = self.factory.post('/bot/image', data={'id': self.username, 'image': file})
            force_authenticate(request)
            response = self.view(request)

        expected_bot_answer = ANSWER_UNKNOWN

        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.data)
        self.assertEqual(response.data['response'], expected_bot_answer)

        # Additional assertions to check the database state
        user = Profile.objects.filter(username=self.username).first()
        self.assertIsNotNone(user)

        # Get the name of the image file
        image_file_name = os.path.basename(self.image_file)

        image = Image.objects.filter(related_image__contains=image_file_name).first()
        self.assertIsNotNone(image)

        expected_user_response = 'UNKNOWN'

        message = Message.objects.filter(user=user, user_message='IMAGE').first()
        self.assertIsNotNone(message)
        self.assertEqual(message.user_response, expected_user_response)