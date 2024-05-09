
def cast_to_bool(value: str) -> bool:
    if value is None:
        return None
    value = value.lower()

    if value == 'true':
        return True
    
    elif value == 'false':
        return False
    
    else:
        return None
    