from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django import forms
from betfairlightweight import APIClient
from betfairlightweight.filters import market_filter
from betfairlightweight.exceptions import APIError
import os
import logging
from django.core.paginator import Paginator
import betfair_bot

# Create a logger
logger = logging.getLogger(__name__)

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

def market_data_view(request):
    # Use betfairlightweight to fetch market data
    try:
        # Create an instance of the betfairlightweight API client
        api_client = APIClient(
            username=os.environ['BETFAIR_USERNAME'],
            password=os.environ['BETFAIR_PASSWORD'],
            app_key=os.environ['BETFAIR_APP_KEY'],
            certs=os.environ['BETFAIR_CERTS']
        )

        # Log in to the Betfair API
        api_client.login()

        # Fetch market data using the API client
        market_data = api_client.betting.list_market_catalogue(
            filter=market_filter(text_query='horse racing'),
            market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION'],
            max_results=10
        )

        # Log out from the Betfair API
        api_client.logout()

    except APIError as e:
        market_data = []
        # Log the exception
        logger.error(f"Error fetching market data: {str(e)}")

    # Render the template with market data
    return render(request, 'bot/market_data.html', {'market_data': market_data})

def betting_history_view(request):
    bets_list = Bet.objects.all().order_by('-id')
    paginator = Paginator(bets_list, 10)  # Show 10 bets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'bot/betting_history.html', context)

def performance_metrics_view(request):
    # Assuming Bet model has 'stake', 'won' (boolean), and 'payout' fields
    bets = betfair_bot.objects.all()
    total_bets = bets.count()
    wins = bets.filter(won=True).count()
    losses = bets.filter(won=False).count()
    total_staked = sum(bet.stake for bet in bets)
    total_return = sum(bet.payout for bet in bets if bet.won)
    profit = total_return - total_staked
    roi = (profit / total_staked) * 100 if total_staked > 0 else 0

    performance_metrics = {
        'total_bets': total_bets,
        'wins': wins,
        'losses': losses,
        'total_staked': total_staked,
        'total_return': total_return,
        'profit': profit,
        'roi': roi,
    }

    # Render the template with performance metrics
    return render(request, 'bot/performance_metrics.html', {'performance_metrics': performance_metrics})
