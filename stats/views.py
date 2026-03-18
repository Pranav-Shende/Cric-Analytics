# stats/views.py
from django.core.cache import cache
import requests
from django.shortcuts import render
from django.utils import timezone 
from .models import Player, BattingStat, BowlingStat, FieldingStat, Law,AllRounderStat
#from .utils import get_test_batting_rankings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import ComparePlayersForm
from .forms import DLSCalculatorForm
from .dls import dls_pre_first_innings, dls_mid_first_innings, dls_pre_second_innings, dls_mid_second_innings
import json
import os
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

# Load once at the top level of views.py (runs once on startup)
JSON_PATH = os.path.join(settings.BASE_DIR, 'stats', 'data', 'rankings.json')

with open(JSON_PATH, 'r') as f:
    RANKINGS_DATA = json.load(f)

def ipl_live_data(request):
    # This is a placeholder URL - you'll eventually use a real API key here
    api_url = "abc"
    
    # Logic: If we don't have the "Final Data" yet, we fetch it live
    try:
        response = requests.get(api_url)
        data = response.json()
        ipl_matches = data.get('data', {}).get('matchList', [])
    except Exception:
        ipl_matches = [] # Fallback if the API is down

    return render(request, 'stats/ipl_dashboard.html', {'matches': ipl_matches})

def worlcup_live_data(request):
    # This is a placeholder URL - you'll eventually use a real API key here
    api_url = "xyz"
    
    # Logic: If we don't have the "Final Data" yet, we fetch it live
    try:
        response = requests.get(api_url)
        data = response.json()
        world_cup_matches = data.get('data', {}).get('matchList', [])
    except Exception:
        world_cup_matches = [] # Fallback if the API is down

    return render(request, 'stats/world_cup_dashboard.html', {'matches': world_cup_matches})


def live_data(request):
    # 4. Fetch the key from .env using the exact name you saved it as
    api_key = os.getenv("CRICKET_API_KEY") 
    
    # 5. Build the URL using the variable
    api_url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"

    try:
        response = requests.get(api_url)
        data = response.json()
        all_matches = data.get('data', [])
    except Exception as e:
        print(f"Error fetching API: {e}")
        all_matches = []

    # ... rest of your logic stays exactly the same ...
    today = timezone.now().date().isoformat()
    today_matches = []
    # (Rest of your loop code here)
    for match in all_matches:
        match_date = match.get('dateTimeGMT') or match.get('date')
        
        if match_date and match_date.startswith(today):
            # We extract the score list safely
            scores = match.get('score', [])
            
            # Add helper keys to the match object to make HTML easier to read
            match['t1_name'] = match.get('teams', ['Team 1', ''])[0]
            match['t2_name'] = match.get('teams', ['', 'Team 2'])[1]
            
            # Map scores if they exist
            match['t1_score'] = scores[0] if len(scores) > 0 else None
            match['t2_score'] = scores[1] if len(scores) > 1 else None
            
            today_matches.append(match)

    return render(request, 'stats/live_score.html', {'matches': today_matches})

## Not working
# def official_rankings_view(request):

#     test_batters = cache.get('icc_test_batting')

#     if not test_batters:
#         test_batters = get_test_batting_rankings()
#         cache.set('icc_test_batting', test_batters, 86400)  # 24 hours

#     return render(
#         request,
#         'stats/icc_ranking.html',
#         {'test_batters': test_batters}
#     )



def icc_rankings(request):
    # Just pass the pre-loaded data to the context
    return render(request, 'stats/icc_ranking.html', {
        'rankings': RANKINGS_DATA
    })

# better than above
def player_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Scenario 1: Basic search for the name as typed
        search_filter = Q(name__icontains=query)
        
        # Scenario 2: If they type a full name like "Virat Kohli", 
        # we check for players that match "V" and "Kohli"
        parts = query.split()
        if len(parts) > 1:
            first_initial = parts[0][0] # Get 'V' from 'Virat'
            last_name = parts[-1]       # Get 'Kohli'
            search_filter |= Q(name__istartswith=first_initial) & Q(name__icontains=last_name)
        
        results = Player.objects.filter(search_filter).distinct()
    
    return render(request, 'stats/search_results.html', {'results': results, 'query': query})


