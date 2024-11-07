from datetime import datetime, timedelta
from rest_framework import exceptions


def get_required_int_from_query_params(request, field_name):
        str_int = request.query_params.get(field_name)
        
        if str_int:
            try:
                return int(str_int)
            except ValueError:
                raise exceptions.ValidationError(f'Invalid integer for {field_name}.')
        else:
            raise exceptions.ValidationError(f'{field_name} parameter is required.')


def get_required_date_from_query_params(request, field_name):
        """It will return a datetime object with zero time values."""
        
        str_date = request.query_params.get(field_name)
        
        if str_date:
            try:
                return datetime.strptime(str_date, '%Y-%m-%d')
            except ValueError:
                raise exceptions.ValidationError(f'Invalid date format for {field_name}. Use YYYY-MM-DD.')
        else:
            raise exceptions.ValidationError(f'{field_name} parameter is required.')


def get_required_duration_from_query_params(request, field_name):
        str_duration_in_hours = request.query_params.get(field_name)
        
        if str_duration_in_hours:
            try:
                int_duration_in_hours = int(str_duration_in_hours)
            except ValueError:
                raise exceptions.ValidationError(f'Invalid duration format for {field_name}. Duration should be an integer.')
            try:
                return timedelta(hours=int_duration_in_hours)
            except ValueError:
                raise exceptions.ValidationError(f'Invalid duration format for {field_name}. Duration should be an integer.')
        else:
            raise exceptions.ValidationError(f'{field_name} parameter is required.')
