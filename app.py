from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)  #for the cookies

logged = True
#need a method to update this

BAD_USER = -1
BAD_PASS = -2
GOOD = 1

@app.route('/')
def root():
    #redirect to home if there is a session
    #otherwise display login/register page
    #if <logged in>: 
    #   return redirect(url_for("home"))
    if logged:
        return redirect("home")
    else:
        return render_template("login.html")
    #return redirect(url_for("login"))

#authenticate user credentials
@app.route('/login', methods = ['POST'])
def login():
    user = request.form['user']
    passw = request.form['pass']

    result = authenticate(user, passw)

    #if successful, redirect to home
    #otherwise redirect back to root?
    if result == GOOD:
        return redirect( url_for('home') )
    if result == BAD_USER:
        pass
    if result == BAD_PASS:
        pass
    return redirect( url_for('root') )

#user dashboard 
@app.route('/home')
def home():
    #render template for dashboard
    if logged:
        return render_template("home.html")
    else:    
        return redirect(url_for("login"))
        

#allows user to view stories/add to stories (unless we want to separate the two)
@app.route('/view')
def view():
    #render template
    if logged:
        return render_template("addview.html")
    else:    
        return redirect(url_for("login"))

#allows user to create new story 
@app.route('/newstory')
def new():
    #render template
    if logged:
        return render_template("new.html")
    else:    
        return redirect(url_for("login"))
    
if __name__ == '__main__':
    app.run(debug=True)

#log out user
@app.route('/logout')
def logout():

    #pop out user from session
    #flash logout message
    return redirect("login")



''' JUNK PILE
#create new account 
@app.route('/register')
def register():
    #if there isn't an existing user w/ same username, add to users table 
    #otherwise redirect to root with flashed message 
'''
