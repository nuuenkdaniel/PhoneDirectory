from flask import Blueprint, render_template, request

views = Blueprint('views',__name__)

@views.route('/')
def home():
    from website.database import search
    print(search(["address"],["name"],["Daniel Lew"]))
    return render_template("home.html")

@views.route('/add-person', methods=['GET','POST'])
def add_person():
    if request.method == 'POST':
        from website.database import add_person
        email = request.form.get('email')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        street_address = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zip')
        add_person(name,phone_number,street_address,city,state,zipcode,email)
        
    return render_template("add_person.html")

@views.route('/search', methods=['GET','POST'])
def search_by_name():
    if request.method == 'POST':
        from website.database import search
        request.form.get()
    return render_template("search.html")