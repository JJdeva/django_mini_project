from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
import pandas as pd
import random
class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."
    def __init__(self):
        df = pd.read_csv('/Users/jay/github/teamproject/site2/userinfo.csv')

        self.name = list(df['name'])
        self.email = list(df['email'])

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=2,
            type=int,
            help="몇 명의 유저를 만드나"
        )

    def handle(self, *args, **options):
        random.seed(10)
        total = options.get("total")
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            total,
            {
                "is_staff": False,
                "is_superuser": False,
                "nickname": lambda x: random.choice(self.name),#seeder.faker.name(),
                "email": lambda x: seeder.faker.email(),
            }
        )
        seeder.execute()
        # self.stdout.write(self.style.SUCCESS(f"{total}명의 유저가 작성되었습니다."))