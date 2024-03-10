from django.db import models
from django.contrib.auth.models import User

class Market(models.Model):
    market_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    # Add more fields as necessary

    def __str__(self):
        return self.name

class Bet(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional, if tracking users
    selection = models.CharField(max_length=255)
    stake = models.DecimalField(max_digits=6, decimal_places=2)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    won = models.BooleanField(default=False)
    payout = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.selection} - {'Won' if self.won else 'Lost'}"

    @property
    def calculate_profit(self):
        """Calculate profit for this bet."""
        if self.won:
            return self.payout - self.stake
        return -self.stake

    class Meta:
        ordering = ['-market__start_time']

from django.db import models

class Horse(models.Model):
    name = models.CharField(max_length=255)
    odds = models.FloatField(help_text="Decreasing odds show more people betting on this horse")
    current_form = models.CharField(max_length=255)
    barrier = models.IntegerField()
    track_conditions = models.CharField(max_length=255)
    race_location = models.CharField(max_length=255)
    jockey = models.CharField(max_length=255)
    trainer = models.CharField(max_length=255)

def calculate_chance(self):
        # Example calculation - adjust weights and formula as needed
        # These are placeholder calculations. You'll need to replace them with your own logic.
        odds_weight = 0.4
        form_weight = 0.3
        conditions_weight = 0.2
        location_weight = 0.05
        jockey_trainer_weight = 0.05
        
        # Example scoring logic. Replace with your actual scoring based on the horse's data.
        score = (self.odds * odds_weight) + (self.get_form_score() * form_weight) + \
                (self.get_conditions_score() * conditions_weight) + \
                (self.get_location_score() * location_weight) + \
                (self.get_jockey_trainer_score() * jockey_trainer_weight)
        
        # Example conversion of score to percentage chance. Adjust as necessary.
        percentage_chance = max(0, min(100, score))  # Ensure result is between 0 and 100
        return percentage_chance

def chance_color(self):
        chance = self.calculate_chance()
        if chance <= 25:
            return 'darkred'
        elif chance <= 50:
            return 'lightred'
        elif chance <= 65:
            return 'orange'
        elif chance <= 80:
            return 'yellow'
        elif chance <= 90:
            return 'lightgreen'
        else:
            return 'darkgreen'
    
    # Placeholder methods for converting various attributes to scores.
    # These methods should contain logic to convert each attribute into a score.
def get_form_score(self):
        """
        Convert current form to a score.
        
        Assumes current_form is a string of recent finishes, e.g., '1-3-2'.
        Lower scores are better (1 is best possible score).
        """
        form_scores = {
            '1': 1,  # Win
            '2': 2,  # Second place
            '3': 3,  # Third place
            # Define more as needed
        }
        max_score_per_race = max(form_scores.values()) + 1  # Beyond last defined score
        
        # Split the form string into individual performances
        performances = self.current_form.split('-')
        
        # Calculate the score
        score = 0
        for i, performance in enumerate(performances, start=1):
            # Convert each race finish to a score, unknown finishes get the worst score
            race_score = form_scores.get(performance, max_score_per_race)
            # Apply weighting by race recency (most recent race has a multiplier of 1)
            weighted_score = race_score * (len(performances) - i + 1)
            score += weighted_score
        
        # Normalize the score to be out of 100, or another suitable scale
        # This is simplistic normalization for demonstration
        normalized_score = (score / (len(performances) * max_score_per_race * len(performances))) * 100
        
        return normalized_score

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

def __str__(self):
        return self.name

class Track(models.Model):
    METROPOLITAN = 'Metropolitan'
    COUNTRY = 'Country'
    OTHER = 'Other'
    
    TRACK_TYPES = [
        (METROPOLITAN, 'Metropolitan'),
        (COUNTRY, 'Country'),
        (OTHER, 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    track_type = models.CharField(max_length=12, choices=TRACK_TYPES, default=OTHER)

def get_track_rating(self):
        """
        Rates tracks based on type: Metropolitan > Country > Other.
        Returns a numerical rating with Metropolitan tracks rated highest, 
        followed by Country, and Other types are rated the lowest.
        """
        track_ratings = {
            self.METROPOLITAN: 100,
            self.COUNTRY: 75,
            self.OTHER: 50,
        }
        
        return track_ratings.get(self.track_type, 0)  # Default rating if track type is somehow not listed

def __str__(self):
        return f"{self.name} ({self.location}) - {self.track_type}"

