from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(
        label="密码", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'email', 'img', 'bio')
