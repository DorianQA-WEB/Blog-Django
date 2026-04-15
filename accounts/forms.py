from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    '''SignUpForm
Наследует: UserCreationForm
Назначение: регистрация нового пользователя с дополнительными полями и кастомными виджетами.
Поля:
first_name (str): текстовое поле, max_length=100, placeholder "Enter first name".
last_name (str): текстовое поле, max_length=100, placeholder "Enter last name".
username (str): текстовое поле, max_length=30, placeholder "Enter Username".
email (str): email-поле, max_length=200, placeholder "Enter your E-Mail".
password1 (str): пароль, max_length=50, placeholder "Enter password".
password2 (str): подтверждение пароля, max_length=50, placeholder "Confirm password".
Meta:
model = User
fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
Поведение:
- Использует стандартную валидацию UserCreationForm (включая проверку совпадения password1/password2).
- Виджеты настроены для Bootstrap-классов.'''
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter first name'}
    ))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter last name'}
    ))
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter Username'}
    ))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter your E-Mail'}
    ))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Confirm password'}
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    '''LoginForm
Наследует: AuthenticationForm
Назначение: форма входа с опцией "remember_me".
Поля:
username (str): required, max_length=100, placeholder "Username".
password (str): required, max_length=50, placeholder "Password".
remember_me (bool): необязательное булево поле.
Meta:
model = User
field = ['username', 'password', 'remember_me']  # опечатка: должно быть fields
Замечания:
- Для корректной работы Meta должен использовать атрибут fields (множественное число).
- Поле remember_me нужно обрабатывать вручную в представлении (установка сессии с разным временем жизни).'''
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': "form-control mb-1", 'placeholder': "Username"}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control mb-1', 'placeholder': "Password"}))
    remember_me = forms.BooleanField(required=False)


    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    '''UpdateUserForm
Наследует: forms.ModelForm
Назначение: обновление username и email текущего пользователя.
Поля:
username (str): required, max_length=100, placeholder "Username".
email (Email): required, placeholder "Email".
Meta:
model = User
fields = ['username', 'email']
Поведение:
- Стандартная валидация email и уникальности username должна обрабатываться в clean() при необходимости.'''
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control mb-1', 'placeholder': 'Username'}
                               ))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Email'}
    ))


    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    '''UpdateProfileForm
Наследует: forms.ModelForm
Назначение: обновление профиля пользователя.
Поля:
avatar (Image): FileInput с классом form-control mb-1.
bio (str): Textarea с классом form-control.
Meta:
model = Profile
fields = ['avatar', 'bio']'''
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control mb-1'}
    ))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
