# import requests
#from bs4 import BeautifulSoup

# def get_icc_rankings(category='batting', format='test'):
#     # URL structure for ICC rankings
#     url = f"https://www.icc-cricket.com/rankings/mens/player-rankings/{format}/{category}"
    
#     # We must use a 'User-Agent' header so the website doesn't block our request
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
    
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     rankings = []
    
#     # The ICC website uses a specific table class for its rankings
#     table = soup.find('table', class_='table')
#     if table:
#         rows = table.find_all('tr')[1:11]  # Get the top 10 rows (skipping header)
#         for row in rows:
#             cols = row.find_all('td')
#             if len(cols) >= 3:
#                 rankings.append({
#                     'rank': cols[0].text.strip(),
#                     'name': cols[1].text.strip(),
#                     'rating': cols[4].text.strip() if len(cols) > 4 else cols[3].text.strip(),
#                 })
#     return rankings


# import requests
# from bs4 import BeautifulSoup

# def get_icc_rankings(category='batting', format='test'):
#     # Correct 2026 URL structure
#     url = f"https://www.icc-cricket.com/rankings/{category}/mens/{format}"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
#     }
    
#     try:
#         response = requests.get(url, headers=headers, timeout=15)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         rankings = []

#         # 1. Target the Rank 1 Player (Modern 'banner' structure)
#         banner = soup.find('div', class_='rankings-block__banner')
#         if banner:
#             name_div = banner.find('div', class_=['rankings-block__banner--name-large', 'name'])
#             team_div = banner.find('div', class_=['rankings-block__banner--nationality', 'country'])
#             rating_div = banner.find('div', class_=['rankings-block__banner--rating', 'rating'])
            
#             if name_div:
#                 rankings.append({
#                     'rank': '1',
#                     'name': name_div.text.strip(),
#                     'team': team_div.text.strip() if team_div else "N/A",
#                     'rating': rating_div.text.strip() if rating_div else "0"
#                 })

#         # 2. Target Ranks 2-10 (Modern 'table-body' structure)
#         # Using a list of potential classes because ICC uses variations
#         rows = soup.find_all('tr', class_=['table-body', 'ranking-list__item'])
        
#         for row in rows[:9]:
#             cells = row.find_all('td')
#             if len(cells) >= 3:
#                 rankings.append({
#                     'rank': cells[0].text.strip().split('\n')[0],
#                     'name': cells[1].text.strip().replace('\n', ' '),
#                     'team': cells[2].text.strip(),
#                     'rating': cells[3].text.strip() if len(cells) > 3 else "0"
#                 })
        
#         return rankings
#     except Exception as e:
#         print(f"DEBUG: Scraper Error - {e}")
#         return []


import requests
from bs4 import BeautifulSoup

def get_test_batting_rankings():
    url = "https://www.icc-cricket.com/rankings/batting/mens/test"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rankings = []

    # 🔹 Rank 1 player (separate banner block)
    banner = soup.find("div", class_="rankings-block__banner")

    if banner:
        name = banner.find("div", class_="rankings-block__banner--name-large")
        country = banner.find("div", class_="rankings-block__banner--nationality")
        rating = banner.find("div", class_="rankings-block__banner--rating")

        rankings.append({
            "rank": 1,
            "name": name.text.strip() if name else "N/A",
            "country": country.text.strip() if country else "N/A",
            "rating": rating.text.strip() if rating else "N/A"
        })

    # 🔹 Rank 2–10 players
    rows = soup.find_all("tr", class_="table-body")

    for row in rows[:9]:  # Top 10 only
        rank = row.find("td", class_="table-body__cell table-body__cell--position")
        name = row.find("a", class_="table-body__cell-name")
        country = row.find("span", class_="table-body__logo-text")
        rating = row.find("td", class_="table-body__cell table-body__cell--rating")

        rankings.append({
            "rank": rank.text.strip() if rank else "N/A",
            "name": name.text.strip() if name else "N/A",
            "country": country.text.strip() if country else "N/A",
            "rating": rating.text.strip() if rating else "N/A"
        })

    return rankings


# ✅ Test it
if __name__ == "__main__":
    data = get_test_batting_rankings()
    for player in data:
        print(player)



# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# from .models import Player
# import time

