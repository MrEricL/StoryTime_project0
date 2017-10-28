import sqlite3
from db_builder import getPass, addUser


def authenticate(user, passw):
     info = getPass(user)
     if info == None:
         return -1
     elif info != passw:
          return -2
     else:
          return 1

if __name__ == '__main__': 
     print authenticate('manahal', 'mt123')
     print authenticate('joe', 'mt123')
     print authenticate('jack', 'mt123')
     

def register(user, passw):
     addUser(user,passw)

