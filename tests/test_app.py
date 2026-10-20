from  page_analyzer import app
from unittest.mock import patch, Mock


# Тестирование главной страницы
def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Анализатор страниц" in response.text

# Тестирование добавления URL
def test_post_url():
    client = app.test_client()
    response = client.post("/urls", data={"url": "https://example.com"})
    assert response.status_code == 302  # Переход на страницу с информацией о добавленном URL

# Тестирование добавления некорректного URL
def test_post_invalid_url():
    client = app.test_client()
    response = client.post("/urls", data={"url": "invalid-url"})
    assert response.status_code == 422  # Статус код 422 для некорректного URL
    assert "Некорректный URL" in response.text
