# coding=utf-8

import requests, BeautifulSoup, time, datetime, re, json, random, pickle
from termcolor import colored


d = datetime.datetime.now().strftime('%H:%M:%S')

def log(event):
	# NIKE EVENT CHECKER
	print("N.E.C by Azerpas :: " + str(d) + " :: " + event)

class NEC(object):
	def __init__(self):
		self.events = {} # {'date':'','name':''}
		self.s = requests.session()
		self.url = "https://www.nike.com/events-registration/event?id="
		self.start = 91472 #91472
		self.country = ""
		self.proxy = {'http':'','https':'','ftp':''}
		self.headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

	def check(self,ad):
		req = self.s.get(self.url+str(ad), headers = self.headers, proxies = self.proxy).text
		soup = BeautifulSoup.BeautifulSoup(req)
		script = soup.findAll('script')
		pattern = re.compile("""eventDetails":(.*),"languageLocales""") #nike.events.content = {(.*)
		fields = re.findall(pattern, script[4].text)
		try:
			m = json.loads(fields[0])
		except:
			theid = colored(str(ad),'blue')
			print("!!!!!!!!!!!!!!!!!!!!!!")
			print("ERROR: CAN'T READ DATA OF ID: " + theid)
			print("!!!!!!!!!!!!!!!!!!!!!!")
			return
		log("Data retrieved")
		if self.country != "":
			if m[0]['language']['countryCode'] != self.country:
				return

		name = colored(m[0]['name'], 'red', attrs=['bold','underline'])
		country = colored(m[0]['language']['countryCode'], 'blue')
		description = colored(m[0]['description'].replace("<br>", "").replace("<br />","").replace("<br/>","").replace("&amp;","&") , 'yellow').replace("</b>","").replace("<b>","")
		url = colored(m[0]['eventUrl'], 'blue') 
		print("-------------------------")
		print("||" + name + "||" + country)
		print("||" + description + "||")
		print("||" + url + "||")
		print("-------------------------")
		self.events = {'name':name,'description':description,'url':url,'country':country,'id':ad}
		self.save()

	def save(self):
		log("Saving event into 'event.txt'")
		try:
			file = open('event.txt','r')
			print('TXT already exists')
			try:
				Filelist = pickle.load(file)
			except EOFError:
				print("--------------------")
				print("Event error")
				print("--------------------")
				return
			Filelist.append(self.events)
			file = open('event.txt','w')
			pickle.dump(Filelist,file)

		except IOError as e:
			print('Creating txt')
			file = open('event.txt','w')
			Filelist = []
			Filelist.append(self.events)
			#file.write(Filelist)
			pickle.dump(Filelist,file)
			#file.write('\n')
	print('Event successfuly saved')



	def main(self):
		log("Starting")
		print(colored("\nDo you want to search for events of a specific country?",'red'))
		aux = raw_input("Press fr, us, gb, etc... or return to continue: ")
		if aux in ['fr','us','tr','tw','la','gb','ru','pl','gr','ar','es','th','it','pt','nl','ar']:
			self.country = aux
		else:
			self.country = ""
		# fr us tr tw la gb ru pl gr ar es th
		while True:
			log("Scraping data of ID: " + str(self.start))
			self.check(self.start)
			time.sleep(random.uniform(0.3,0.6))
			self.start += 1
			print("\n")



if __name__ == "__main__":
	NEC = NEC()
	NEC.main()
