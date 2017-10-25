from db_builder import getInfo, addUser

BAD_USER = -1
BAD_PASS = -2
GOOD = 1

def authenticate(user, passw):
     info = getInfo(user)
     if info == None:
         return BAD_USER
     elif info != passw:
         return BAD_PASS
     else:
         return GOOD

print authenticate('manahal', 'mt123')
print authenticate('joe', 'mt123')
print authenticate('jack', 'mt123')


def register(user, passw):
     addUser(user,passw)
