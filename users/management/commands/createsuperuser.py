import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser.'
    
    def handle(self, *args, **options):

        while(True):
            email = input('email: ')

            if email:
                break
            else :
                print('email is required !!!')

        # while(True):
        #     phone_number = input('phone_number: ')

        #     if phone_number:
        #         break
        #     else :
        #         print('phone_number is required !!!')

        while(True):
            password = getpass.getpass(prompt='password: ')

            if password:
                break
            else :
                print('password is required !!!')

        User.objects.create_superuser(email=email, password=password)
