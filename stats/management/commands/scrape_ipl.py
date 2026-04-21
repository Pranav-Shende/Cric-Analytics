import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from datetime import datetime
import os
from django.conf import settings

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
                file_path = os.path.join(settings.BASE_DIR, 'ipl_points_latest.csv')
                df.to_csv(file_path, index=False)
            # Add Timestamp
            df["SCRAPED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save CSV
            df.to_csv("ipl_points_latest.csv", index=False)
            
            self.stdout.write(self.style.SUCCESS('Successfully scraped IPL data!'))
            self.stdout.write(str(df.head(5)))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Surgical Scraper Error: {e}"))