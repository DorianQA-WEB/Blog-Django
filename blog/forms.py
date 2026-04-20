from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """
    Форма для отправки поста по электронной почте.

    Позволяет пользователю ввести:
    - Имя (обязательно)
    - Свой email (обязательно)
    - Email получателя (обязательно)
    - Комментарий (необязательно)

    Используется на странице детального просмотра поста.
    """
    name = forms.CharField(max_length=25, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'from-control ma-1', 'placeholder': 'E-Mail'}))
    to = forms.EmailField(required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': "To"}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control mb-1', 'placeholder': 'Comments'}))

class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
                             )
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}))


    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    """
    Форма для добавления комментария к посту.

    Наследуется от ModelForm, привязана к модели Comment.
    Пользователь может ввести:
    - Имя (обязательно)
    - Email (обязательно)
    - Текст комментария (обязательно)

    Отображается под каждым постом.
    """
    query = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control mb-1', 'placeholder': 'Enter search term...'}))

