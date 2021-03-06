from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):   # 부모 필드(username, password1, password2)
    # 추가 필드
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')  # 튜플 구조임