# # Load variables from .env
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def get_player_insight(player_name, country, batting_avg):
#     """Generates a bio for a single player (used during on-the-fly updates)."""
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     prompt = (f"Act as a cricket historian. Provide a 2-line interesting career summary "
#               f"for {player_name} from {country}. They have a batting average of {batting_avg}.")
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception:
#         return "Insight currently unavailable."

# def generate_all_bios():
#     """Bulk updates all players in the database who are missing a bio."""
#     players = Player.objects.filter(ai_bio__isnull=True)
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     for player in players:
#         # We try to find a batting average to give the AI more context
#         # This assumes you have a relationship set up
#         avg = "N/A"
#         if hasattr(player, 'battingstat_set'):
#             stat = player.battingstat_set.first()
#             if stat: avg = stat.average

#         prompt = f"Write a 2-line professional career summary for {player.name} from {player.country}. Avg: {avg}."
#         try:
#             response = model.generate_content(prompt)
#             player.ai_bio = response.text.strip()
#             player.save()
#             print(f"✅ Saved bio for {player.name}")
#         except Exception as e:
#             print(f"❌ Error for {player.name}: {e}")
#         time.sleep(4)
# def generate_all_bios():
#     """Bulk updates all players with comprehensive stats."""
#     players = Player.objects.filter(ai_bio__isnull=True)
#     # Using the updated model name to avoid the 404 error
#     model = genai.GenerativeModel('gemini-2.5-flash') 
    
#     for player in players:
#         # 1. Gather Batting Stats
#         bat_avg = "N/A"
#         if hasattr(player, 'battingstat_set'):
#             b_stat = player.battingstat_set.first()
#             if b_stat: bat_avg = b_stat.average

#         # 2. Gather Bowling Stats
#         bowl_wkts = "N/A"
#         bowl_avg = "N/A"
#         if hasattr(player, 'bowlingstat_set'):
#             w_stat = player.bowlingstat_set.first()
#             if w_stat:
#                 bowl_wkts = w_stat.wickets
#                 bowl_avg = w_stat.average

#         # 3. Create a comprehensive prompt
#         prompt = (
#             f"Write a 2-line professional career summary for {player.name} from {player.country}. "
#             f"Stats: Batting Avg {bat_avg}, Bowling Wkts {bowl_wkts}, Bowling Avg {bowl_avg}. "
#             f"Identify if they are a specialist batsman, bowler, or all-rounder."
#         )

#         try:
#             response = model.generate_content(prompt)
#             player.ai_bio = response.text.strip()
#             player.save()
#             print(f"✅ Saved balanced bio for {player.name}")
#         except Exception as e:
#             print(f"❌ Error for {player.name}: {e}")
        
#         time.sleep(4) # Staying within Free Tier limits


import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from .models import Player

# 1. Configuration Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_player_insight(player_name, country, batting_avg):
    """Generates a bio for a single player (used for manual/individual updates)."""
    # Updated to gemini-2.5-flash to avoid 404 errors
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = (f"Act as a cricket historian. Provide a 2-line interesting career summary "
              f"for {player_name} from {country}. They have a batting average of {batting_avg}.")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Insight currently unavailable."

def generate_all_bios():
    """Bulk updates all players in the database with balanced career summaries."""
    players = Player.objects.filter(ai_bio__isnull=True)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    for player in players:
        # 1. Gather Batting Stats
        bat_avg = "N/A"
        if hasattr(player, 'battingstat_set'):
            b_stat = player.battingstat_set.first()
            if b_stat: 
                bat_avg = b_stat.average

        # 2. Gather Bowling Stats
        bowl_wkts = "N/A"
        bowl_avg = "N/A"
        if hasattr(player, 'bowlingstat_set'):
            w_stat = player.bowlingstat_set.first()
            if w_stat:
                bowl_wkts = w_stat.wickets
                bowl_avg = w_stat.average

        # 3. Create a comprehensive prompt
        prompt = (
            f"Write a 2-line professional career summary for {player.name} from {player.country}. "
            f"Stats: Batting Avg {bat_avg}, Bowling Wkts {bowl_wkts}, Bowling Avg {bowl_avg}. "
            f"Identify if they are a specialist batsman, bowler, or all-rounder."
        )

        try:
            response = model.generate_content(prompt)
            player.ai_bio = response.text.strip()
            player.save()
            print(f"✅ Saved balanced bio for {player.name}")
        except Exception as e:
            print(f"❌ Error for {player.name}: {e}")
        
        # 4. Respect Free Tier limits (15 requests/min)
        time.sleep(4)