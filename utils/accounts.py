import sqlite3
from db_builder import getPass, addUser, check_password


def authenticate(user, passw):
     info = getPass(user)
     if info == None:
         return -1
     elif check_password(info, passw):
          return 1
     else:
          return -2

if __name__ == '__main__': 
     print authenticate('manahal', 'mt123')
     print authenticate('joe', 'mt123')
     print authenticate('jack', 'mt123')
     

def register(user, passw):
     addUser(user,passw)

