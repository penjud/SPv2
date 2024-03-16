from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from betfairlightweight import APIClient
from betfairlightweight.filters import market_filter
from betfairlightweight.exceptions import APIError
import os
import logging
from django.core.paginator import Paginator
import betfair_bot
from betfair_bot.models import Bet
from betfair_bot.forms import PlaceBetForm
from bot.bot_logic import MartingaleStrategy, ValueBettingStrategy
from betfair_bot.forms import TestingForm
from betfair_bot.models import BetfairData

# Create a logger
logger = logging.getLogger(__name__)

# Example form class for placing a bet
class PlaceBetForm(forms.Form):
    bet_amount = forms.DecimalField(min_value=0.01)
    selected_horse = forms.ChoiceField(choices=[('Horse 1', 'Horse 1'), ('Horse 2', 'Horse 2'), ('Horse 3', 'Horse 3')])

@login_required
def home(request):
    # Context to pass to the template
    context = {
        'welcome_message': 'Welcome to our betting bot!',
        'features': ['Automatic betting', 'Real-time statistics', 'User-friendly interface'],
    }
    return render(request, 'bot/home.html', context)

@login_required
def testing_view(request):
    if request.method == 'POST':
        form = TestingForm(request.POST)
        if form.is_valid():
            barrier_number = form.cleaned_data['barrier_number']
            track_conditions = form.cleaned_data['track_conditions']
            odds_range = form.cleaned_data['odds_range']
            
            # Query the historical data based on the selected criteria
            historical_data = BetfairData.objects.filter(
                barrier_number=barrier_number,
                track_conditions=track_conditions,
                odds__range=odds_range
            )

            # Perform testing logic here
            # ...

            context = {
                'form': form,
                'historical_data': historical_data,
            }
            return render(request, 'betfair_bot/templates/testing_results.html', context)
    else:
        form = TestingForm()
    
    context = {
        'form': form,
    }
    return render(request, 'betfair_bot/templates/testing.html', context)

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

@login_required
def betting_history (request):
    bets_list = Bet.objects.all().order_by('-id')
    paginator = Paginator(bets_list, 10)  # Show 10 bets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'bot/betting_history.html', context)

@login_required
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

@login_required
def get_conditions_score(self):
        """
        Convert track conditions to a score based on the horse's performance tendency.
        
        This method assumes the horse has a tendency to perform better on certain types of tracks.
        Scores are hypothetical and should be adjusted based on real data or more detailed criteria.
        """
        conditions_scores = {
            'Fast': 90,
            'Good': 80,
            'Soft': 70,
            'Heavy': 60,
        }

        # Assuming `self.track_conditions` is one of 'Fast', 'Good', 'Soft', 'Heavy'
        # Adjust the condition scores above according to the horse's performance history or known preferences
        # For simplicity, we directly return the score associated with the current track conditions
        # In a more sophisticated model, you might adjust these scores based on detailed performance data
        return conditions_scores.get(self.track_conditions, 50)  # Default score if condition is unknown

@login_required
def get_location_score(self):
        """
        Convert race location to a score based on the horse's preference or performance history.
        
        Scores are hypothetical and should be adjusted based on real performance data or more detailed criteria.
        """
        location_scores = {
            'Track A': 90,  # Assuming this horse performs well at Track A
            'Track B': 75,
            'Track C': 60,
            'Track D': 45,  # Assuming this horse performs less well at Track D
        }

        # Assuming `self.race_location` is the name of the track where the race will occur
        # Return the score associated with the horse's current race location
        # In a more sophisticated model, this might be adjusted based on detailed historical performance data at each location
        return location_scores.get(self.race_location, 50)  # Default score if location is unknown or not listed

        jockey = models.CharField(max_length=255)
        trainer = models.CharField(max_length=255)

@login_required
def get_jockey_trainer_score(self):
        """
        Convert jockey and trainer information to a score based on their historical performance and influence.
        
        This method uses hypothetical scoring logic. Adjust the implementation based on actual data and criteria.
        """
        # Example: Hypothetical performance ratings or win rates for jockeys and trainers
        jockey_performance = {
            'Jockey A': 90,
            'Jockey B': 80,
            # Add more as necessary
        }
        
        trainer_performance = {
            'Trainer X': 90,
            'Trainer Y': 85,
            # Add more as necessary
        }
        
        # Retrieve scores or ratings based on the current jockey and trainer
        jockey_score = jockey_performance.get(self.jockey, 75)  # Default score if jockey is unknown
        trainer_score = trainer_performance.get(self.trainer, 75)  # Default score if trainer is unknown
        
        # Combine jockey and trainer scores. Adjust weighting as necessary based on their perceived influence.
        combined_score = (jockey_score * 0.5) + (trainer_score * 0.5)
        
        # Normalize or adjust the combined score as necessary to fit your scoring system
        return combined_score

def __str__(self):
        return self.name