from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])      # now accepts both GET and POST requests
def login():
    if request.method=='POST':
        email = request.form.get('email');
        password = request.form.get('password');    
    
        user = User.query.filter_by(email=email).first()  # Check if the user email exists
        if user: 
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='message')
                login_user(user, remember=True)  # Log the user in
                return redirect(url_for('views.notes'))
            else : 
                flash("Incorrect password, try again.", category='error')
        else: 
            flash("User account does not exist.", category='error')
    return render_template("login.html", user=current_user)     # sets the user to current user to be used in auth purposes later

@auth.route('/logout')
@login_required
def logout():
    logout_user()       # log out the user
    flash("Logged out successfully!", category='message')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()  # Check if the user email exists
        if user:
            flash("Email already exists. Choose another email ", category='error')  
        elif len(email) < 4:
           flash("Email must be greater than 4 characters.", category='error')
        elif password1 != password2:    # Check if the passwords match
            flash("Passwords don\'t match.", category='error')
        elif len(password1) < 6:
            flash("Password must be at least 6 characters.", category='error')
        else:
            flash("Account created successfully!", category='message')    
            # Add user to database
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))  # Hash the password before storing it )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.notes'))      # home() function of views.py

    return render_template("signup.html")