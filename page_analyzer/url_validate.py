import validators
from urllib.parse import urlparse

# Валидация и нормализация URL
def validate_and_normalize_url(url):
    parsed_url = urlparse(url)
    name = f"{parsed_url.scheme}://{parsed_url.netloc}"
    if validators.url(url):
        return name
    return None


# Тримминг текста до указанной длины
def truncate_text(text, max_length=200):
    if text and len(text) > max_length:
        return text[:max_length] + "..."
    return text