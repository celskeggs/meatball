import datetime, asyncore, smtpd, os, couch, email

maildb = couch.get_db("meatball_mail")

REVISION = 1
def convert_message(msg):
	out = {"revision": REVISION, "unixfrom": msg.get_unixfrom(), "content-type": msg.get_content_type()}
	payload = msg.get_payload()
	charset = msg.get_charset()
	out["charset"] = charset.input_charset if charset != None else None
	if type(payload) == str:
		out["body"] = payload
	else:
		out["body"] = [convert_message(m) for m in payload]
	out["headers"] = list(msg.items())
	out["preamble"] = msg.preamble
	out["epilogue"] = msg.epilogue
	out["defects"] = msg.defects

class EmailServer(smtpd.SMTPServer):
	index = 0
	def process_message(self, p, mf, rt, data):
		name = '%s-%d' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'), self.index)
		obj = {"revision": REVISION, "peer": p, "mailfrom": mf, "recipients": rt, "success": True}
		try:
			message = email.message_from_string(data)
			obj["message"] = convert_message(message)
		except Exception as e:
			obj["success"] = False
			obj["source"] = data
			obj["failure"] = e
		maildb[name] = obj
		print(filename, "received")
		self.index += 1

def run():
	EmailServer(('', 25), None)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print("Interrupted!")

if __name__ == '__main__':
	run()
