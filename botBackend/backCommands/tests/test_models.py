from django.test import TestCase
from django.utils import timezone
from ..models import Profile, Message
from ..const import ANSWER_0


class ProfileModelTests(TestCase):

    def test_save_new_profile(self):
        username = 'test_user'
        profile = Profile(username=username)
        profile.save()

        self.assertEqual(profile.step_in_dialog, 0)
        self.assertIsNotNone(profile.date_of_creation)
        self.assertEqual(profile.username, username)

    def test_save_existing_profile(self):
        username = 'test_user'
        user_message = 'start'
        last_response = 'START'
        last_message = Message(user_response=last_response, user_message=user_message)
        profile = Profile(username=username)
        profile.save()

        self.assertEqual(profile.step_in_dialog, 0)
        self.assertIsNotNone(profile.date_of_creation)
        self.assertEqual(profile.username, username)

        last_message.user = profile
        last_message.save()

        profile.save()

        self.assertEqual(profile.step_in_dialog, 1)


class MessageModelTests(TestCase):

    def test_save_message(self):
        username = 'test_user'
        user_message = 'start'
        user_response = 'START'
        bot_answer = ANSWER_0
        profile = Profile(username=username)
        profile.save()

        message = Message(user=profile, user_response=user_response, user_message=user_message)
        message.save()

        self.assertEqual(message.user, profile)
        self.assertEqual(message.user_response, user_response)
        self.assertEqual(message.bot_answer, bot_answer)
        self.assertIsNotNone(message.datetime)


