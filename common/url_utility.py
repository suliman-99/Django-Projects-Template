

def get_request_base_url(request):
    scheme = request.scheme
    host = request.get_host()
    return f"{scheme}://{host}"


def remove_media_base_url(url_string, base_url):
    base_url += '/media/'
    if url_string.startswith(base_url):
        url_string = url_string[len(base_url):]
    return url_string


def add_media_base_url(url_string, base_url):
    base_url += '/media/'
    if not url_string.startswith('http'):
        url_string = base_url + url_string
    return url_string
