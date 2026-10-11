from .url_validate import validate_and_normalize_url
from .db import (
    select_urls, 
    select_url_by_id, 
    add_url_to_db, url_exists, 
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


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY



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
    return render_template("home.html", title="Анализатор страниц")



# Получение списка URL
@app.route("/urls", methods=["GET"])
def get_urls():
    urls = select_urls()
    return render_template(
        "urls.html", urls=urls,
        title="Список страниц"
        )



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
        add_url_check_to_db(id)
        flash("Страница успешно проверена", "info")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("show_url", id=id)) 





