from models import User, Complaints, Images
from flask import render_template, request, redirect, url_for, jsonify, session
from app import bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from werkzeug.utils import secure_filename
import uuid
import os
from utils import allowed_file


def add_routes(app, db):


    # for admin logins 
    @app.route('/admin_login', methods=['POST'])
    def admin_login():
        data = request.form
        if not data and data["email"] and data["password"]:
            return redirect(url_for('error_page'))
        if data["email"] == "admin@gmail.com" and data["password"]=="password":
            return render_template('admin/showcomplaints.htm')
        else:
            return redirect(url_for('error_page'))
        # if not data:
        #     print(data)
        #     if data["email"] == "admin@gmail.com" and data["password"] == "password":
        #         return render_template('/admin/showcomplaints.htm')
        #     else:
        #         return render_template('/error/error.htm')
        # else:
        #     return redirect(url_for('error_page'))



    @app.route('/test')
    def test():
        return render_template('/test.htm')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('entry'))


    @app.route('/register-complaint')
    def register_complaint():
        if session.get("email"):
            return render_template('/home/registercomp.htm')
        else:
            return redirect(url_for('entry'))
        
    @app.route('/admin')
    def admin():
        return render_template('/admin/admin.htm')
        

    @app.route('/view_complaint/<complaint_id>/<user_id>')
    def view_complaint(complaint_id, user_id):
        if session.get("email") and int(user_id) == int(session.get("user_id")):
            # to get the complaint details also the user details 
            # or combine the sql statement to get all the detail .
            # query = text("SELECT * FROM user WHERE email=:email")
            # res  = db.session.execute(query, {"email": email})
            # result = res.fetchall()
            getcomp_det = text("select * from user join complaints where user.id= complaints.user_id and complaints.id=:complaint_id;")
            res = db.session.execute(getcomp_det, {"complaint_id" : complaint_id})
            complaint_res = res.fetchall()
            print(complaint_res)

            getimage_det = text("select * from images where complaint_id=:complaint_id")
            res = db.session.execute(getimage_det, {"complaint_id" : complaint_id})
            image_res = res.fetchall()

            print(image_res)
            return render_template('/home/viewcomp.htm',complaint=complaint_res, images=image_res)
        else:
            return redirect(url_for('entry'))
    

    @app.route('/complaints')
    def complaints():
        if session.get("email"):
            query = text("SELECT * FROM complaints WHERE user_id=:user_id")
            res  = db.session.execute(query, {"user_id": session['user_id']})
            result = res.fetchall()
            print(result)
            return render_template('/home/complaint.htm', complaints=result)
        else:
            return redirect(url_for('entry'))



    @app.route('/error')
    def error_page():
        return render_template('error/error.htm')
    

    
    @app.route('/home')
    def home():
        if session.get("email"):

            # getting the total count
            query = text("SELECT COUNT(*) FROM complaints WHERE user_id=:user_id")
            res  = db.session.execute(query, {"user_id": session['user_id']})
            result = res.fetchall()

            # getting the total  points
            query = text("SELECT points FROM user WHERE id=:user_id")
            res  = db.session.execute(query, {"user_id": session['user_id']})
            result_point = res.fetchall()


            print(result)
            return render_template('home/home.htm', user_res = result, result_point = result_point)
        else:
            return redirect(url_for('entry'))
        


    @app.route('/')
    def entry():
        return render_template('login/login.htm')
    



    @app.route('/regcomp', methods=['POST'])
    def regcomp():
        try: 
            data = request.form
            files = request.files.getlist('images')
            print(files)

            if not files or files[0].filename == '':
                redirect(url_for('register_complaint'))
            
            upload_count = 0
            file_paths = []
            for file in files:
                print(file.filename)
                if file:
                    original_filename = secure_filename(file.filename)

                    extension = original_filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{str(uuid.uuid4())}.{extension}"


                    # creating a final path
                    final_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    absolute_path = os.path.abspath(final_path)

                    actual_path = os.path.join(app.config['ACTUAL_PATH'], unique_filename)
                    file_paths.append(actual_path)

                    file.save(absolute_path)
            
            url = f"https://maps.google.com/maps?q={data['lat']},{data['long']}&z=15&output=embed"
            complaint = Complaints(
                user_id = session['user_id'],
                title = data['title'],
                description = data['description'],
                location_url = url,
                severity = data['severity'],
                created_at = datetime.now(),
                updated_at =  datetime.now()
            )
            db.session.add(complaint)
            db.session.commit()
            comp_id = complaint.id
            print(file_paths)

            for image_path in file_paths:
                image = Images(
                    complaint_id = comp_id,
                    image_url = image_path
                )
                db.session.add(image)
                db.session.commit()

        except SQLAlchemyError as e:
            return redirect(url_for('error'))
        return redirect(url_for('home'))

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
                    session['user_id'] = result[0][0]
                    session['user_name'] = result[0][1]
                    session['email'] = result[0][2]
                    return redirect(url_for('home'))
                else:
                    session['password_incc'] = True
                    return redirect(url_for('entry'))
            
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
                phoneno = request.form.get("phoneno")
                
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
                    points = 0,
                    phoneno = phoneno
                )

                db.session.add(newuser)
                db.session.commit()

                session['success'] = True



        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
        return render_template('login/login.htm')
        


        

