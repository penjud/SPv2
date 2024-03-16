from django.core.management.base import BaseCommand
from betfair_bot.models import BetfairData
import csv
import re
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads historical data from a CSV file into the BetfairData model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load data from')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Extract horse prize money using regular expression
                horse_prize_money_str = row['horse prize money']
                numbers = re.findall(r'[\d.]+', horse_prize_money_str)
                horse_prize_money = float(numbers[0]) if numbers else None

                BetfairData.objects.create(
                    meeting_date=datetime.strptime(row['meeting date'], '%d/%m/%Y %I:%M:%S %p').strftime('%Y-%m-%d'),
                    track=row['track'],
                    race_number=int(row['race number']),
                    start_time=datetime.strptime(row['start time'], '%H:%M').strftime('%H:%M') if row['start time'] else None,
                    age_restrictions=row['age restrictions'],
                    class_restrictions=row['class restrictions'],
                    weight_restrictions=int(row['weight restrictions']) if row['weight restrictions'].isdigit() else None,
                    race_prizemoney=row['race prizemoney'],
                    horse_name=row['horse name'],
                    horse_age=int(row['horse age']),
                    horse_sex=row['horse sex'],
                    horse_number=int(row['horse number']) if row['horse number'].isdigit() else None,
                    horse_jockey=row['horse jockey'],
                    horse_barrier=int(row['horse barrier']) if row['horse barrier'].isdigit() else None,
                    horse_trainer=row['horse trainer'],
                    horse_weight=float(row['horse weight']) if row['horse weight'] else None,
                    horse_claim=float(row['horse claim']) if row['horse claim'] else None,
                    horse_last10=row['horse last10'],
                    horse_record=row['horse record'],
                    horse_record_distance=row['horse record distance'],
                    horse_record_track=row['horse record track'],
                    horse_record_track_distance=row['horse record track distance'],
                    horse_record_fast=row['horse record fast'],
                    horse_record_good=row['horse record good'],
                    horse_record_dead=row['horse record dead'],
                    horse_record_slow=row['horse record slow'],
                    horse_record_heavy=row['horse record heavy'],
                    horse_record_jumps=row['horse record jumps'],
                    horse_record_first_up=row['horse record first up'],
                    horse_record_second_up=row['horse record second up'],
                    horse_prize_money=horse_prize_money,
                    form_barrier=int(row['form barrier']) if row['form barrier'].isdigit() else None,
                    form_class=row['form class'],
                    form_distance=int(row['form distance']) if row['form distance'].isdigit() else None,
                    form_jockey=row['form jockey'],
                    form_margin=float(row['form margin']) if row['form margin'] else None,
                    form_meeting_date=datetime.strptime(row['form meeting date'], '%d/%m/%y').strftime('%Y-%m-%d') if row['form meeting date'] else None,
                    form_name=row['form name'],
                    form_other_runners=row['form other runners'],
                    form_position=int(row['form position']) if row['form position'].isdigit() else None,
                    form_price=float(row['form price']) if row['form price'] else None,
                    form_time=datetime.strptime(row['form time'], '%M:%S.%f').strftime('%H:%M:%S.%f') if row['form time'] else None,  # This might need parsing to a time object if not in the correct format
                    form_track=row['form track'],
                    form_track_condition=row['form track condition'],
                    form_weight=float(row['form weight']) if row['form weight'] else None
                )