from flask import Blueprint, render_template, request, redirect, url_for, session

views = Blueprint("views",__name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route("/add-person", methods=["GET","POST"])
def add_person():
    if request.method == "POST":
        from website.database import add_person
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        street_address = request.form.get("street_address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zip")
        add_person(first_name,last_name,phone_number,street_address,city,state,zipcode,email)
        
    return render_template("add_person.html")

@views.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        session["search_name"] = request.form.get("name")
        session["search_email"] = request.form.get("email")
        session["search_phone_number"] = request.form.get("number")
        session["search_street_address"] = request.form.get("street-address")
        session["search_city"] = request.form.get("city")
        session["search_state"] = request.form.get("state")
        session["search_zipcode"] = request.form.get("zip")
        return redirect(url_for("views.results"))
    return render_template("search.html")

@views.route("/results")
def results():
    print(session["search_name"])
    return render_template("results.html")