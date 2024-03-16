# betfair_bot/forms.pyfrom django import forms

from django import forms

class PlaceBetForm(forms.Form):
    market_id = forms.CharField(label='Market ID', max_length=100)
    strategy = forms.ChoiceField(label='Betting Strategy', choices=[
        ('martingale', 'Martingale'),
        ('value_betting', 'Value Betting'),
    ])

class TestingForm(forms.Form):
    barrier_number = forms.IntegerField(label='Barrier Number')
    track_conditions = forms.ChoiceField(label='Track Conditions', choices=[('good', 'Good'), ('soft', 'Soft'), ('heavy', 'Heavy')])
    odds_range = forms.CharField(label='Odds Range', help_text='Enter the odds range in the format: min-max')   # Add other form fields as needed