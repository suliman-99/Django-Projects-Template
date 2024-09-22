from django.contrib.auth import get_user_model
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from .serializers import (
    SuperUserSeederSerializer,
)


User = get_user_model()


@SeederRegistry.register
class SuperUserSeeder(seeders.CSVFileSerializerSeeder):
    serializer_class = SuperUserSeederSerializer
    csv_file_path = 'seeder/data/SuperUser.csv'
    priority = 0
    id = 'SuperUserSeeder'
    just_debug = True
