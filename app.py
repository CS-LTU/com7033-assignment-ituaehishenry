from flask import Flask, render_template, request, redirect, url_for, flash, session

# To automate the webbrowser the webbrowser is imported below.
import webbrowser
#Threading allows multple running of tasks at the same time.
from threading import Thread
import time
import sqlite3
import os
""" For stronger security of password_hashing -
# using bcrypt implace of the built in security in flask - Werkzeug.
"""
       
                  
from pymongo import MongoClient
import bcrypt
from functools import wraps
import secrets # generate token as a security measure

# Mongodb set-up - using a secret mongodb link
from dotenv import load_dotenv
load_dotenv()
from bson.objectid import ObjectId

 # Adding validation as means of additional security - functions are imported from validation module file created.
from validation import val_age, val_bmi, val_glucose, val_binary, val_required

# Connect to MongoDB using the environment variable and Mongodb set-up
client = MongoClient(os.getenv('MONGODB_URI'))
db = client["Stroke_db"]
patient_collection = db["Stroke"]

    


app = Flask(__name__)
# introducing cookies for security
app.secret_key = 'your-secret-key-here' # In production this won't be used here

#CSRF protection

def generate_csrf_token():

    """
    Generate and save a CSRF token
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
        return session['csrf_token']
    
def csrf_token_required(f):
    """
    decorator use to require CSRF token for POST requests
    """    
    @wraps(f)
    def dec_func(*args, **kwargs):
        if request.method == 'POST':
            token = session.get('csrf_token')
            form_token =request.form.get('csrf_token')

            # check for tokenif it manches and exists
            if not token or not form_token or token != form_token:
                flash('Invalid CSRF token. Please try again', 'error' )
                return redirect(request.referrer or url_for('home'))
            
        return f(*args, **kwargs)
    return dec_func 

 #make CSRF token available
@app.context_processor
def input_csrf_token():
    """
    Make CSRF tokenavailable

    """ 
    return dict(csrf_token=generate_csrf_token())   

# Login required decorator- Preventing unauthorised users to have access 

def login_required(f):
    @wraps(f)
    def dec_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('let_login'))
        return f(*args, **kwargs)
    return dec_function
# Individual redirected to admin and if not admin the individual is redirect to the home page.
def admin_required(f):
    @wraps(f)
    def dec_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return dec_function


#Setting SQLite for authentication of user.
def init_db():
    # To implement the RBAC features role column is added to the table.
    # Initialising the SQLite DB for user data
    conn = sqlite3.connect('users3.db')
    cursor =conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     first_name TEXT NOT NULL,
                     last_name  TEXT NOT NULL,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT  NOT NULL,
                     role TEXT DEFAULT 'user',
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )
                   """ )
    conn.commit()
    conn.close()
    create_admin_if_needed()
def create_admin_if_needed():    
 
    conn = sqlite3.connect('users3.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'),
        bcrypt.gensalt()).decode('utf-8')  

        cursor.execute(
            "INSERT INTO users (first_name, last_name, username, password, role) values (?,?,?,?,? )",
             ('Admin', 'User', 'admin', hashed_password,'admin' )   
        )    
        conn.commit()
        print("Admin user created: username= 'admin', password='admin123'") 

        conn.close()  

       
# Starting with route for the home page
@app.route('/')
def home():
    user_fullname = None
    if 'username' in session:
        # Get user's full name from database
        conn = sqlite3.connect('users3.db')
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM users WHERE username = ?", (session['username'],))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_fullname = f"{user[0]} {user[1]}"
    return render_template("index.html", user_fullname=user_fullname) 

# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# Route for the Help and Support page
@app.route('/help')
def Support():
    return render_template("help.html")

# routing for users registration
@app.route('/register', methods =['GET','POST'])
def let_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']#.encode('utf-8')
# validation check        

        if not first_name.strip():
            flash("Your first name is required", "error")
            return redirect(url_for())
        if not last_name.strip():
            flash("Your last name is required", "error")
            return redirect(url_for())
        if not username.strip():
            flash("Your username is required", "error")
            return redirect(url_for())
        if not password.strip():
            flash("Your password is required", "error")
            return redirect(url_for())
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        try: 
            conn = sqlite3.connect('users3.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, username, password, role) VALUES (?,?,?,?,?)",
                            (first_name, last_name, username, hashed_password, 'user'))
            conn.commit()
            conn.close()
            return render_template("success.html")
            
        
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for("let_register"))
    return render_template("Register.html")



#Routing for login
@app.route('/login', methods = ['GET', 'POST'])
def let_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users3.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username =?",(username,))
        record = cursor.fetchone()
        conn.close()

        if record and bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8')):
            session['username'] = username
            session['role'] = record[1]
            flash("Login was successful!", "success")
            return redirect(url_for("home"))
        else:
            flash('Invalid username or password', "error")
            return redirect(url_for('let_login'))
    return render_template('Login.html')
#Routing for logout
@app.route('/logout')
def let_logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))

#Importing from MDB to use the CRUD functions in flask
try:
    from Prototype.MDB import add_patient, view_patient, update_patient, delete_patient
except ImportError:
    # Fallback if MDB module doesn't exist
    def add_patient(patient_data):
        patient_collection.insert_one(patient_data)
        return True
    
    def view_patient(username, is_admin):
        if is_admin:
            return list(patient_collection.find())
        else:
            return list(patient_collection.find({"created_by": username}))
    
    def update_patient(patient_id, updated_data, username, is_admin):
        if is_admin:
            patient_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": updated_data})
            return True
        return False
    
    def delete_patient(patient_id, username, is_admin):
        if is_admin:
            patient_collection.delete_one({"_id": ObjectId(patient_id)})
            return True
        return False
