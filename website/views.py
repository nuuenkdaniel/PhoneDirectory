from flask import Blueprint, render_template, request

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/add-person', methods=['GET','POST'])
def add_person():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        print(email+","+name+","+phone_number)
    return render_template("add_person.html")

@views.route('/look-up')
def look_up():
    return render_template("look_up.html")

@views.route('/search-by-name')
def search_by_name():
    return render_template("search.html")