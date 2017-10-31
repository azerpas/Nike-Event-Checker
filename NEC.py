# coding=utf-8

import requests, BeautifulSoup, pickle, time, datetime, re, json


d = datetime.datetime.now().strftime('%H:%M:%S')

def log(event):
	# NIKE EVENT CHECKER
	print("N.E.C by Azerpas :: " + str(d) + " :: " + event)

class NEC(object):
	def __init__(self):
		self.events = [] # {'date':'','name':''}
		self.s = requests.session()
		self.url = "https://www.nike.com/events-registration/event?id="
		self.start = "91597"

	def check(self):
		req = self.s.get(self.url+self.start).text
		soup = BeautifulSoup.BeautifulSoup(req)
		script = soup.findAll('script')
		pattern = re.compile("""eventDetails":(.*),"languageLocales""") #nike.events.content = {(.*)
		fields = re.findall(pattern, script[4].text)
		
		m = json.loads(fields[0])
		print(m)

	def main(self):
		self.check()

if __name__ == "__main__":
	NEC = NEC()
	NEC.main()
