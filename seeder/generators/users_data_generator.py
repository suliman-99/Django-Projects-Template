import secrets
from django.contrib.auth.hashers import make_password

first_names = [
    'عبد الرحمن',
    'عبد الغني',
    'عبد الله',
    'احمد',
    'محمد',
    'محمود',
    'سعيد',
    'سليمان',
    'اسامة',
    'اسماعيل',
    'مصطفى',
    'مؤيد',
    'كامل',
    'فادي',
    'مازن',
    'انس',
    'عمار',
    'خالد',
    'عصام',
    'بلال',
    'منذر',
]

last_names = [
    'عبد الرحيم',
    'عبد المالك',
    'عبد المجيد',
    'احمد',
    'محمد',
    'محمود',
    'قجة',
    'حلبي',
    'حوراني',
    'كردي',
    'عوض',
    'تركمان',
    'حمصي',
    'شما',
    'ابراهيم',
    'حاج',
    'حبيب',
    'صالح',
    'علي',
    'الشامي',
    'الحلو',
    'المصري',
    'ظريفه',
]

# ------------------------------------------------------------------

def get_first_name():
    length = len(first_names)
    return first_names[secrets.randbelow(length)]

def get_last_name():
    length = len(last_names)
    return last_names[secrets.randbelow(length)]

def get_email(first_name, last_name, idx):
    return f'test{idx}@gmail.com'.replace(" ", "")

def get_phone_number():
    return f'00966{secrets.randbelow(100000000)}'

def get_password():
    return make_password('1')

def get_image(idx):
    return f'_seeders_data_/users/images/user{(idx%10)+1}.jpg'
