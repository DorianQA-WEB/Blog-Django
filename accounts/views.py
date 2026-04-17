from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, LoginForm, UpdateProfileForm, UpdateUserForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


class SignUpView(generic.CreateView):
    """
    CreateView для регистрации нового пользователя.

        Назначение: отображает форму регистрации и создаёт нового пользователя при отправке валидной формы.
        Поведение:
            GET: рендерит форму SignUpForm с начальными данными (self.initial).
            POST: при валидной форме сохраняет пользователя, добавляет success-сообщение и редиректит на страницу входа.
            dispatch: перенаправляет аутентифицированных пользователей на 'blog:post_list'.
        Побочные эффекты: создаёт запись User в БД и выводит сообщение через django.contrib.messages. """
    form_class = SignUpForm
    initial = None # принимает {'key': 'value'}
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='blog:post_list')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f"Успешно создан аккаунт {username}")
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    """
    LoginView с поддержкой галочки «Запомнить меня».

        Назначение: выполняет вход пользователя; при снятой галочке remember_me делает сессию сессионной (истекает при закрытии браузера).
        Поведение:
            form_valid: если form.cleaned_data['remember_me'] == False, вызывает request.session.set_expiry(0) и помечает сессию как изменённую.
        Побочные эффекты: изменяет время жизни сессии в зависимости от выбранной опции. """
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
    # Установим время истечения сеанса равным 0 секундам.
    # Таким образом, он автоматически закроет сеанс после закрытия браузера.
    # И обновим данные.
            self.request.session.set_expiry(0)
            self.request.session.modified = True

    # В противном случае сеанс браузера будет таким же
    # как время сеанса cookie "SESSION_COOKIE_AGE", определенное в settings.py
        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    """
    Защищённый представлением, позволяющее пользователю просматривать и редактировать профиль.

        Назначение: обрабатывает обновление данных User и связанных Profile через UpdateUserForm и UpdateProfileForm.
        Поведение:
            Требует аутентификацию (@login_required).
            POST: валидирует оба формы; при успехе сохраняет их, добавляет success-сообщение и редиректит на 'users-profile'.
            GET: инициализирует формы текущими данными пользователя и профиля и рендерит шаблон registration/profile.html.
        Побочные эффекты: обновляет записи User и Profile; может сохранять загруженные файлы (request.FILES). """
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'user_form': user_form,
                                                         'profile_form': profile_form})




class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
    PasswordChangeView с сообщением об успешной смене пароля.

        Назначение: предоставляет интерфейс смены пароля и перенаправляет на профиль после успешного изменения.
        Поведение:
            Показывает шаблон registration/change_password.html.
            При успешной смене показывает success_message и редиректит на success_url.
        Побочные эффекты: обновляет пароль пользователя. """
    template_name = 'registration/change_password.html'
    success_message = 'Ваш пароль успешно изменен'
    success_url = reverse_lazy('users-profile')
