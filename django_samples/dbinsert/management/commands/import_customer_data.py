import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from dbinsert.models import Customer


class Command(BaseCommand):
    help = 'Import customer data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):
        print('way', options['csv_file'])
        csv_file = options['csv_file'][0]
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            customers = []
            for row in reader:
                customers.append(
                    Customer(
                        name=row['氏名'],
                        name_kana=row['氏名(かな)'],
                        email=row['メールアドレス'],
                        address=row['住所'],
                        birthday=datetime.strptime(row['誕生日'], '%Y/%m/%d').date()
                    )
                )
        with transaction.atomic():
            print(customers)
            Customer.objects.bulk_create(customers)
        self.stdout.write(self.style.SUCCESS('Successfully imported customer data'))
