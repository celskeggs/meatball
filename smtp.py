import datetime
import asyncore
import smtpd

class EmailServer(smtpd.SMTPServer):
	index = 0

	def process_message(self, p, mf, rt, data):
		filename = '/tmp/%s-%d.eml' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'), self.index)
		with open(filename) as f:
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
