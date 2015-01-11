import requests
from bs4 import BeautifulSoup as BS
import time
from sys import argv

script, filename = argv

def cmpcgpa(x, y):
	if x[2] > y[2]:
		return 1
	else:
		return -1

def cmpsgpa(x, y):
	if x[1] > y[1]:
		return 1
	else:
		return -1


url = 'http://117.211.91.61/web/Default.aspx/'

start = raw_input("Enter your year code (eg - EL112 if your roll no is EL112001):")
sem = raw_input("Enter sem:")

reglist = []
rolls = open(filename)
for roll in rolls.readlines():
	reglist.append(roll)

ranklist = []

def getState(url, data=None, headers=None):
	r = requests.post(url, data=data, headers=headers)
	soup = BS(r.text)
	state = soup.findAll(attrs={'name': '__VIEWSTATE'})[0]['value']
	return state

i = 0

headers = {
	'Host': '117.211.91.61',
	'Connection': 'keep-alive',
	'Content-Length': '377',
	'Cache-Control': 'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/	xml;q=0.9,image/webp,*/*;q=0.8',
	'Origin': 'http://117.211.91.61',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 	(KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Referer': 'http://117.211.91.61/web/Default.aspx',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.8,hi;q=0.6'
}

data_raita = {
	"ToolkitScriptManager1_HiddenField": "",
	"__EVENTTARGET": "",
	"__EVENTARGUMENT": "",
	"__VIEWSTATE": '',
	'txtRegno': '',
	'btnimgShow.x': '34',
	'btnimgShow.y': '10'
}

data_soup = {
	"ToolkitScriptManager1_HiddenField": "",
	"__EVENTTARGET": "",
	"__EVENTARGUMENT": "",
	"__VIEWSTATE": '',
	'txtRegno': '',
	'ddlSemester': '',
	'btnimgShowResult.x': '25',
	'btnimgShowResult.y': '11'
}

while i < len(reglist):
	try:
		bawasir = getState(url)
	except:
		continue
	data_raita['__VIEWSTATE'] = bawasir
	data_raita['txtRegno'] = start + str(reglist[i])
	try:
		state = getState(url, data=data_raita, headers=headers)
	except:
		continue

	data_soup['__VIEWSTATE'] = state
	data_soup['ddlSemester'] = sem
	data_soup['txtRegno'] = start + reglist[i]

	try:
		s = requests.post(url, headers=headers, data=data_soup)
	except:
		continue

	soup = BS(s.text)
	#print s.text

	try:
		roll = str(soup.find(id="lblSRollNo").text)
		cgpa = str(soup.find(id="lblCPI").text)
		sgpa = str(soup.find(id="lblSPI").text)
	except:
		i += 1
		continue

	ranklist.append((roll, sgpa, cgpa))
	#print roll, " ", sgpa, " ", cgpa

	time.delay(2)#because the server appears to not respond if queries are made back-to-back without any delay
	i += 1

#print ranklist

ranklist.sort(cmp = cmpsgpa, reverse=True)
c = 1
print "SGPA Wise"
print "-" * 10
for item in ranklist:
	print c, ".", item[0], "\t\t",
	print "%s\t%s" % (item[1], item[2])
	c += 1

ranklist.sort(cmp = cmpcgpa, reverse=True)
c = 1
print "CGPA Wise"
print "-" * 10
for item in ranklist:
	print c, ".", item[0], "\t\t",
	print "%s\t%s" % (item[1], item[2])
	c += 1
