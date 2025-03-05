from models import User
from flask import render_template


def add_routes(app, db):

    @app.route('/login')
    def login():
        return render_template('login.htm')
    
    