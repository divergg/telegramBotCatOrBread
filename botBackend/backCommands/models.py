from django.db import models
from django.utils import timezone

from .const import (ANSWER_0, ANSWER_1_NO, ANSWER_1_YES, ANSWER_2_NO,
                    ANSWER_2_YES, ANSWER_UNKNOWN)

# Create your models here.

class Profile(models.Model):

    username = models.CharField(max_length=50,
                                verbose_name="username",
                                blank=True,
                                default='')

    # Identify user's position in a dialog
    step_in_dialog = models.IntegerField(default=0,
                                         verbose_name='current step',
                                         null=False)

    date_of_creation = models.DateTimeField(null=False,
                                            default=timezone.now,
                                            verbose_name='creation time')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        last_message = Message.objects.filter(user=self).last()
        if not last_message:
            self.step_in_dialog = 0
        else:
            last_response = last_message.user_response
            image = last_message.image
            if last_response == 'START':
                self.step_in_dialog = 1
            elif image:
                if last_response == 'YES':
                    self.step_in_dialog = 0
            elif last_response == 'NO':
                self.step_in_dialog = 0
            elif last_response == 'YES':
                if 0 < self.step_in_dialog < 2:
                    self.step_in_dialog += 1
                else:
                    self.step_in_dialog = 0

        super().save(*args, **kwargs)


class Image(models.Model):

    related_image = models.ImageField(upload_to='images/',
                                      default=None,
                                      null=True,
                                      verbose_name='image')


class Message(models.Model):

    RESPONSE_CHOICES = [
        ('YES', 'YES'),
        ('NO', 'NO'),
        ('UNKNOWN', 'UNKNOWN'),
        ('START', 'START'),
    ]

    """
    Logic of bot answers:
    0 - for command @start (zero step of user)
    1 - for first step of user (after command @start). 
    2 - for second step of user (if user answers 'YES' on the first step)
    3 - for unknown commands
    If the user answered yes on the previous step - the 0-element of tuple is used as a response
    If user downloaded an Image the model goes to the 2-nd or 3-d step 
    """

    END_STRING = 'Для повторного определения кота(хлеба) нажмите /start'

    BOT_ANSWERS_CHOICES = {
        0: (ANSWER_0,),
        1: (ANSWER_1_YES, ANSWER_1_NO),
        2: (ANSWER_2_YES, ANSWER_2_NO),
        3: (ANSWER_UNKNOWN,)
    }

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user")
    user_message = models.TextField(verbose_name="user message", default=None)
    user_response = models.CharField(
        verbose_name="response", max_length=15, choices=RESPONSE_CHOICES, default='UNKNOWN'
    )
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE,
                              related_name="image",
                              default=None, null=True)

    bot_answer = models.TextField(verbose_name="bot answer", default=None)
    datetime = models.DateTimeField(null=False,
                                    default=timezone.now,
                                    verbose_name='message time')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'Message #{self.id}'

    def __overwrite_bot_answer(self):
        step_in_dialog = self.user.step_in_dialog
        index = step_in_dialog
        if self.user_response == 'START':
            self.bot_answer = self.BOT_ANSWERS_CHOICES[0][0]
        elif index > 0:
            if self.user_response == 'YES':
                if self.image:
                    self.bot_answer = self.BOT_ANSWERS_CHOICES[2][0]
                else:
                    self.bot_answer = self.BOT_ANSWERS_CHOICES[index][index - index]
            elif self.user_response == 'NO':
                self.bot_answer = self.BOT_ANSWERS_CHOICES[index][index - index + 1]
            else:
                self.bot_answer = self.BOT_ANSWERS_CHOICES[3][0]
        else:
            self.bot_answer = self.BOT_ANSWERS_CHOICES[3][0]

    def save(self, *args, **kwargs):
        self.__overwrite_bot_answer()
        super().save(*args, **kwargs)
        self.user.save()
