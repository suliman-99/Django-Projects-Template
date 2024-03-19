from django.contrib.auth import get_user_model
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
# from seeder.generators import users_data_generator
from seeder.serializers import (
    SuperUserSeederSerializer,
    # CategorySerializer,
    # SubCategorySerializer,
)


User = get_user_model()


@SeederRegistry.register
class SuperUserSeeder(seeders.CSVFileSerializerSeeder):
    serializer_class = SuperUserSeederSerializer
    csv_file_path = 'seeder/seeders/SuperUser.csv'
    priority = 0
    id = 'SuperUserSeeder'
    just_debug = True


# @SeederRegistry.register
# class UserSeeder(seeders.Seeder):
#     id = 'UserSeeder'
#     priority = 0
#     just_debug = True    

#     def seed(self):
#         users = [ User() for _ in range(50) ]
#         for idx, user in enumerate(users) :
#             user.first_name = users_data_generator.get_first_name() + ' ' + users_data_generator.get_last_name()
#             user.email = users_data_generator.get_email(user.first_name, user.last_name, idx+1)
#             user.email_verified = True
#             user.phone_number = users_data_generator.get_phone_number()
#             user.password = make_password(users_data_generator.get_password())
#             user.image = users_data_generator.get_image(idx)
#             user.bio = 'مهمتنا هي ايصال الطلب بجودة عالية وسعر مناسب لمن يحتاجه لهذا نحن الان من احسن وارقى التجار في العالم ونسعى لان نصبح في المقدمة برضى زبائننا وحبهم لنا نستقبل طلباتكم في اي وقت واي يوم لنكون جانبكم دائما لذلك لا تترددوا في الطلب من عندنا والتواصل معنا عند حدوث اي مشكلة في التوصيل وكل عام وانتم بخير'
#             user.is_store = True
#         User.objects.bulk_create(users)


# @SeederRegistry.register
# class CategorySeeder(seeders.CSVFileSerializerSeeder):
#     id = 'CategorySeeder'
#     priority = 1
#     just_debug = True
#     csv_file_path = 'seeder/data/CategorySeeder.csv'
#     serializer_class = CategorySerializer


# @SeederRegistry.register
# class SubCategorySeeder(seeders.CSVFileSerializerSeeder):
#     id = 'SubCategorySeeder'
#     priority = 2
#     just_debug = True
#     csv_file_path = 'seeder/data/SubCategorySeeder.csv'
#     serializer_class = SubCategorySerializer
