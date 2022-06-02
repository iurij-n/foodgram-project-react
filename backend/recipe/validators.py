import re

from django.core.exceptions import ValidationError


def validate_slug(value):
    """Проверка поля slug модели Tag."""

    if re.findall(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Required 200 characters or fewer, '
            'letters, digits and _ only.')
