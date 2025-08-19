from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView, PasswordResetCompleteView

from .forms import RegisterForm

def register_view(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    ctx = {
        'form': form,
        'page_title': 'Signup',
        'keywords': ['register', 'signup'],
        'description': 'signup'
    }
    
    return render(req, 'registration/register.html', ctx)

class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Login'
        ctx['keywords'] = ['login']
        ctx['description'] = 'login'
        return ctx

class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Password Reset'
        ctx['keywords'] = ['password', 'reset']
        ctx['description'] = 'password reset'
        return ctx

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Password Reset Done'
        ctx['keywords'] = ['password', 'reset']
        ctx['description'] = 'password reset done'
        return ctx

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Password Reset Confirm'
        ctx['keywords'] = ['password', 'reset']
        ctx['description'] = 'password reset confirm'
        return ctx

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Password Reset Complete'
        ctx['keywords'] = ['password', 'reset']
        ctx['description'] = 'password reset complete'
        print(ctx)
        return ctx
