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
updates_table = 'CREATE TABLE updates (storyID INTEGER, update TEXT, contributor INTEGER);'
c.execute(updates_table)

#==========================================================

#COUNTERS
userID_counter = 0;  #helps to assign userID
storyID_counter = 0; #helps to assign storyID

#==========================================================

#ADD VALUES TO TABLES

#add a user
def addUser(new_username, new_password):
    new_userID = userID_counter
    userID_counter += 1
    c.execute('INSERT INTO users VALUES (?,?,?)',[new_username, new_password, new_userID])


#add a new story
def addStory(new_title, st_author, st_content):
    new_storyID = storyID_counter
    storyID_counter += 1
    c.execute('INSERT INTO stories (?,?,?,?)', [new_storyID, new_title, st_author, st_content])
    c.execute('INSERT INTO updates (?,?,?)', [new_storyID, st_content, st_author])


#make an update to a story
