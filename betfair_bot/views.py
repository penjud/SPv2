from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django import forms

# Example form class for placing a bet
class PlaceBetForm(forms.Form):
    bet_amount = forms.DecimalField(min_value=0.01)
    selected_horse = forms.ChoiceField(choices=[('Horse 1', 'Horse 1'), ('Horse 2', 'Horse 2'), ('Horse 3', 'Horse 3')])

def home(request):
    # Context to pass to the template
    context = {
        'welcome_message': 'Welcome to our betting bot!',
        'features': ['Automatic betting', 'Real-time statistics', 'User-friendly interface'],
    }
    return render(request, 'bot/home.html', context)

def place_bet(request):
    if request.method == 'POST':
        form = PlaceBetForm(request.POST)
        if form.is_valid():
            # Process the bet through your BettingStrategy logic
            # ...
            messages.success(request, 'Your bet has been placed!')
            return redirect(reverse('betting_history'))
        else:
            # If the form is not valid, display it again with errors
            return render(request, 'bot/place_bet.html', {'form': form})
    else:
        # Instantiate an empty form for GET request
        form = PlaceBetForm()
        return render(request, 'bot/place_bet.html', {'form': form})

def betting_history(request):
    # Retrieve betting history data
    user_betting_history = [
        {'date': '2024-03-10', 'bet': 'Horse 1', 'outcome': 'Won', 'amount': 50},
        {'date': '2024-03-09', 'bet': 'Horse 2', 'outcome': 'Lost', 'amount': 30},
    ]
    return render(request, 'bot/betting_history.html', {'betting_history': user_betting_history})
