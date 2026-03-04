import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
    label="Password",
    strip=False,
    widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',  # prevents autofill suggestions
        'autocorrect': 'off',
        'autocapitalize': 'none',
        'spellcheck': 'false',
    }),
    help_text=mark_safe("""
        <ul style="margin-bottom: 0; padding-left: 1.2rem;">
            <li>At least 8 characters long</li>
            <li>At least 1 uppercase letter</li>
            <li>At least 3 digits</li>
            <li>At least 1 special character</li>
        </ul>
    """)
)
    password2 = forms.CharField(
    label="Confirm Password",
    widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'autocorrect': 'off',
        'autocapitalize': 'none',
        'spellcheck': 'false',
    }),
    strip=False,
)


    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Custom condition: 8+ chars, 1 uppercase, 3 digits, 1 special char
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least 1 uppercase letter.")
        if len(re.findall(r'\d', password)) < 3:
            raise forms.ValidationError("Password must contain at least 3 digits.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least 1 special character.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
