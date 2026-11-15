import validators
from urllib.parse import urlparse

# Валидация и нормализация URL
def validate_and_normalize_url(url):
    parsed_url = urlparse(url)
    name = f"{parsed_url.scheme}://{parsed_url.netloc}"
    if len(url) > 200:
        return None
    if validators.url(url):
        return name
    return None


