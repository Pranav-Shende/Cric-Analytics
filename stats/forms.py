from django import forms
from .models import Player

class ComparePlayersForm(forms.Form):
    # We use ModelChoiceField to get a dropdown of all players
    player1 = forms.ModelChoiceField(
        queryset=Player.objects.all().order_by('name'),
        label="Select Player 1",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    player2 = forms.ModelChoiceField(
        queryset=Player.objects.all().order_by('name'),
        label="Select Player 2",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

# SCENARIO_CHOICES = [
#     ('pre1', 'Pre-First Innings'),
#     ('mid1', 'Mid-First Innings'),
#     ('pre2', 'Pre-Second Innings'),
#     ('mid2', 'Mid-Second Innings'),
# ]

# FORMAT_CHOICES = [('odi', 'ODI'), ('t20', 'T20')]

# class DLSCalculatorForm(forms.Form):
#     scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
#     format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
#     team1_score = forms.IntegerField(required=False, label="Team 1 Score")
#     team2_score = forms.IntegerField(required=False, label="Team 2 Score")
#     overs_bowled = forms.FloatField(required=False, label="Overs Bowled (e.g. 10.2)")
#     wickets_lost = forms.IntegerField(required=False, label="Wickets Lost")
#     delay_minutes = forms.IntegerField(required=False, label="Delay (Minutes)")
#from django import forms

# class DLSCalculatorForm(forms.Form):
#     scenario = forms.ChoiceField(widget=forms.Select(attrs={'id': 'scenario'}))
#     # scenario = forms.ChoiceField(
#     #     choices=[('pre1', 'Pre-First Innings'), ('mid1', 'Mid-First Innings'), 
#     #              ('pre2', 'Pre-Second Innings'), ('mid2', 'Mid-Second Innings')],
#     #     widget=forms.Select(attrs={'id': 'scenario', 'class': 'form-select'})
#     # )
#     format = forms.ChoiceField(
#         choices=[('odi', 'ODI'), ('t20', 'T20')],
#         widget=forms.Select(attrs={'id': 'format', 'class': 'form-select'})
#     )
#     team1_score = forms.IntegerField(
#         required=False, 
#         widget=forms.NumberInput(attrs={'id': 'team1-score', 'class': 'form-control'})
#     )
#     team2_score = forms.IntegerField(
#         required=False, 
#         widget=forms.NumberInput(attrs={'id': 'team2-score', 'class': 'form-control'})
#     )
#     overs_bowled = forms.FloatField(
#         required=False, 
#         widget=forms.NumberInput(attrs={'id': 'overs-bowled', 'class': 'form-control', 'step': '0.1'})
#     )
#     wickets_lost = forms.IntegerField(
#         required=False, 
#         widget=forms.NumberInput(attrs={'id': 'wickets-lost', 'class': 'form-control'})
#     )
#     delay_minutes = forms.IntegerField(
#         required=False, 
#         widget=forms.NumberInput(attrs={'id': 'delay', 'class': 'form-control'})
#     )


from django import forms

class DLSCalculatorForm(forms.Form):
    scenario = forms.ChoiceField(
        choices=[('pre1', 'Pre-First'), ('mid1', 'Mid-First'), ('pre2', 'Pre-Second'), ('mid2', 'Mid-Second')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    format = forms.ChoiceField(
        choices=[('odi', 'ODI'), ('t20', 'T20')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    team1_score = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    team2_score = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    overs_bowled = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}))
    wickets_lost = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    delay_minutes = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))