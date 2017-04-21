from django import forms
from dashboard.models import FantasyPicks

class EventsForm(forms.ModelForm):

    class Meta:
        model = FantasyPicks
        fields = ['event_id', 'event_name']
