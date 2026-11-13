from .url_validate import validate_and_normalize_url, truncate_text
from .db import (
    select_urls,
    select_url_by_id,
    add_url_to_db,
    url_exists,
    add_url_check_to_db,
    select_url_checks_by_id,
)
from .config import SECRET_KEY
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


# Главная страница
@app.route("/", methods=["GET"])
def index():
    return render_template("home.html", title="Анализатор страниц")


# Добавление URL
@app.route("/urls", methods=["POST"])
def post_url():
    url = request.form["url"]
    name = validate_and_normalize_url(url)

    if name:
        exists, existing_id = url_exists(name)
        if exists:
            flash("Страница уже существует", "info")
            return redirect(url_for("show_url", id=existing_id))

        url_id = add_url_to_db(name)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("show_url", id=url_id))

    flash("Некорректный URL", "danger")
    return render_template("home.html", title="Анализатор страниц"), 422


# Получение списка URL
@app.route("/urls", methods=["GET"])
def get_urls():
    urls = select_urls()
    return render_template("urls.html", urls=urls, title="Список страниц")


# Получение информации о конкретном URL
@app.route("/urls/<int:id>", methods=["GET"])
def show_url(id):
    url = select_url_by_id(id)
    checks = select_url_checks_by_id(id)
    return render_template("url.html", url=url, checks=checks)


# Запуск проверки URL
@app.route("/urls/<int:id>/checks", methods=["POST"])
def check_url(id):
    # Здесь будет логика проверки URL
    try:
        url = select_url_by_id(id)
        if not url:
            flash("URL не найден", "danger")
            return redirect(url_for("get_urls"))
        response = requests.get(url[1], timeout=5)
        response.raise_for_status()

        # Извлечение информации из HTML-страницы
        soup = BeautifulSoup(response.content, "html.parser")
        h1 = soup.find("h1").text if soup.find("h1") else None
        title = soup.find("title").text if soup.find("title") else None
        description = (
            soup.find("meta", attrs={"name": "description"})["content"]
            if soup.find("meta", attrs={"name": "description"})
            else None
        )

        # Тримминг текста до 200 символов
        h1 = truncate_text(h1)
        title = truncate_text(title)
        description = truncate_text(description)


        # Добавление информации о проверке в базу данных
        add_url_check_to_db(id, response.status_code, h1, title, description)
        flash("Страница успешно проверена", "success")
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("show_url", id=id))
