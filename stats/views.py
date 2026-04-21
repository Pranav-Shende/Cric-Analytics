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
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv
import pandas as pd
import json
import os
import re
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

# For every match happening around the world
# def live_data(request):
#     # 4. Fetch the key from .env using the exact name you saved it as
#     api_key = os.getenv("CRICKET_API_KEY") 
    
#     # 5. Build the URL using the variable
#     api_url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"

#     try:
#         response = requests.get(api_url)
#         data = response.json()
#         all_matches = data.get('data', [])
#     except Exception as e:
#         print(f"Error fetching API: {e}")
#         all_matches = []

#     # ... rest of your logic stays exactly the same ...
#     today = timezone.now().date().isoformat()
#     today_matches = []
#     # (Rest of your loop code here)
#     for match in all_matches:
#         match_date = match.get('dateTimeGMT') or match.get('date')
        
#         if match_date and match_date.startswith(today):
#             # We extract the score list safely
#             scores = match.get('score', [])
            
#             # Add helper keys to the match object to make HTML easier to read
#             match['t1_name'] = match.get('teams', ['Team 1', ''])[0]
#             match['t2_name'] = match.get('teams', ['', 'Team 2'])[1]
            
#             # Map scores if they exist
#             match['t1_score'] = scores[0] if len(scores) > 0 else None
#             match['t2_score'] = scores[1] if len(scores) > 1 else None
            
#             today_matches.append(match)

#     return render(request, 'stats/live_score.html', {'matches': today_matches})

#Changed due to api change
# For only selected teams
# def live_data(request):
#     api_key = os.getenv("CRICKET_API_KEY") 
#     api_url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"

#     # 1. List of International Countries
#     INTERNATIONAL_TEAMS = [
#         "INDIA", "AUSTRALIA", "PAKISTAN", "ENGLAND", "SOUTH AFRICA", 
#         "NEW ZEALAND", "WEST INDIES", "SRI LANKA", "BANGLADESH", 
#         "AFGHANISTAN", "IRELAND", "ZIMBABWE", "NEPAL", "NETHERLANDS"
#     ]

#     # 2. List of Big League Teams (IPL, BBL, etc.)
#     LEAGUE_TEAMS = [
#          "Mumbai Indians","Chennai Super Kings [CSK]","Royal Challengers Bangalore","Kolkata Knight Riders",
#          "Gujarat Titans","Rajasthan Royals","Lucknow Super Giants","Delhi Capitals","Punjab Kings",
#          "Sunrisers Hyderabad","Adelaide Strikers","Brisbane Heat","Hobart Hurricanes","Melbourne Renegades",
#          "Melbourne Stars","Perth Scorchers","Sydney Sixers","Sydney Thunders"# Add more teams here
#     ]

#     try:
#         response = requests.get(api_url)
#         data = response.json()
#         all_matches = data.get('data', [])
#     except Exception as e:
#         all_matches = []

#     today = timezone.now().date().isoformat()
#     filtered_matches = []

#     for match in all_matches:
#         match_date = match.get('dateTimeGMT') or match.get('date')
        
#         # Extract team names from the match name (e.g., "India vs Australia")
#         # or from the 'teams' list if the API provides it.
#         teams_list = match.get('teams', [])
#         t1 = teams_list[0].upper() if len(teams_list) > 0 else ""
#         t2 = teams_list[1].upper() if len(teams_list) > 1 else ""

#         if match_date and match_date.startswith(today):
            
#             # Check if EITHER team is an International team OR a Big League team
#             is_international = any(team in t1 or team in t2 for team in INTERNATIONAL_TEAMS)
#             is_league = any(team in t1 or team in t2 for team in LEAGUE_TEAMS)

#             if is_international or is_league:
#                 scores = match.get('score', [])
#                 match['t1_name'] = t1.title() # Convert back to 'India' from 'INDIA'
#                 match['t2_name'] = t2.title()
                
#                 match['t1_score'] = scores[0] if len(scores) > 0 else None
#                 match['t2_score'] = scores[1] if len(scores) > 1 else None
                
#                 filtered_matches.append(match)

