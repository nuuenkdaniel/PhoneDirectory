from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint("views",__name__)

@views.route('/')
def home():
    from website.database import search
    
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
        from website.database import search
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("number")
        street_address = request.form.get("street-address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zip")
        return redirect(url_for("views.results"))
    return render_template("search.html")

@views.route("/results")
def results():
    return render_template("results.html")