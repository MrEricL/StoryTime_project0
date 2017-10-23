from flask import Flask, render_template, request, session, url_for, flash
import os

app = Flask(__name__)

@app.route('/')
def root():
    #redirect to home if there is a session
    #otherwise display login/register page 

#authenticate user credentials
@app.route('/login')
def login():
    #if successful, redirect to home
    #otherwise redirect back to root?

#create new account 
@app.route('/register')
def register():
    #if there isn't an existing user w/ same username, add to users table 
    #otherwise redirect to root with flashed message 
    
#log out user
@app.route('/logout/')
def logout():
    #pop out user from session
    #flash logout message
    #redirect to root

#user dashboard 
@app.route('/home')
def home():
    #render template for dashboard

#allows user to view stories/add to stories (unless we want to separate the two)
@app.route('/view')
def view():
    #render template

#allows user to create new story 
@app.route('/newstory')
def new():
    #render template
