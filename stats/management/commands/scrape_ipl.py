# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from django.core.management.base import BaseCommand
# from datetime import datetime
# import os

# class Command(BaseCommand):
#     help = "Scrapes IPL 2026 points table without extra parser engines"

#     def handle(self, *args, **kwargs):
#         # The source of truth for the 2026 season
#         URL = "https://www.iplt20.com/points-table/men"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         }
        
#         try:
#             self.stdout.write("Connecting to IPL Official Site...")
#             response = requests.get(URL, headers=headers, timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Find the standings table
#             table = soup.find('table')
#             if not table:
#                 self.stdout.write(self.style.ERROR("Table not found! The site structure might have changed."))
#                 return

#             # 1. Extract Headers manually
#             headers_list = [th.text.strip().upper() for th in table.find_all('th')]
            
#             # 2. Extract Row Data manually
#             rows_data = []
#             for tr in table.find_all('tr'):
#                 cells = tr.find_all('td')
#                 if len(cells) > 1:
#                     row_content = [td.text.strip() for td in cells]
#                     rows_data.append(row_content)

#             # 3. Create DataFrame (Manual parsing avoids lxml/html5lib dependency)
#             df = pd.DataFrame(rows_data, columns=headers_list[:len(rows_data[0])])

#             # 4. Clean the Team names (Removing logos/extra text)
#             # Official site often has team names as "Punjab Kings\nPBKS"
#             if 'TEAM' in df.columns:
#                 df['TEAM'] = df['TEAM'].apply(lambda x: x.split('\n')[0].strip())

#             # 5. Add Metadata
#             df["SCRAPED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # 6. Save to CSV in your project root
#             # This allows your Django views to read it easily
#             csv_filename = "ipl_points_latest.csv"
#             df.to_csv(csv_filename, index=False)
            
#             self.stdout.write(self.style.SUCCESS(f"Successfully generated {csv_filename}"))

#             # 7. Print a preview to the console for confirmation
#             # Check for common column names in case the site uses 'PTS' vs 'POINTS'
#             preview_cols = [c for c in ['POS', 'TEAM', 'PTS', 'P', 'W', 'L', 'NRR'] if c in df.columns]
#             self.stdout.write("\n--- CURRENT STANDINGS PREVIEW ---")
#             self.stdout.write(str(df[preview_cols].head(10)))
#             self.stdout.write("---------------------------------\n")

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Scraper crashed: {e}"))

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from datetime import datetime
import io

class Command(BaseCommand):
    help = "Surgical IPL 2026 Scraper - Bypasses missing table tags"

    def handle(self, *args, **kwargs):
        # Using a direct data-heavy URL
        URL = "https://www.espncricinfo.com/series/ipl-2026-1510719/points-table-standings"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        try:
            self.stdout.write("Surgically extracting IPL Standings...")
            response = requests.get(URL, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Plan A: Search for the common standings class in 2026
            # Plan B: Just find any table on the page
            table = soup.select_one('table') or soup.find('table')
            
            if not table:
                self.stdout.write(self.style.ERROR("Could not find a table structure. The site might be JS-heavy."))
                return

            # Extract headers and rows manually to avoid lxml/html5lib
            rows_data = []
            for tr in table.find_all('tr'):
                cells = tr.find_all(['td', 'th'])
                row = [cell.text.strip() for cell in cells]
                if len(row) > 2: # Ensure it's not an empty or spacer row
                    rows_data.append(row)

            if len(rows_data) < 2:
                self.stdout.write(self.style.ERROR("Found a table, but it had no data rows."))
                return

            # Create the DataFrame
            df = pd.DataFrame(rows_data[1:], columns=rows_data[0])
            
            # Standardize Column Names
            df.columns = [c.upper().replace(' ', '_').strip() for c in df.columns]
            if 'POS' in df.columns:
                df = df[df['POS'].apply(lambda x: str(x).strip().isdigit())]
                
            # Add Timestamp
            df["SCRAPED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save CSV
            df.to_csv("ipl_points_latest.csv", index=False)
            
            self.stdout.write(self.style.SUCCESS('Successfully scraped IPL data!'))
            self.stdout.write(str(df.head(5)))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Surgical Scraper Error: {e}"))