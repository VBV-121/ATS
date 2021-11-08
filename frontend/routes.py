import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort, Response
from frontend import app, db, bcrypt
from frontend.forms import registrationForm, loginForm
from frontend.models import User, RequestUser
from flask_login import login_user, current_user, logout_user, login_required

#Setting up the home page route
@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
@login_required
def home():        
    return render_template("home.html")

#This is just added registration function but we wont be using it
@app.route("/register",methods=['GET','POST'])
def register():
    #Check if someone is already logged in or not
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    #Fetch form
    form = registrationForm()
    #Trigger when submit button is clicked
    if form.validate_on_submit():
        #Create a class of the details that are entered in the form
        RequestUsers = RequestUser(username=form.username.data, email = form.email.data, password=form.password.data)
        #Add data to database
        db.session.add(RequestUsers)
        db.session.commit()
        #Show a popup
        flash(f'Your account has been created!','success')
        #Reload the page
        return redirect(url_for('login'))
    #Load the page initially
    return render_template('register.html',title='Register',form=form)

@app.route("/adminpage",methods=['GET','POST'])
def adminpage():
    #Trigger when submit button is clicked
    if request.method == 'POST':
       #If add button is clicked 
       if request.form['submit_button'] == 'add':
           #Fetch all the detaild from the request user database
           RequestUsers = RequestUser.query.all()
           username = RequestUsers[-1].username
           password = RequestUsers[-1].password
           email = RequestUsers[-1].email
           #Create a hashcode of the password
           hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
           #Create a user class of the user
           Users = User(username=username, email = email, password=hashed_password)
           #Add to database
           db.session.add(Users)
           db.session.commit()
           print(Users)
           #Reload the page
           return render_template("adminpage.html")
    #Fetch all the detaild from the request user database
    RequestUsers = RequestUser.query.all()
    username = RequestUsers[-1].username
    email = RequestUsers[-1].email
    #Load inital page
    return render_template("adminpage.html",email=email,username=username)


#When login page is opened this function will run
@app.route("/login",methods=['GET','POST'])
def login():
    #If the user is already logged in then this if condition will activate and send the user to home page 
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    #Import the loginform defined in the forms.py file 
    form = loginForm()
    #When submit button is clicked this if condition will be activated
    if form.validate_on_submit():
        #Find the user with the give email in the database
        if form.email.data == "admin@gmail.com" and form.password.data == "admin123":
            return redirect(url_for("adminpage"))
        else:
            user = User.query.filter_by(email=form.email.data).first()
            print(user)
            #If user exists and password in a match the this if condition will activate 
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                #Login the user
                login_user(user, remember = form.remember.data)
                #Load the home page after verification
                return redirect(url_for('home'))
            #if the above condition of email id and password were enter wronged this part will be activated
            else:
                #Display this message
                flash("Login Unsuccessful. Wrong Email or password",'danger')
    #Load the Login page and pass the title and form to the frontend
    return render_template('login.html',title='Login',form=form)

#When logout page is opened this function will run
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
