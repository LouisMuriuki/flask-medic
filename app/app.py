from datetime import timedelta
import datetime
from functools import wraps
import os
import pathlib
import requests
from flask import Flask, abort, flash, redirect, session,request,render_template, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app=Flask(__name__)
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
DB_USERNAME=os.getenv('DB_USERNAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')
# db = SQLAlchemy(app)
# Check if db is not already initialized
# if not hasattr(app, 'db'):
#     db_uri = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#     app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#     app.permanent_session_lifetime=timedelta(minutes=5)
#     db.init_app(app)
    
    


# from db import models 

# Initialize the database
# app.db.create_all()

app.secret_key=os.getenv('FLASK_SECRET')
##temporary disable hhtps check
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# OAuth
client_secrets_file = os.path.join(pathlib.Path(__file__).parent,"client_secret.json")

# Create a Flow instance from the client secrets file
flow = Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/user.gender.read", "https://www.googleapis.com/auth/user.birthday.read"],
    redirect_uri='http://localhost:5000/callback'  # Replace with your redirect URI
)

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
   return render_template("home.html")
 
 
@app.route("/login",methods=['GET','POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

def calculate_age(birthdate):
    """Calculate age based on birthdate."""
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@app.route("/callback",methods=['GET','POST'])
def callback():
    if "state" not in session:
        abort(500)  # Handle the case when 'state' is not in the session

    flow.fetch_token(authorization_response=request.url)
    
    if not session["state"] == request.args["state"]:
        abort(500)  # if does not match
    print(session)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    #     # Check if the user already exists in the database
    # user = models.User.query.filter_by(google_id=id_info.get("sub")).first()
    # if not user:
    #     # If the user does not exist, create a new user
    #     new_user = models.User(
    #         google_id=id_info.get("sub"),
    #         email=id_info.get("email"),
    #         first_name=id_info.get("given_name"),
    #         last_name=id_info.get("family_name"),
    #         age=calculate_age(id_info.get("birthdate"))
    #         )

    #     db.session.add(new_user)
    #     db.session.commit()
        
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    
    flash("Login successful!")
    return redirect("/prescription")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
 
 
@app.route("/prescription",methods=['GET','POST'])
# @login_is_required
def renderPresciption():
    dummy_prescriptions = [
    {
        'medicine_name': 'Aspirin',
        'dosage': '1 tablet daily',
        'instructions': 'Take with water after meals',
        'doctor': 'Dr. Smith',
    },
    {
        'medicine_name': 'Antibiotic',
        'dosage': '2 tablets twice a day',
        'instructions': 'Take with food',
        'doctor': 'Dr. Jones',
    },
    # Add more dummy data as needed
]
    #    if "user" in session:
           # prescriptions = models.Prescription.query.all()
    return render_template("prescription.html",prescriptions=dummy_prescriptions)
    #    else:
    #     flash("You are not logged in!")
    #     return redirect("/")
    
   

@app.route("/prescription/add")
# @login_is_required
def addPrescription():
    # if "user" in session:
    #     user=session["user"]
    #     if request.method=="POST":
    #         medicine_name=request.form.get('medicine')
    #         dosage=request.form.get('dosage')
    #         instructions=request.form.get('instructions')
    #         doctor=request.form.get('doctor')
            
            # current_user = models.User.query.filter_by(id=user['id']).first()
            
            # new_prescription = models.Prescription(
            #     name=medicine_name,
            #     dosage=dosage,
            #     instructions=instructions,
            #     doctor=doctor,
            #      user_id=current_user.id
            # )
            # db.session.add(new_prescription)
            # db.session.commit()

        #     flash("Prescription added successfully!")
        #     return redirect(url_for('protected_area'))

        # else:
            return render_template("addPrescription.html")
    # else:
    #     flash("You are not logged in!")
    #     return redirect(url_for("login"))


if __name__=='__main__':
   app.run(debug=True)