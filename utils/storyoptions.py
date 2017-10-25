import db_builder

def viewStory(thisUser,thisStory):
    if db_builder.hasContributed(thisUser,thisStory):
        return db_builder.getFullStory(thisStory)
    else:
        return db_builder.getLastEdit(thisStory)

print viewStory(0,0)
print viewStory(6,0)
