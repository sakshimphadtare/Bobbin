import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))

        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))

        if len(re.findall(r'\d', password)) < 3:
            raise ValidationError(_('Password must contain at least three digits.'))

        if not re.search(r'[!@#$%^&*()\-_=+{}\[\]:;"\'<>,.?/]', password):
            raise ValidationError(_('Password must contain at least one special character.'))

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, contain 1 uppercase letter, "
            "3 digits, and 1 special character."
        )
