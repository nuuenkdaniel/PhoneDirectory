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
        session["search_first_name"] = request.form.get("first_name")
        session["search_last_name"] = request.form.get("last_name")
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
    from website.database import search
    table = []
    columns = []
    filters = []
    if session["search_first_name"] != None:
        table.append("info"); columns.append("first_name"); filters.append(session["search_first_name"])
        table.append("info"); columns.append("last_name"); filters.append(session["search_last_name"])
    if session["search_email"] != None:
        table.append("contact_info"); columns.append("email"); filters.append(session["search_email"])
    if session["search_phone_number"] != None:
        table.append("contact_info"); columns.append("phone_number"); filters.append(session["search_phone_number"])
    if session["search_street_address"] != None:
        table.append("address"); columns.append("street_address"); filters.append(session["search_street_address"])
        table.append("address"); columns.append("state"); filters.append(session["search_state"])
        table.append("address"); columns.append("city"); filters.append(session["search_city"])
        table.append("address"); columns.append("zipcode"); filters.append(session["search_zipcode"])
    data = search(table,columns,filters)
    print(data)
    return render_template("results.html",data=data)