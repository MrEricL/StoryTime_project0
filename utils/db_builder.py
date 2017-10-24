import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="usersandstories.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()         #facilitates db ops

#==========================================================
'''
TABLE CREATION
Database usersandstories.db
Tables: users, stories, updates
'''

#Create the users table
user_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER);'
c.execute(user_table)

#Create the stories table
stories_table = 'CREATE TABLE stories (storyID INTEGER, title TEXT, author INTEGER, content TEXT);'
c.execute(stories_table)

#Create the updates table
update_table = 'CREATE TABLE updates (storyID INTEGER, contribution TEXT, contributor INTEGER);'
c.execute(update_table)

#==========================================================

#COUNTERS
userID_counter = 0;  #helps to assign userID
storyID_counter = 0; #helps to assign storyID

#==========================================================

#ADD VALUES TO TABLES

#add a user
def addUser(new_username, new_password):
    global userID_counter
    new_userID = userID_counter
    userID_counter += 1
    c.execute('INSERT INTO users VALUES (?,?,?)',[new_username, new_password, new_userID])


#add a new story
def addStory(new_title, st_author, st_content):
    global storyID_counter
    new_storyID = storyID_counter
    storyID_counter += 1
    c.execute('INSERT INTO stories VALUES (?,?,?,?)',[new_storyID, new_title, st_author, st_content])
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, st_content, st_author])


#make an update to a story
def addUpdate(new_storyID, new_content, new_contributor):
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, new_content, new_contributor])
    c.execute('SELECT content FROM stories WHERE storyID= ' + str(new_storyID) + ';')
    old_content = c.fetchone()
    #print 'OLD CONTENT...'
    #print old_content
    final_content = old_content[0] +' ' + new_content
    #print 'NEW CONTENT...'
    #print final_content
    c.execute('UPDATE stories SET content ="' + final_content + '" WHERE storyID =' + str(new_storyID) + ';')

def getLastEdit(st_ID):
    all_edits = c.execute('SELECT contribution FROM updates WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in all_edits:
        retVal = x[0]
    print retVal


#TESTING
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
#getLastEdit(1)


db.commit()
db.close()
