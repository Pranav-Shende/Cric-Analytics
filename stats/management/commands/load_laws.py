import json
import os
from django.core.management.base import BaseCommand
from stats.models import Law, LawSubsection

class Command(BaseCommand):
    help = 'Load the 42 Laws of Cricket from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'cricket_laws.json'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found!'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            laws_data = json.load(file)
            count = 0
            for item in laws_data:
    # 1. Create or update the main Law
                law_obj, created = Law.objects.update_or_create(
                    number=item['number'],
                    defaults={'title': item['title']}
                )
                # 2. Loop through the subsections in this law
                for sub in item.get('subsections', []):
                    LawSubsection.objects.update_or_create(
                        law=law_obj,
                        number=sub['number'],
                        defaults={
                            'title': sub['title'],
                            'content': sub['content']
                        }
                    )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} Laws of Cricket!'))