# Patients Management Routes
#Routing for admin_dashboard
@app.route('/admin/dashboard')
@admin_required
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
#Route for view
@app.route('/view_patients')
@login_required

def view_patients():
    username = session['username']
    is_admin = (session.get('role') == 'admin')
    patients = view_patient(username=username, is_admin=is_admin)
    return render_template('view_patient.html',patients = patients)
#Route for Add Patient

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
@csrf_token_required 
def add_patient_route():
    if request.method == 'POST':
 # validation checks
        errors = []   
# required fields check
        is_valid, result = val_required(request.form.get('name', ''),"Name")
        if not is_valid:
            errors.append(result)
# numbers validation
        is_valid, result = val_age(request.form.get('age', ''))
        if not is_valid:
            errors.append(result)

        is_valid, result = val_bmi(request.form.get('bmi','')) 
        if not is_valid:
            errors.append(result)

        is_valid, result = val_glucose(request.form.get('avg_glucose_level', ''))
        if not is_valid:
            errors.append(result)
#binary fields validation check
        is_valid, result  = val_binary(request.form.get('hypertension', ''), "Hypertension")
        if not is_valid:
            errors.append(result)

        is_valid, result = val_binary(request.form.get('heart_disease', ''), "Heart disease") 
        if not is_valid:
            errors.append(result)
            
        is_valid, result = val_binary(request.form.get('stroke', ''),"Stroke")
        if not is_valid:
            errors.append(result)
# show and stop if any validation errors occur
        if errors:
            for error in errors:
                flash(error, "error")
                return render_template('add_patient.html')            
        patient_data = {
            'name': request.form['name'],
            'age': float(request.form['age']),
            'gender': request.form['gender'],
            'hypertension': int(request.form['hypertension']),
            'heart_disease': int(request.form['heart_disease']),
            'ever_married': request.form['ever_married'],
            'work_type': request.form['work_type'],
            'Residence_type': request.form['Residence_type'],
            'avg_glucose_level': float(request.form['avg_glucose_level']),
            'bmi': float(request.form['bmi']),
            'smoking_status': request.form['smoking_status'],
            'stroke': int(request.form['stroke']),
            'created_by': session['username'] # To track who created this
        }
        
        if add_patient(patient_data):
            flash('Patient added successfully!', 'success')
            return redirect(url_for('view_patients'))
        else:
            flash('Error adding patient. Please try again.', 'error')
    
    return render_template('add_patient.html')
# Route to update patient
@app.route('/update_patient/<patient_id>', methods=['GET', 'POST'])
@login_required
@csrf_token_required 
def update_patient_route(patient_id):
    if request.method == 'POST':

        # validation checks
        errors = []   
# required fields check
        is_valid, result = val_required(request.form.get('name', ''),"Name")
        if not is_valid:
            errors.append(result)
# numbers validation
        is_valid, result = val_age(request.form.get('age', ''))
        if not is_valid:
            errors.append(result)

        is_valid, result = val_bmi(request.form.get('bmi','')) 
        if not is_valid:
            errors.append(result)

        is_valid, result = val_glucose(request.form.get('avg_glucose_level', ''))
        if not is_valid:
            errors.append(result)
#binary fields validation check
        is_valid, result  = val_binary(request.form.get('hypertension', ''), "Hypertension")
        if not is_valid:
            errors.append(result)

        is_valid, result = val_binary(request.form.get('heart_disease', ''), "Heart disease") 
        if not is_valid:
            errors.append(result)
            
        is_valid, result = val_binary(request.form.get('stroke', ''),"Stroke")
        if not is_valid:
            errors.append(result)
# show and stop if any validation errors occur
        if errors:
            for error in errors:
                flash(error, "error")
                return render_template('update_patient.html', patient_id=patient_id)  
        updated_data = {
            'name': request.form['name'],
            'age': float(request.form['age']),
            'gender': request.form['gender'],
            'hypertension': int(request.form['hypertension']),
            'heart_disease': int(request.form['heart_disease']),
            'ever_married': request.form['ever_married'],
            'work_type': request.form['work_type'],
            'Residence_type': request.form['Residence_type'],
            'avg_glucose_level': float(request.form['avg_glucose_level']),
            'bmi': float(request.form['bmi']),
            'smoking_status': request.form['smoking_status'],
            'stroke': int(request.form['stroke'])
        }
        username = session['username']
        is_admin = (session.get('role') == 'admin')
        if update_patient(patient_id, updated_data, username=username, is_admin=is_admin):
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('view_patients'))
        else:
            flash('Error updating patient. Please try again.', 'error')
    
    return render_template('update_patient.html', patient_id=patient_id)

# Route to delete patient - GET for confirmation, POST for actual deletion
@app.route('/delete_patient/<patient_id>', methods=['GET', 'POST'])
@login_required
def delete_patient_route(patient_id):
    if request.method == 'POST':
        username = session['username']
        is_admin = (session.get('role') == 'admin')

        if delete_patient(patient_id, username=username, is_admin=is_admin):
            
            flash('Patient deleted successfully!', 'success')
            return redirect(url_for('view_patients'))
        else:
            flash('Error deleting patient or insufficient permission.', 'error')
            return redirect(url_for('view_patients'))
    return render_template('delete_patient.html', patient_id=patient_id)





def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    init_db()
    print("Starting server...")
    Thread(target=run_flask).start()
    Thread(target=open_browser).start()