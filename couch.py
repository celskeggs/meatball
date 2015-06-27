import couchdb

couch = couchdb.Server()
def get_db(name):
	if name in couch:
		return couch[name]
	else:
		print("Automatically created database", name)
		return couch.create(name)
