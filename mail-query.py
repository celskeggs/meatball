import couch

maildb = couch.get_db("meatball_mail")

n = 0
for message in maildb:
	msg = maildb[message]
	print(message, msg.headers.get("subject", "No Subject"))
	n += 1

print("Found", n, "messages.")
