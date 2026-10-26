import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random
import os

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route('/home')
def home():
	return render_template('home.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['To'] = email
    
    
    # Configure SMTP credentials through environment variables; never store
    # account passwords in source code.
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not smtp_user or not smtp_password:
        app.logger.error("SMTP_USER and SMTP_PASSWORD are required for OTP email.")
        return (
            "Email verification is not configured. Set SMTP_USER and "
            "SMTP_PASSWORD environment variables, then restart the app.",
            503,
        )

    msg["From"] = smtp_user
    try:
        with smtplib.SMTP(os.environ.get("SMTP_HOST", "smtp.gmail.com"),
                          int(os.environ.get("SMTP_PORT", "587")), timeout=15) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    except (OSError, smtplib.SMTPException, ValueError):
        app.logger.exception("Could not send signup verification email")
        return "Could not send the verification email. Check your SMTP settings.", 502
    return render_template("val.html")

@app.route('/predict_lo', methods=['POST'])
def predict_lo():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")

@app.route("/notebook")
def notebook():
    return render_template("Notebook.html")


@app.route('/predict',methods=['POST'])
def predict():
    try:
        # The HTML form uses numeric feature names (0, 1, ...).
        int_features = [float(value) for value in request.form.values()]
        if not int_features:
            raise ValueError("Please enter all required feature values.")

        model_path = os.path.join(os.path.dirname(__file__), 'model_wapper.sav')
        if not os.path.isfile(model_path):
            return "Model file not found: model_wapper.sav", 500

        model = joblib.load(model_path)
        expected = getattr(model, "n_features_in_", None)
        if expected is not None and len(int_features) != expected:
            return (
                f"Invalid number of features: received {len(int_features)}, "
                f"but the model expects {expected}.",
                400,
            )

        prediction = model.predict(np.asarray(int_features, dtype=float).reshape(1, -1))
        # Pass a scalar to Jinja rather than a NumPy array.
        result = prediction.item() if hasattr(prediction, "item") else prediction[0]
        return render_template('prediction.html', prediction=result)
    except ValueError as exc:
        return f"Invalid input: {exc}", 400
    except Exception as exc:
        app.logger.exception("Prediction failed")
        return (
            "Prediction could not be completed. Check that the dependencies "
            "match the model version and that all feature values are valid.",
            500,
        )



if __name__ == "__main__":
    app.run(debug=True)
