"""
Search.py
Functions for searching through the database

Mary Thompson
December 2012
"""

#Input: string tag, list of dictionarys dblist
#Returns ID of first photo found that has given tag
def get_id(tag, dblist):

    for entry in dblist:
	if tag in entry['keywords']:
	    return entry['id']
	else:
	    return 0

#Input list query color, list color being compared
#Returns the distance between the vectors
def get_sim(query, stored):

    diff = [pow((a-b),2) for a,b in zip(query,stored]
    return math.sqrt(sum(diff))


"""
So try something like

query = [123,53,63]
images = self.name_of_database_here.find( {'colors':{'$all':colors}} )

current = 999.999
previous = 999.999
closest = '' #Dont know if id is a string or number
for image in images:
    current = get_sim(query,image['color'])
    if current < previous:
	previous = current
	closest = image['id']

I hope I typed this right...
"""
