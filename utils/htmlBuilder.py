from db_builder import hasContributed, getUserID
tableRealHead='''
<table style="width:100%">
      <tr>
        <th></th>
        <th>Title</th>
        <th>Author</th>
        <th>Status</th>
      </tr>
'''
tableHead='''

      <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
          <form method="GET" action = "/view">
          <input type="hidden" name="StoryID" value= %s> 
          '''

tableView='''
<input type="submit" value="View">
</form>
</td>
</tr>
'''

tableAdd='''
<input type="submit" value="Add">
</form>
</td>
</tr>
'''

tableEnd='''
</table>
'''

def buildTable(entries, user):
    listCont = contributeTable (entries, user)
    htmlString=tableRealHead
    counter=0
    for each in entries:
        htmlString = htmlString + tableHead % (each['storyID'], each['title'], each['author'], each['storyID'])
        if listCont[counter] == None:
          htmlString = htmlString + tableAdd
        else:
          htmlString = htmlString + tableView
        counter = counter + 1
    htmlString= htmlString+tableEnd
    return htmlString

def contributeTable(entries,user):
  userID = getUserID(user)
  ret = []
  for each in entries:
    ret.append(hasContributed(userID,each['storyID']))
  return ret



