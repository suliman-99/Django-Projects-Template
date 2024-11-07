import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number


def get_phone_number_country_code(phone_number):
    if not phone_number:
        return None
    
    if isinstance(phone_number, str):
        if not phone_number.startswith('+'):
            phone_number = f'+{phone_number}'
        phone_number = phonenumbers.parse(phone_number)
    
    return phone_number.country_code


def get_phone_number_region_code(phone_number):
    if not phone_number:
        return None
    
    if isinstance(phone_number, str):
        if not phone_number.startswith('+'):
            phone_number = f'+{phone_number}'
        phone_number = phonenumbers.parse(phone_number)
    
    return region_code_for_number(phone_number)
