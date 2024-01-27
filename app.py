from flask import Flask, jsonify, render_template, request, session, redirect
# from firebase_admin import credentials, firestore, initialize_app
from dotenv import dotenv_values
import pyrebase

app = Flask(__name__)

config = dict(dotenv_values(".env"))

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = "peepeepoopoo"

@app.route("/", methods=["POST", "GET"])
def index():
    # if request.method == "POST":
    #     if request.form["submit"] == "login":
    #         return redirect("/login")
    #     elif request.form["submit"] == "register":
    #         return redirect("/register")
    if 'username' in session:
        return f"Already Logged in <a href='/logout'>Logout</a>"
    return render_template("home.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
        if "user" in session:
            return render_template("signedin.html", user=session['user'], email_verified=True)
        else:
            if request.method == "POST":
                email = request.form.get("email")
                passwd = request.form.get("password")
                # try:
                user = auth.sign_in_with_email_and_password(email, passwd)
                # session["user"] = email
                print("USER Signed in!!!!!!")
                id_token = user["idToken"]
                email_verified = auth.get_account_info(id_token)["users"][0]["emailVerified"]
                if email_verified:
                    session["user"] = email
                return render_template("signedin.html", user=email, email_verified=email_verified)
                # except:
                #     return "Failed to login"
        return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if "user" in session:
        return render_template("signedin.html", user=session['user'])
    if request.method == "POST":
        email = request.form.get("email")
        passwd = request.form.get("password")
        user = auth.create_user_with_email_and_password(email, passwd)
        print("USER CREATED!!!!!!")
        auth.send_email_verification(user["idToken"])
        return render_template("after_registration.html")
    return render_template("register.html")
        
@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
