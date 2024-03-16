from django.shortcuts import redirect, render
# Create yfrom django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect
        
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.betfair_username = form.cleaned_data['betfair_username']
            user.profile.betfair_password = form.cleaned_data['betfair_password']
            user.profile.betfair_api_key = form.cleaned_data['betfair_api_key']
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