from django.shortcuts import render, get_object_or_404
from .models import Player, BattingStat, BowlingStat, FieldingStat

def player_profile(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    #formats = ['Test', 'ODI', 'T20']
    # Logic to ensure a bio exists (fallback)
    if not player.ai_bio:
        # You could trigger a single generation here if needed
        pass
    
    # We fetch the stats and organize them by format for easy template access
    batting_dict = {s.format: s for s in BattingStat.objects.filter(player=player)}
    bowling_dict = {s.format: s for s in BowlingStat.objects.filter(player=player)}
    fielding_dict = {s.format: s for s in FieldingStat.objects.filter(player=player)}
    
    # context = {
    #     'player': player,
    #     'formats': formats,
    #     'batting_dict': batting_dict,
    #     'bowling_dict': bowling_dict,
    #     'fielding_dict': fielding_dict,
    # }
    # return render(request, 'stats/player_profile.html', context)
    return render(request, 'stats/player_profile.html', {
        'player': player,
        'ai_bio': player.ai_bio,
        'formats': ['Test', 'ODI', 'T20I'],
        'batting_dict': batting_dict,
        'bowling_dict': bowling_dict,
        'fielding_dict': fielding_dict,
    })


# def player_profile(request, player_id):
#     # Fetch the player or show 404 if not found
#     player = get_object_or_404(Player, id=player_id)
    
#     # Fetch all stats related to this player
#     batting = BattingStat.objects.filter(player=player)
#     bowling = BowlingStat.objects.filter(player=player)
#     fielding = FieldingStat.objects.filter(player=player)

#     context = {
#         'player': player,
#         'batting_stats': batting,
#         'bowling_stats': bowling,
#         'fielding_stats': fielding,
#     }
#     return render(request, 'stats/player_profile.html', context)

# 1. The Home Page (The Hub)
def home(request):
    return render(request, 'stats/home.html')

# 2. Batsmen Page
# def batsmen_list(request):
#     top_batters = BattingStat.objects.order_by('-runs')
#     return render(request, 'stats/batsmen.html', {'batters': top_batters})
def batsmen_list(request):
    # Fetch stats instead of players so we have the 'format' field
    batsmen_stats = BattingStat.objects.select_related('player').all().order_by('-runs')
    return render(request, 'stats/batsmen.html', {'batsmen': batsmen_stats})

# 3. Bowlers Page
def bowlers_list(request):
    stats = BowlingStat.objects.select_related('player').all().order_by('-wickets')
    return render(request, 'stats/bowlers.html', {'stats': stats, 'title': 'Bowling Rankings'})

# 4. Fielders Page
def fielders_list(request):
    stats = FieldingStat.objects.select_related('player').all().order_by('-catch')
    return render(request, 'stats/fielders.html', {'stats': stats, 'title': 'Fielding Rankings'})

# 5. All-Rounders Page (Using your simplified logic)
def all_rounders_list(request):
    stats = AllRounderStat.objects.select_related('player').all().order_by('-all_rounder_rating') # Or runs/wickets
    return render(request, 'stats/all_rounders.html', {'stats': stats, 'title': 'All-Rounder Rankings'})

# 6. Laws List (Preserving your detailed subsections)
def laws_list(request):
    laws = Law.objects.prefetch_related('subsections').all().order_by('number')
    return render(request, 'stats/laws_list.html', {'laws': laws})



# def compare_players(request):
#     p1 = None
#     p2 = None
#     p1_stats = None
#     p2_stats = None
    
#     # Check for both players and a format (defaulting to ODI)
#     form = ComparePlayersForm(request.GET or None)
#     selected_format = request.GET.get('format', 'odi').lower()

#     if form.is_valid():
#         p1 = form.cleaned_data['player1']
#         p2 = form.cleaned_data['player2']
        
#         # Fetch the BattingStat for each player in the selected format
#         p1_stats = BattingStat.objects.filter(player=p1, format=selected_format).first()
#         p2_stats = BattingStat.objects.filter(player=p2, format=selected_format).first()

#     return render(request, 'stats/compare.html', {
#         'form': form,
#         'p1': p1, 
#         'p2': p2,
#         'p1_stats': p1_stats,
#         'p2_stats': p2_stats,
#         'selected_format': selected_format
#     })

# def compare_players(request):
#     p1 = None
#     p2 = None
#     p1_stats = None
#     p2_stats = None
    
#     form = ComparePlayersForm(request.GET or None)
#     selected_format = request.GET.get('format', 'odi').strip()

#     if form.is_valid():
#         p1 = form.cleaned_data['player1']
#         p2 = form.cleaned_data['player2']
        
#         # DEBUG PRINTS: Check these in your terminal!
#         print(f"--- DLS DEBUG ---")
#         print(f"Player 1: {p1} (ID: {p1.id if p1 else 'None'})")
#         print(f"Format: '{selected_format}'")

#         # Try a broader search to see if ANYTHING exists for this player
#         p1_stats = BattingStat.objects.filter(player=p1, format__icontains=selected_format).first()
        
#         # If still None, check if stats exist AT ALL for this player
#         if not p1_stats:
#             all_stats = BattingStat.objects.filter(player=p1)
#             print(f"Stats found for this player in other formats: {[s.format for s in all_stats]}")

#         p2_stats = BattingStat.objects.filter(player=p2, format__icontains=selected_format).first()

#     return render(request, 'stats/compare.html', {
#         'form': form,
#         'p1': p1, 
#         'p2': p2,
#         'p1_stats': p1_stats,
#         'p2_stats': p2_stats,
#         'selected_format': selected_format
#     })

def compare_players(request):
    p1 = None
    p2 = None
    p1_batting = p1_bowling = p1_fielding=None
    p2_batting = p2_bowling = p2_fielding=None
    
    form = ComparePlayersForm(request.GET or None)
    selected_format = request.GET.get('format', 'odi').lower()

    if form.is_valid():
        p1 = form.cleaned_data['player1']
        p2 = form.cleaned_data['player2']
        
        # We use __icontains to be safe with 'odi' vs 'ODI'
        
        p1_batting = BattingStat.objects.filter(player=p1, format__icontains=selected_format).first()
        p1_bowling = BowlingStat.objects.filter(player=p1, format__icontains=selected_format).first()
        p1_fielding = FieldingStat.objects.filter(player=p1, format__icontains=selected_format).first()
        p2_fielding = FieldingStat.objects.filter(player=p2, format__icontains=selected_format).first()
        p2_batting = BattingStat.objects.filter(player=p2, format__icontains=selected_format).first()
        p2_bowling = BowlingStat.objects.filter(player=p2, format__icontains=selected_format).first()

    return render(request, 'stats/compare.html', {
        'form': form,
        'p1': p1, 'p2': p2,
        'p1_batting': p1_batting, 'p1_bowling': p1_bowling,'p1_fielding': p1_fielding,
        'p2_batting': p2_batting, 'p2_bowling': p2_bowling,'p2_fielding': p2_fielding,
        'selected_format': selected_format,
    })

def dls_calculator(request):
    result = None
    scenario = None
    form = DLSCalculatorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        scenario = data['scenario']
        fmt = data['format']
        delay = data.get('delay_minutes') or 0

        try:
            if scenario == "pre1":
                result = dls_pre_first_innings(fmt, delay)
            elif scenario == "mid1":
                result = dls_mid_first_innings(fmt, data['overs_bowled'], data['wickets_lost'], delay)
            elif scenario == "pre2":
                result = dls_pre_second_innings(fmt, data['team1_score'], delay)
            elif scenario == "mid2":
                result = dls_mid_second_innings(fmt, data['team1_score'], data['team2_score'], 
                                               data['overs_bowled'], data['wickets_lost'], delay)
        except Exception as e:
            result = {"error": str(e)}

    return render(request, 'stats/dls.html', {'form': form, 'result': result, 'scenario': scenario})