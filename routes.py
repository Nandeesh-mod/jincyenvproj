from models import User
from flask import render_template, request, redirect, url_for, jsonify, session
from app import bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

def add_routes(app, db):



    @app.route('/error')
    def error_page():
        return render_template('error/error.htm')
    

    
    @app.route('/home')
    def home():
        if session.get("email"):
            return render_template('home/home.htm')
        else:
            return redirect(url_for('entry'))
        


    @app.route('/')
    def entry():
        return render_template('login/login.htm')

    @app.route('/login',methods=['POST'])
    def login():
        try: 
            data = request.form
            if not data or not data.get('email') or not data.get('password'):
                session['data_enterd'] = True
                return redirect(url_for('entry'))
            else:
                email = data.get('email')
                password = data.get('password')
                query = text("SELECT * FROM user WHERE email=:email")
                res  = db.session.execute(query, {"email": email})
                result = res.fetchall()

                if len(result) == 0:
                    return render_template('login/login.htm')
                
                print(result)
                if bcrypt.check_password_hash(result[0][3],password):
                    session['user_name'] = result[0][1]
                    session['email'] = result[0][2]
                    return redirect(url_for('home'))
                else:
                    session['password_incc'] = True
                    return render_template('login/login.htm')
            
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return redirect(url_for('error_page'))
    
    
    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            data = request.form
            if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('fname') or not data.get('address'):
                session['data_enterd'] = True
                return redirect(url_for('entry'))
            else:
                email = request.form.get("email")
                # validate email already exist 
                if User.query.filter_by(email=email).first():
                    session['email_exist'] = True
                    return redirect(url_for('entry'))

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
        



        

