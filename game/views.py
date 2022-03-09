from django.views.generic import (CreateView, ListView, UpdateView, TemplateView,
                                  RedirectView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

import random

from mixins.mixins import RoleRequiredMixin
from .models import Question, Answer, Game, UserAnswer
from .forms import QuestionForm, AnswerForm, GamePlayForm


class QuestionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    roles_required = ['admin']
    template_name = 'game/question_create_update.html'
    form_class = QuestionForm

    def get_success_url(self):
        messages.success(self.request, 'Question is successfully created.')
        return reverse_lazy('game:question_list')


class QuestionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    roles_required = ['admin']
    template_name = 'game/question_create_update.html'
    form_class = QuestionForm

    def get_object(self, queryset=None):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        return question

    def get_success_url(self):
        messages.success(self.request, 'Question is successfully updated.')
        return reverse_lazy('game:question_list')


class QuestionListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    roles_required = ['admin']
    template_name = 'game/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        qs = Question.objects.all()
        return qs


class AnswerCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    roles_required = ['admin']
    template_name = 'game/answer_create_update.html'
    form_class = AnswerForm

    def get_form_kwargs(self):
        kwargs = super(AnswerCreateView, self).get_form_kwargs()
        kwargs['question_id'] = self.kwargs.get('question_id')
        return kwargs

    def form_valid(self, form):
        answer = form.save(commit=False)
        question_id = self.kwargs.get('question_id')
        answer.question_id = question_id

        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        messages.success(self.request, 'Answer is successfully created.')
        return reverse_lazy('game:answer_list', kwargs={'question_id': question.id})


class AnswerUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    roles_required = ['admin']
    template_name = 'game/answer_create_update.html'
    form_class = AnswerForm

    def get_object(self, queryset=None):
        answer_id = self.kwargs.get('answer_id')
        answer = get_object_or_404(Answer, id=answer_id)
        return answer

    def get_success_url(self):
        question_id = self.object.question_id
        messages.success(self.request, 'Answer is successfully updated.')
        return reverse_lazy('game:answer_list', kwargs={'question_id': question_id})


class AnswerListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    roles_required = ['admin']
    template_name = 'game/answer_list.html'
    context_object_name = 'answers'

    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        qs = Answer.objects.filter(question_id=question_id)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerListView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        context['question'] = question
        return context


class GameStartTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'game/game_start.html'


class GameListView(LoginRequiredMixin, ListView):
    template_name = 'game/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        qs = Game.objects.filter(user=self.request.user)
        return qs


class GameCreateRedirectView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        questions_list = list(Question.objects.all().values_list('id', flat=True))

        if len(questions_list) < 5:
            messages.error(self.request, 'There are not enough questions in our database!')
            return HttpResponseRedirect(reverse_lazy('game:game_start'))

        # create a game
        game = Game.objects.create(
            user_id=self.request.user.id,
        )

        self.game_id = game.id

        selected_questions = random.sample(questions_list, 5)

        for question in selected_questions:
            UserAnswer.objects.create(
                game_id=game.id,
                question_id=question,
            )

        return super(GameCreateRedirectView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('game:game_play', kwargs={'game_id': self.game_id})


class PlayGameView(LoginRequiredMixin, FormView):
    template_name = 'game/game_play.html'
    form_class = GamePlayForm

    def dispatch(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, id=game_id, user_id=self.request.user)
        questions = UserAnswer.objects.filter(game_id=game.id, answer__isnull=True)
        if not questions.exists():
            game.is_finished = True
            game.save()
            messages.error(self.request, 'The game is over!')
            return HttpResponseRedirect(reverse_lazy('game:game_list'))

        return super(PlayGameView, self).dispatch(request, *args, **kwargs)

    def get_question(self):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, id=game_id, user_id=self.request.user)
        question = UserAnswer.objects.filter(game_id=game.id, answer__isnull=True)
        if question.exists():
            question = question.first().question
            return question.id

    def get_context_data(self, **kwargs):
        context = super(PlayGameView, self).get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.get_question())
        context['question'] = question
        return context

    def get_form_kwargs(self):
        kwargs = super(PlayGameView, self).get_form_kwargs()
        kwargs['game_id'] = self.kwargs.get('game_id')
        kwargs['question_id'] = self.get_question()
        return kwargs

    def form_valid(self, form):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, id=game_id)
        question_id = self.get_question()
        question = get_object_or_404(Question, id=question_id)
        answer = form.cleaned_data.get('answer')
        user_answer = UserAnswer.objects.filter(game_id=game.id, answer__isnull=True)
        if user_answer.exists():
            user_answer = user_answer.first()
            user_answer.answer = answer
            user_answer.save()

        if answer.is_right_answer:
            game.score += question.point
            game.save()
            messages.success(self.request, 'Your answer was Right')
        else:
            right_answer = question.answers.filter(is_right_answer=True)
            messages.error(self.request, 'Your answer was Wrong, The right answer was {}'.format(
                right_answer[0]
            ))

        return super(PlayGameView, self).form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs.get('game_id')
        return reverse_lazy('game:game_play', kwargs={'game_id': game_id})
