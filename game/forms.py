from django import forms

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'point']
        widgets = {
            'point': forms.NumberInput(attrs={'max': 20, 'min': 5})
        }


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.question_id = kwargs.pop('question_id', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['answer', 'is_right_answer']
        widgets = {
            'is_right_answer': forms.CheckboxInput()
        }

    def clean(self):
        # is_right_answer
        is_right_answer = self.cleaned_data.get('is_right_answer')

        if is_right_answer:
            right_answers = Answer.objects.filter(
                question_id=self.question_id,
                is_right_answer=True
            )
            if self.instance.id:
                right_answers = right_answers.exclude(id=self.instance.id)

            if right_answers.count() > 0:
                raise forms.ValidationError('Just one Right Answer is allowed!')

        return super(AnswerForm, self).clean()


class GamePlayForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question_id = kwargs.pop('question_id', None)
        self.game_id = kwargs.pop('game_id', None)
        super(GamePlayForm, self).__init__(*args, **kwargs)

        self.fields['answer'].queryset = Answer.objects.filter(question_id=self.question_id)

    answer = forms.ModelChoiceField(queryset=None, required=True)
