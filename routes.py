from models import User
from flask import render_template, request, redirect, url_for, jsonify, session
from app import bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def add_routes(app, db):

    @app.route('/login')
    def login():
        return render_template('login/login.htm')
    
    
    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            data = request.form
            if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('fname') or not data.get('address'):
                session['data_enterd'] = True
                return redirect(url_for('login'))
            else:
                email = request.form.get("email")
                # validate email already exist 
                if User.query.filter_by(email=email).first():
                    session['email_exist'] = True
                    return redirect(url_for('login'))

                fname = request.form.get("fname")
                username = request.form.get("username")
                password = request.form.get("password")
                address = request.form.get("address")
                
                # hashing the password
                hashed_password = bcrypt.generate_password_hash(password=password)
                created_date = datetime.now()

                newuser = User(
                    username = username,
                    firstname = fname,
                    email = email,
                    password_hash = hashed_password,
                    address = address,
                    created_at = created_date,
                    points = 0
                )

                db.session.add(newuser)
                db.session.commit()

                session['success'] = True



        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
        return render_template('login/login.htm')


            
            
        # fname = request.form.get("fname")
        # username = request.form.get("username")
        # password = request.form.get("password")
        # email = request.form.get("email")
        # address = request.form.get("address")

        # # hashing the password
        # hashed_password = bcrypt.generate_password_hash(password=password)
        # created_date = datetime.now()

        



        return "test"

