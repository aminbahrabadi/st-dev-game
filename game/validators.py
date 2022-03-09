from django.core.exceptions import ValidationError


def question_point_validator(point):
    if point not in range(5, 21):
        raise ValidationError('Point must be in range of 5 to 20')
