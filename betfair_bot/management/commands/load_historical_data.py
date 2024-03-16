from django.core.management.base import BaseCommand
from betfair_bot.models import BetfairData
import csv
import bz2

class Command(BaseCommand):
    help = 'Loads historical data from compressed files into the database'

    def handle(self, *args, **options):
        # Specify the path to your historical data files
        data_files = [
            'data/betfair_data/BASIC/2015/Apr/29/27432645.bz2',
            'data/betfair_data/BASIC/2015/Aug/27432942.bz2',
            # Add more files as needed
        ]

        for file_path in data_files:
            with bz2.open(file_path, 'rt') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    BetfairData.objects.create(
                        race_name=row['race_name'],
                        horse_name=row['horse_name'],
                        barrier_number=row['barrier_number'],
                        track_conditions=row['track_conditions'],
                        odds=row['odds'],
                        # Set other fields accordingly
                    )

        self.stdout.write(self.style.SUCCESS('Historical data loaded successfully.'))