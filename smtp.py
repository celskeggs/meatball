import datetime, asyncore, smtpd, os

directory = "/var/lib/meatball/mail"

class EmailServer(smtpd.SMTPServer):
	index = 0

	def process_message(self, p, mf, rt, data):
		filename = '%s/%s-%d.eml' % (directory, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), self.index)
		with open(filename, "w") as f:
			f.write(data)
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
