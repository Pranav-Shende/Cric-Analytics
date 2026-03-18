import csv
import os
from django.core.management.base import BaseCommand
from stats.models import Player, FieldingStat

class Command(BaseCommand):
    help = 'Load international fielding stats from CSV'

    def handle(self, *args, **kwargs):
        # Make sure this filename matches your fielding CSV exactly
        file_path = 'master_international_stats_fielding.csv'
        
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


                # 2. Update/Create Fielding Stats
                FieldingStat.objects.update_or_create(
                    player=player_obj,
                    format=row['format'],
                    defaults={
                        'innings': int(row['inns']) if row.get('inns') else 0,
                        'catch': int(row['ct']) if row.get('ct') else 0.0,
                        'stump_out': int(row['st']) if row.get('st') else 0,
                        'dismisals': row['dis'] if row.get('dis') and row['dis'] != '-' else None,
                        'dismisals_per_inning': float(row['d/i']) if row.get('d/i') and row['d/i'] != '-' else None,
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} fielding records!'))