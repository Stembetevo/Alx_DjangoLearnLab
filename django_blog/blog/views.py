from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Sign Up View 
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! Please login.')
        return super().form_valid(form)

register = SignUpView.as_view()

# Profile View
@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'user': request.user})

# Edit Profile View
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'blog/edit_profile.html', {'user': request.user})

# Home View (temporary)
def home(request):
    return render(request, 'blog/base.html')

# Posts View (temporary)
def posts(request):
    return render(request, 'blog/base.html')