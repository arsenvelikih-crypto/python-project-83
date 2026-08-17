import os
from urllib.parse import urlparse
from datetime import datetime
import psycopg
import validators
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
conn = psycopg.connect(DATABASE_URL)





@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        if validators.url(url):
            parsed_url = urlparse(url)
            name = parsed_url.netloc
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM urls WHERE name = %s",
                            (name,)
                )
                existing_url = cur.fetchone()
                if existing_url:
                    flash("Сайт уже добавлен", "danger")
                else:
                    cur.execute(
                        "INSERT INTO urls (name, created_at) VALUES (%s, %s)", 
                        (name, datetime.now())
                        )
                    flash("Страница успешно добавлена", "success")
            conn.commit()
            return redirect(url_for("index"))
        else:
            flash("Ошибка добавления страницы", "danger")
    return render_template("home.html", title="Анализатор страниц")




@app.route("/urls", methods=["GET"])
def get_urls():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
        urls = cur.fetchall()
    return render_template("urls.html", urls=urls, title="Список страниц")




@app.route("/urls/<int:id>", methods=["GET"])
def show_url(id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, created_at FROM urls WHERE id = %s",
            (id,)
        )
        url = cur.fetchone()
    return render_template("url.html", url=url)





