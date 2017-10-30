import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid


#==========================================================
'''
TABLE CREATION
Database usersandstories.db
Tables: users, stories, updates
'''

def tableCreation():
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #Create the users table
    user_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER);'
    c.execute(user_table)
    #Create the stories table
    stories_table = 'CREATE TABLE stories (storyID INTEGER, title TEXT, author INTEGER, content TEXT);'
    c.execute(stories_table)
    #Create the updates table
    update_table = 'CREATE TABLE updates (storyID INTEGER, contribution TEXT, contributor INTEGER);'
    c.execute(update_table)
    db.commit()
    db.close()

#==========================================================

#COUNTERS
#userID_counter = 0;  #helps to assign userID
#storyID_counter = 0; #helps to assign storyID

#==========================================================

#ADD VALUES TO TABLES

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def check_password(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

#add a user
def addUser(new_username, new_password):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #global userID_counter
    #new_userID = userID_counter
    #userID_counter += 1
    userCount = c.execute('SELECT COUNT(*) FROM users;')
    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    #new_userID += 1
    hash_pass = hash_password(new_password)
    print ('The string to store in the db is: ' + hash_pass)
    c.execute('INSERT INTO users VALUES (?,?,?)',[new_username, hash_pass, new_userID])
    db.commit()
    db.close()


#add a new story
def addStory(new_title, st_author, st_content):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #global storyID_counter
    #storyID_counter += 1
    #new_storyID = storyID_counter
    storyCount = c.execute('SELECT COUNT(*) FROM stories;')
    new_storyID = 0
    for x in storyCount:
        new_storyID = x[0]
        #print new_storyID
    #new_storyID += 1
    c.execute('INSERT INTO stories VALUES (?,?,?,?)',[new_storyID, new_title, st_author, st_content])
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, st_content, st_author])
    db.commit()
    db.close()


#make an update to a story
def addUpdate(new_storyID, new_content, new_contributor):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, new_content, new_contributor])
    stuff = c.execute('SELECT content FROM stories WHERE storyID= ' + str(new_storyID) + ';')
    old_content = stuff.fetchone()
    #print 'OLD CONTENT...'
    #print old_content
    final_content = old_content[0] +' ' + new_content
    #print 'NEW CONTENT...'
    #print final_content
    c.execute('UPDATE stories SET content ="' + final_content + '" WHERE storyID =' + str(new_storyID) + ';')
    db.commit()
    db.close()

def getLastEdit(st_ID):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    all_edits = c.execute('SELECT contribution FROM updates WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in all_edits:
        retVal = x[0]
    db.close()
    return retVal

def getFullStory(st_ID):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    story = c.execute('SELECT content FROM stories WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in story:
        retVal = x[0]
    db.close()
    return retVal

def getTitle(st_ID):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    retTitle = c.execute('SELECT title FROM stories WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in retTitle:
        retVal =  x[0]
    db.close()
    return retVal

def checkUsername(userN):
    f="data/usersandstories.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

#==========================================================
#ACCESSORS
def getPass(username):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

def getUserID(username):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, userID FROM users"
    info = c.execute(command)

    retVal = None
    for user in info:
        if str(user[0]) == username:
            retVal = str(user[1])
    db.close()
    return retVal

def getName(ID):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    info = c.execute('SELECT username FROM users WHERE userID =' + str(ID) + ';')
    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

def seeStories():
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops

    command = 'SELECT storyID, title, author FROM stories;'
    return c.execute(command)

#==========================================================
#HELPERS
def hasContributed(thisUser,thisStory):
    f="data/usersandstories.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    con = c.execute('SELECT contributor FROM updates WHERE storyID = ' + str(thisStory) + ';')
    
    for row in con:
        #print "This contributor edited the story:"
        #print row
        if str(row[0])==str(thisUser):
            db.close()
            #print True
            return True
        #print row[0]
    db.close()
    return False


if __name__ == '__main__':     
    #TESTING
    tableCreation()

    #add users
    addUser('manahal', 'mt123')
    addUser('joe', 'fgh349')
    addUser('bob', 'iryg9137')
    addUser('sasha', 'jfhv173')
    
    #make story
    addStory('welcome', 0, 'well hello there')
    addStory('bye', 3, 'we enjoyed the time')
    
    #update story
    addUpdate(0, 'how are you doing', 1)
    addUpdate(1, 'we will see you later', 3)
    addUpdate(0, 'doing fine', 2)
    addUpdate(1, 'kk will do', 0)
    
    #get the last edit
    getLastEdit(0)
    getLastEdit(1)
    
    #get full story
    print getFullStory(0)
    print getFullStory(1)
    
    #get title
    print getTitle(0)
    print getTitle(1)

    print getUserID('manahal')
    print getUserID('sasha')

    print getName(0)
    print getName(1)
    print getName(2)
    print getName(3)
    
    #check if somebody's edited the story
    print "Has user 0 edited story 0 (should be True): " + str( hasContributed(0,0) )
    print "Has user 6 edited story 0 (should be False): " + str( hasContributed(6,0) )
    print "Has user 3 edited story 1 (should be True): " + str( hasContributed(3,1) )
    print "Has user 2 edited story 0 (should be True): " + str( hasContributed(2,0) )


