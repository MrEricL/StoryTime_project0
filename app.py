from flask import Flask, render_template, request, session, url_for, flash, redirect, Markup
from utils.accounts import authenticate
from utils.htmlBuilder import buildTable
from utils.db_builder import checkUsername, addUser, addStory, getUserID, seeStories, hasContributed, getName, getFullStory, getLastEdit, tableCreation
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)  #for the cookies

BAD_USER = -1
BAD_PASS = -2
GOOD = 1

user = ""

@app.route('/')
def root():
    #redirect to home if there is a session
    #otherwise display login/register page
    if session.has_key('user'):
        return redirect("home")
    else:
        return render_template("login.html")
 
#authenticate user credentials
@app.route('/login', methods = ['POST','GET'])
def login():
    user = request.form['user']
    #print user
    passw = request.form['pass']
    #print passw

    result = authenticate(user, passw)
    #print result

    #if successful, redirect to home
    #otherwise redirect back to root with flashed message 
    if result == GOOD:
        session['user'] = user
        #for x in session:
            #print session[x]
        return redirect( url_for('home') )
    if result == BAD_USER:
        flash('Incorrect username. Please try again.')
        return redirect( url_for('root') )
    if result == BAD_PASS:
        flash('Incorrect password. Please try again.')
        return redirect( url_for('root') )
    return redirect( url_for('root') )

@app.route('/register', methods = ['POST', 'GET'])
def register():
    user = request.form['user']
    print user
    password = request.form['pass']
    print password

    if checkUsername(user):
        flash('Username unavailable. Please try another username.')
        return redirect(url_for('root'))
    else:
        addUser(user,password)
        session['user'] = user
        return redirect( url_for('home'))
    
    
#user dashboard 
@app.route('/home', methods = ['POST','GET'])
def home():
    if 'user' in session:
        cursor = seeStories()
        entries = [dict(storyID=str(entry[0]), title=str(entry[1]), author=str(getName(str(entry[2]))), option=hasContributed(entry[2],entry[0]))   for entry in cursor.fetchall()]
        print "Current userID:"
        print getUserID(session['user'])
        print "Has user 0 contributed to story 0:"
        print hasContributed(getUserID(session['user']), 0)
        return render_template("home.html", code=Markup(buildTable(entries,session['user'])))
        
    else:    
        return redirect(url_for("root"))
        

#allows user to view stories/add to stories (unless we want to separate the two)
@app.route('/view', methods = ['POST', 'GET'])
def view():
    #render template
    if 'user' in session:
        thisStory = request.form['thisStory']
        #hasCont = hasContributed(session['user'],thisStory)
        #if hasCont:
            #content = getFullStory(thisStory)
        #else:
            #content = getLastEdit(thisStory)
        #return render_template("addview.html", content=content, hasCont=hasCont)
        return "in progress..."
    else:    
        return redirect(url_for("root"))

#allows user to create new story 
@app.route('/newstory', methods = ['POST','GET'])
def newstory():
    if 'user' in session: 
        return render_template("new.html")
    else:    
        return redirect(url_for("root"))

@app.route('/new', methods = ['POST','GET'])
def new():
    title = request.form['title']
    print title
    user = getUserID(session['user'])
    content = request.form['newStoryText']
    print content
    addStory(title, user, content)
    flash('You have successfully created a new story. Watch its progress below!')
    return redirect(url_for("home"))
    

#log out user
@app.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))




    
if __name__ == '__main__':
    app.run(debug=True)

