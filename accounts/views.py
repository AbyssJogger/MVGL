from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView

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
        'page_title': 'signup',
        'keywords': ['register', 'signup'],
        'description': 'signup'
    }
    
    return render(req, 'register.html', ctx)

class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'login'
        ctx['keywords'] = ['login']
        ctx['description'] = 'login'
        return ctx
