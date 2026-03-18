import csv
from django.core.management.base import BaseCommand
from stats.models import Player, AllRounderStat

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_path = 'master_international_stats_allrounder.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                player, _ = Player.objects.get_or_create(
                    identifier=row['identifier'], 
                    defaults={'name': row['full_name']}
                )
            

                # Save to the new dedicated model
                AllRounderStat.objects.update_or_create(
                    player=player,
                    format=row['format'],
                    defaults={
                        'innings_bat':int(row['inns_bat']) if row['inns_bat'] else 0,
                        'innings_bowl':int(row['inns_bowl']) if row['inns_bowl'] else 0,
                        'runs_bat': int(row['runs_bat']) if row['runs_bat'] else 0,
                        'wickets': int(row['wkts']) if row.get('wkts') else 0,
                        'all_rounder_rating': float(row['ar_rating'],)}
                )
        self.stdout.write("Successfully loaded All-Rounder stats!")