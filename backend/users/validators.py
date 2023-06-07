from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError("Имя пользователя не может быть 'me'!")


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0
    message = (
        'Имя пользователя может содержать:'
        ' буквы, цифры '
        'и знаки @ . + -'
    )
