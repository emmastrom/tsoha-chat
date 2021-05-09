from app import app
from flask import render_template, request, redirect
import messages, users, areas, chains
from db import db

@app.route("/")
def index():
    list_areas = areas.get_list()
    list_chains = []
    list_messages = []
    for area in list_areas:
        list_chains.append(chains.in_area(area[0]))
        list_messages.append(messages.in_area(area[0]))
    return render_template("index.html", count=len(list_areas), areas=list_areas, messages=list_messages, chains=list_chains)

@app.route("/add", methods=["GET", "POST"])
def add_area():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":

        name = request.form["name"]
        if len(name) < 1 or len(name) > 24:
            return render_template("error.html", message="Nimessä pitää olla 1-24 merkkiä")
        areas.add_area(name, users.user_id())
        return redirect("/")

@app.route("/create", methods=["POST"])
def create_chain():
    if request.method == "POST":

        subject = request.form["subject"]
        if len(subject) < 1 or len(subject) > 50:
            return render_template("error.html", message="Aiheessa pitää olla 1-50 merkkiä")

        opening_message = request.form["opening_message"]
        if len(opening_message) > 200:
            return render_template("error.html", message="Aloitusviestissä saa olla enintään 200 merkkiä")

        area_id = request.form["area_id"]
        if users.user_id() == 0:
            render_template("error.html", message="Ketjun luominen epäonnistui. Tarkista, että olet kirjautunut sisään")
        else:
            chains.create(area_id, subject, opening_message)
            return redirect("/area/"+area_id)

@app.route("/remove", methods=["GET", "POST"])
def remove_area():
    if request.method == "GET":
        list = areas.get_my_areas(users.user_id())
        return render_template("remove.html", list=list)

    if request.method == "POST":

        if "area" in request.form:
            area_id = request.form["area"]
            areas.remove_area(area_id, users.user_id())
        return redirect("/")

@app.route("/edit_subject", methods=["GET", "POST"])
def edit_subject():
    if request.method == "GET":
        list = chains.get_my_chains(users.user_id())
        return render_template("edit_subject.html", list=list)

    if request.method == "POST":

        if "chain" in request.form:
            chain_id = request.form["chain"]
            subject = request.form["subject"]
            chains.edit_subject(chain_id, subject)
        return redirect("/")

@app.route("/edit_opening_message", methods=["GET", "POST"])
def edit_opening_message():
    if request.method == "GET":
        list = chains.get_my_chains(users.user_id())
        return render_template("edit_opening_message.html", list=list)

    if request.method == "POST":

        if "chain" in request.form:
            chain_id = request.form["chain"]
            opening_message = request.form["opening_message"]
            chains.edit_opening_message(chain_id, opening_message)
        return redirect("/")

@app.route("/chain/<int:id>")
def chain(id):
    subject = chains.get_subject(id)
    opening_message = chains.get_opening_message(id)
    list = messages.get_list(id)
    return render_template("chain.html", id=id, subject=subject, opening_message=opening_message, count=len(list), messages=list)

@app.route("/area/<int:id>")
def area(id):
    name = areas.get_name(id)
    sql = "SELECT id, subject, opening_message FROM chains WHERE area_id=:id"
    result = db.session.execute(sql, {"id":id})
    chains = result.fetchall()
    return render_template("area.html", id=id, name=name, chains=chains)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if len(content) < 1 or len(content) > 200:
        render_template("error.html", message="Viestin pitää olla 1-200 merkkiä pitkä")
    chain_id = request.form["chain_id"]
    messages.send(content, chain_id)
    return redirect("/chain/"+chain_id)

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]

        if len(username) < 1 or len(username) > 24:
            return render_template("error.html", message="Tunnuksessa pitää olla 1-24 merkkiä")

        password = request.form["password"]

        role = request.form["role"]
        if role != "1" and role != "2":
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if users.register(username, password, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
