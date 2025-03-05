from models import User
from flask import render_template, request


def add_routes(app, db):

    @app.route('/login')
    def login():
        return render_template('login/login.htm')
    
    
    @app.route('/signup', methods=['POST'])
    def signup():
        fname = request.form.get("fname")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        address = request.form.get("address")

        

        return "test"