#     return render(request, 'stats/live_score.html', {'matches': filtered_matches})
def live_data(request):
    api_key = os.getenv("CRICKET_API_KEY") 
    api_url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"

    # Use shorter keywords to ensure matches (e.g., 'MUMBAI' instead of 'MUMBAI INDIANS')
    ELITE_KEYWORDS = [
        "INDIA", "AUSTRALIA", "PAKISTAN", "ENGLAND", "SOUTH AFRICA", 
        "NEW ZEALAND", "WEST INDIES", "SRI LANKA", "BANGLADESH", 
        "AFGHANISTAN", "IRELAND", "ZIMBABWE", "NEPAL", "NETHERLANDS",
        "MUMBAI Indians", "CHENNAI Super Kings", "Royal Challengers BANGALORE", "KOLKATA Knight Riders", "GUJARAT Titans", 
        "RAJASTHAN Royals", "LUCKNOW Super Giants", "DELHI Capital", "PUNJAB Kings", "Sunrisers HYDERABAD"
        
    ]

    try:
        response = requests.get(api_url)
        data = response.json()
        all_matches = data.get('data', [])
        # print(f"DEBUG: API returned {len(all_matches)} matches total.") # Check Render logs
    except Exception as e:
        all_matches = []

    filtered_matches = []

    def format_score_dict(s_list, index):
        if not s_list or len(s_list) <= index:
            return "Yet to bat"
        s = s_list[index]
        # Handle the new dictionary format: {'r': 198, 'w': 10, 'o': 76.4}
        runs = s.get('r', 0)
        wickets = s.get('w', 10)
        overs = s.get('o', 0)
        return f"{runs}/{wickets} ({overs})"

    for match in all_matches:
        match_name = match.get('name', '').upper()
        
        # Check if this match contains ANY of our elite keywords
        is_important = any(word in match_name for word in ELITE_KEYWORDS)

        if is_important:
            
            scores_data = match.get('score', [])
            teams = match.get('teams', ['T1', 'T2'])
            
            # Use .get() to avoid index errors if teams list is short
            match['t1_name'] = teams[0] if len(teams) > 0 else "Team 1"
            match['t2_name'] = teams[1] if len(teams) > 1 else "Team 2"
            
            match['t1_score'] = format_score_dict(scores_data, 0)
            match['t2_score'] = format_score_dict(scores_data, 1)
            
            # Status and Venue for better UI
            match['current_status'] = match.get('status', 'Scheduled')
            match['match_venue'] = match.get('venue', 'Unknown Venue')
            
            search_query = f"{match['t1_name']} vs {match['t2_name']} live scorecard google".replace(" ", "+")
            match['external_link'] = f"https://www.google.com/search?q={search_query}"
            filtered_matches.append(match)

    return render(request, 'stats/live_score.html', {'matches': filtered_matches})

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
    
    return render(request, 'stats/player_profile.html', {
        'player': player,
        'ai_bio': player.ai_bio,
        'formats': ['Test', 'ODI', 'T20I'],
        'batting_dict': batting_dict,
        'bowling_dict': bowling_dict,
        'fielding_dict': fielding_dict,
    })


# 1. The Home Page (The Hub)
def home(request):
    return render(request, 'stats/home.html')

# 2. Batsmen Page

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


# def ipl_standing(request):
#     try:
#         # Read the latest scraped data
#         df = pd.read_csv('ipl_points_latest.csv')
        
#         # Convert to a list of dictionaries
#         standings_data = df.to_dict(orient='records')
        
#         # Get the last updated time from the first row
#         last_updated = df['SCRAPED_AT'].iloc[0] if not df.empty else "N/A"
        
#         context = {
#             'standings': standings_data,
#             'last_updated': last_updated
#         }
#         return render(request, 'stats/standings.html', context)
#     except FileNotFoundError:
#         return render(request, 'stats/standings.html', {'error': 'No data available yet.'})

import pandas as pd
from django.shortcuts import render
import re

def ipl_standing(request):
    csv_path = os.path.join(settings.BASE_DIR, 'ipl_points_latest.csv')
    
    try:
        # Check if file exists first to avoid crash
        if not os.path.exists(csv_path):
             return render(request, 'stats/ipl_standing.html', {'error': 'Data file not found.'})
        df = pd.read_csv(csv_path)
        
        # 1. Fix the POS and TEAMS columns
        if 'TEAMS' in df.columns:
            # Step A: Extract the leading digits from TEAMS and put them into POS
            # This handles strings like "1Punjab Kings" or "10Mumbai Indians"
            df['POS'] = df['TEAMS'].apply(lambda x: re.findall(r'^\d+', str(x))[0] if re.findall(r'^\d+', str(x)) else "N/A")
            
            # Step B: Now remove those digits from the TEAMS column
            df['TEAMS'] = df['TEAMS'].apply(lambda x: re.sub(r'^\d+', '', str(x)).strip())

        # 2. Fix the 'SERIES_FORM' for "NR" logic
        if 'SERIES_FORM' in df.columns:
            def clean_form(form_str):
                # Standardize to "NR" and remove spaces
                cleaned = str(form_str).replace('N R', 'NR').replace(' ', '')
                # Split but keep "NR" as one unit
                return re.findall(r'NR|[WLD]', cleaned)
            
            df['SERIES_FORM'] = df['SERIES_FORM'].apply(clean_form)

        standings_data = df.to_dict(orient='records')
        last_updated = df['SCRAPED_AT'].iloc[0] if not df.empty else "N/A"
        
        context = {
            'standings': standings_data,
            'last_updated': last_updated
        }
        return render(request, 'stats/ipl_standing.html', context)

    except (FileNotFoundError, pd.errors.EmptyDataError):
        return render(request, 'stats/ipl_standing.html', {'error': 'Data not found.'})
    



# For Cron Job

from django.core.management import call_command
from django.http import HttpResponse, HttpResponseForbidden

def trigger_scraper(request):
    # Security: Use a secret key in the URL so strangers can't spam your scraper
    secret_key = request.GET.get('key')
    if secret_key != "your_very_secret_password_123":
        return HttpResponseForbidden("Invalid Secret Key")

    try:
        # This runs the 'python manage.py scrape_ipl' command internally
        call_command('scrape_ipl')
        return HttpResponse("Scraper executed successfully!")
    except Exception as e:
        return HttpResponse(f"Scraper failed: {str(e)}", status=500)