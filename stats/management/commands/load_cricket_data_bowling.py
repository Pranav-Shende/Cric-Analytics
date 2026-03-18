import csv
import os
from django.core.management.base import BaseCommand
from stats.models import Player, BowlingStat

class Command(BaseCommand):
    help = 'Load international bowling stats from CSV'

    def handle(self, *args, **kwargs):
        # Make sure this filename matches your bowling CSV exactly
        file_path = 'master_international_stats_bowling.csv'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found!'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                # 1. Match the Player (they should already exist from the batting import)
                player_obj, created = Player.objects.get_or_create(
                    identifier=row['identifier'],
                    defaults={'name': row['full_name']}
                )
                if not created and player_obj.name != row['full_name']:
                    player_obj.name = row['full_name']
                    player_obj.save()


                # 2. Update/Create Bowling Stats
                # Adjust 'wkts', 'ave', 'econ', 'sr' if your CSV headers are different
                BowlingStat.objects.update_or_create(
                    player=player_obj,
                    format=row['format'],
                    defaults={
                        'innings': int(row['inns']) if row.get('inns') else 0,
                        'overs': float(row['overs']) if row.get('overs') else 0.0,
                        'wickets': int(row['wkts']) if row.get('wkts') else 0,
                        'average': float(row['ave']) if row.get('ave') and row['ave'] != '-' else None,
                        'economy': float(row['econ']) if row.get('econ') and row['econ'] != '-' else None,
                        'best_bowling_figures': row['bbf'] if row.get('bbf') and row['bbf'] != '-' else None,
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} bowling records!'))