# betfair_bot/forms.pyfrom django import forms

from django import forms
from .models import BetfairData

class PlaceBetForm(forms.Form):
    market_id = forms.CharField(label='Market ID', max_length=100)
    strategy = forms.ChoiceField(label='Betting Strategy', choices=[
        ('martingale', 'Martingale'),
        ('value_betting', 'Value Betting'),
    ])
class TestingForm(forms.ModelForm):
    country_code = forms.ChoiceField(label='Country', choices=[('AU', 'Australia'), ('GB', 'Great Britain'), ('US', 'United States')])
    meeting_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)  # Add this line
    horse_barrier = forms.IntegerField(required=False) 
    class Meta:
        model = BetfairData
        fields = ['horse_barrier', 'meeting_date']  # Remove 'odds_range'