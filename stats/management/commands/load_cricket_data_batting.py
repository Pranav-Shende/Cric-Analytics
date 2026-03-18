import csv
import os
from django.core.management.base import BaseCommand
from stats.models import Player, BattingStat

class Command(BaseCommand):
    help = 'Load international batting stats from CSV'

    def handle(self, *args, **kwargs):
        # Path to your CSV (assuming it's in the project root)
        file_path = 'master_international_stats_batting.csv'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found!'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                # 1. Get or Create the Player first
                player_obj, created = Player.objects.get_or_create(
                    identifier=row['identifier'],
                    defaults={'name': row['full_name']}
                )
                if not created and player_obj.name != row['full_name']:
                    player_obj.name = row['full_name']
                    player_obj.save()

                # 2. Create the Batting Stat entry
                # We use 'update_or_create' so we can re-run this without duplicates
                BattingStat.objects.update_or_create(
                    player=player_obj,
                    format=row['format'],
                    defaults={
                        'matches': int(row['mat']) if row['mat'] else 0,
                        'runs': int(row['runs']) if row['runs'] else 0,
                        'average': float(row['ave']) if row['ave'] and row['ave'] != '-' else None,
                        'strike_rate': float(row['sr']) if row['sr'] and row['sr'] != '-' else None,
                        'innings':int(row['inns']) if row['inns'] else 0,
                        'is_league': False
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} batting records!'))