from django.shortcuts import render

from user.forms import CustomAuthenticationForm, UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView


def main(request):
    print(request.user)


def create_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


class CustomLogoutView(LogoutView):
    template_name = 'log_out.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
