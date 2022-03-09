from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .validators import question_point_validator

User = get_user_model()


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.CharField(max_length=2000, null=True, blank=False, verbose_name='Question')
    point = models.IntegerField(default=5, verbose_name='Point',
                                validators=[question_point_validator])

    def __str__(self):
        return self.question


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, null=True, blank=True, related_name='answers',
                                 on_delete=models.CASCADE,
                                 verbose_name='Question')
    answer = models.CharField(max_length=1000, null=True, blank=False, verbose_name='Answer')
    is_right_answer = models.BooleanField(default=False, verbose_name='Right Answer')

    def __str__(self):
        return self.answer


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name='User')
    score = models.IntegerField(default=0, verbose_name='Score')
    is_finished = models.BooleanField(default=False, verbose_name='Is Finished')


class UserAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name='Game')
    question = models.ForeignKey(Question, null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 verbose_name='Question')
    answer = models.ForeignKey(Answer, null=True, blank=True,
                               on_delete=models.CASCADE,
                               verbose_name='Answer')

    @property
    def is_answered(self):
        if self.answer:
            return True
        return False

    @property
    def answer_is_right(self):
        if self.answer:
            if self.answer.is_right_answer:
                return True
        return False
