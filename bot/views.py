# views.py
from django.shortcuts import render
from .bot_logic import MartingaleStrategy

def home(request):
    # This view could display general info about the betting bot and how to use it
    return render(request, 'bot/home.html')

def place_bet(request):
    # Logic to place a bet using a specific strategy
    strategy = MartingaleStrategy()
    market_data = {}  # Fetch market data
    strategy.execute(market_data)
    return render(request, 'bot/bet_placed.html', context={'bet_info': "Your bet has been placed"})
