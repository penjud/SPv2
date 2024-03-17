# betfair_bot/forms.pyfrom django import forms

from django import forms
from django.db import models
from .models import BetfairData
from django.forms import SelectDateWidget
import datetime

class PlaceBetForm(forms.Form):
    market_id = forms.CharField(label='Market ID', max_length=100)
    strategy = forms.ChoiceField(label='Betting Strategy', choices=[
        ('martingale', 'Martingale'),
        ('value_betting', 'Value Betting'),
    ])
class TestingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        current_year = datetime.datetime.now().year
        self.fields['meeting_date'].widget = SelectDateWidget(years=range(2001, current_year + 1))

    class Meta:
        model = BetfairData
        fields = ['country_code', 'meeting_date', 'horse_barrier']  # Specify the order here
    country_code = forms.ChoiceField(label='Country', choices=[('AU', 'Australia'), ('GB', 'Great Britain'), ('US', 'United States')])
    meeting_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)  # Add this line
    horse_barrier = forms.IntegerField(label='Horse Barrier',required=False)  # Fix the label value