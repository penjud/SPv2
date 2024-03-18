import betfairlightweight
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from betfairlightweight import APIClient
from betfairlightweight.filters import market_filter
from betfairlightweight.exceptions import APIError
import os
import logging
from django.core.paginator import Paginator
from betfair_bot.models import Bet
from betfair_bot.forms import PlaceBetForm, TestingForm
from django.conf import settings
from betfairlightweight.exceptions import APIError, PasswordError, AppKeyError
from betfairlightweight.filters import market_filter
from betfair_bot.betfair_api import BetfairAPI
from django.http import request
from betfair_bot.models import BetfairData
from django import forms
from .forms import TestingForm  # Make sure this is the correct import for your form

# Create a logger
logger = logging.getLogger(__name__)

@login_required
def home(request):
    is_api_connected = False
    error_message = None

    try:
        betfair_api = BetfairAPI()
        betfair_api.cert_path = settings.BETFAIR_CERTS_PATH
        betfair_api.initialize_api_client()
        is_api_connected = True
        betfair_api.close_connection()

        # Initialize the APIClient with necessary credentials
        api_client = betfairlightweight.APIClient(
            username=settings.BETFAIR_USERNAME,
            password=settings.BETFAIR_PASSWORD,
            app_key=settings.BETFAIR_APP_KEY,
            certs=settings.BETFAIR_CERTS_PATH
        )

        # Assuming the library requires manual login
        api_client.login()
        logger.debug("Logged in to Betfair API successfully.")

        # Fetch market data using the API client
        market_data = api_client.betting.list_market_catalogue(
            filter=market_filter(text_query='horse racing'),
            market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION'],
            max_results=10
        )

        context = {
            'welcome_message': 'Welcome to SickPunt!',
            'features': ['Automatic betting', 'Real-time statistics', 'User-friendly interface'],
            'is_api_connected': is_api_connected,
            'market_data': market_data
        }

    except APIError as e:
        logger.error(f"APIError encountered: {e}")
        error_message = "API Error occurred while trying to connect to Betfair API."

    except Exception as e:
        logger.error(f"Failed to connect to Betfair API: {str(e)}")
        error_message = "An unexpected error occurred while trying to connect to Betfair API."

    if error_message:
        messages.error(request, error_message)

    context = {
        'welcome_message': 'Welcome to SickPunt!',
        'features': ['Automatic betting', 'Real-time statistics', 'User-friendly interface'],
        'is_api_connected': is_api_connected,
        'error_message': error_message
    }

    return render(request, 'bot/home.html', context)

@login_required
def testing_view(request):
    if request.method == 'POST':
        form = TestingForm(request.POST)
        if form.is_valid():
            country_code = form.cleaned_data.get('country_code')
            meeting_date = form.cleaned_data.get('meeting_date')
            horse_barrier = form.cleaned_data.get('horse_barrier')
            

            historical_data = BetfairData.objects.filter(
                country_code=country_code,
                meeting_date=meeting_date,
                horse_barrier=horse_barrier,  # Assuming this is the correct field name
                
            )

            context = {
                'form': form,
                'historical_data': historical_data,
            }

            logger.debug(f"Filtering with country_code={country_code}, meeting_date={meeting_date}, horse_barrier={horse_barrier}")
            return render(request, 'bot/testing.html', context)
    else:
        form = TestingForm()  # or PlaceBetForm() based on what you want to display initially

    # If it's a GET request or the form is not valid, render the page with the empty or unvalidated form
    return render(request, 'bot/testing.html', {'form': form})


def filter_data(request, form, historical_data):
    # Implement the logic for filtering data
    pass

def my_function(request, form, historical_data):
    return filter_data(request, form, historical_data)

def my_view(request):
    form = PlaceBetForm()  # Define the "form" variable
    historical_data = None  # Define the "historical_data" variable
    return render(request, 'bot/testing.html', {'form': form})

form = PlaceBetForm()  # Define the "form" variable
historical_data = None  # Define the "historical_data" variable
my_function(request, form, historical_data)

def race_selection(request):
    betfair_api = BetfairAPI()
    races = betfair_api.get_races()  # Implement the get_races() method in the BetfairAPI class
    return render(request, 'race_selection.html', {'races': races})

@login_required
def place_bet(request):
    if request.method == 'POST':
        form = PlaceBetForm(request.POST)
        if form.is_valid():
            market_id = form.cleaned_data['market_id']
            strategy_name = form.cleaned_data['strategy']
            betfair_username = request.user.profile.betfair_username
            betfair_password = request.user.profile.betfair_password
            betfair_api_key = request.user.profile.betfair_api_key
            
            # Use the user's Betfair API details to place the bet
            # ...
            
            messages.success(request, 'Your bet has been placed!')
            return redirect('betting_history')
    else:
        form = PlaceBetForm()
    return render(request, 'betfair_bot/place_bet.html', {'form': form})

@login_required
def market_data_view(request):
    try:
        api_client = APIClient(
            username=settings.BETFAIR_USERNAME,
            password=settings.BETFAIR_PASSWORD,
            app_key=settings.BETFAIR_APP_KEY,
            certs=settings.BETFAIR_CERTS_PATH
        )

        api_client.login()

        market_data = api_client.betting.list_market_catalogue(
            filter=market_filter(text_query='horse racing'),
            market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION'],
            max_results=10
        )

        api_client.logout()

    except APIError as e:
        market_data = []
        logger.error(f"Error fetching market data: {str(e)}")

    return render(request, 'bot/market_data.html', {'market_data': market_data})

@login_required
def betting_history(request):
    bets_list = Bet.objects.all().order_by('-id')
    paginator = Paginator(bets_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'bot/betting_history.html', context)

@login_required
def performance_metrics_view(request):
    bets = Bet.objects.all()
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

    return render(request, 'bot/performance_metrics.html', {'performance_metrics': performance_metrics})