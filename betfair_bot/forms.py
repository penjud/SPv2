# betfair_bot/forms.py

from django import forms

class PlaceBetForm(forms.Form):
    market_id = forms.CharField(label='Market ID', max_length=100)
    strategy = forms.ChoiceField(label='Betting Strategy', choices=[
        ('martingale', 'Martingale'),
        ('value_betting', 'Value Betting'),
    ])
    # Add other form fields as needed