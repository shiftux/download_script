# tools needed
# !!! not needed ! http://www.crummy.com/software/BeautifulSoup/#Download
# https://pypi.python.org/pypi/feedparser
# https://pypi.python.org/pypi/setuptools#downloads

""" info on the feedparser
#the entries of the feed (every downloadable element (movie, serie etc.) are accessed with
#wrzko.entries[i] 			#where i>=0 is the number of the elements
len(wrzko.entries) 			#gives the current amount of entries in the feed
wrzko.entries[0].title 		#gives the title of the entry
wrzko.entries[0].published	#tells you when the latest entry was published, alternatively use wrzko.entries[0].published_parsed
wrzko.entries[0].id 		#gives a unique id of the post
wrzko.entries[0].content 	#gives the content of the entry (here all the links are stored)
"""

import feedparser
import os
import subprocess
import time
from datetime import datetime

#################
# global vars
#################

#downloading = False
url = 'http://www.wrzko.eu/feed/'

series=[
"how.i.met.your.mother",
"south.park",
"family.guy",
"homeland",
"american.dad",
"two.and.a.half.men",
"the.big.bang.theory",
"the.simpsons",
"true.blood",
"futurama",
"game.of.thrones",
"new.girl",
"greys.anatomy",
"girls.s03",
"nashville"
]

movies=[
"Captain.Phillips",
"Thor",
"American.hustle",
"catching.fire",
"rush",
"Mandela.Long.Walk.to.Freedom", 
"the.butler"
]

#################
# defining the aid functions
#################
"""
def getId():
	s=id.find("p=")+2
	gotId=id[s:len(id)]
	return gotId"""

def init():
	if not os.path.isfile(".pyload/downloadedIds"):
		subprocess.call("touch .pyload/downloadedIds", shell=True)
	if not os.path.isfile(".pyload/download_log.txt"): 
		subprocess.call("touch .pyload/download_log.txt", shell=True)	
	if not os.path.isfile(".pyload/temp_links.txt"):
		subprocess.call("touch .pyload/temp_links.txt", shell=True)

def writeId(id):
	f=open(".pyload/downloadedIds", 'a')
	f.writelines(id+"\n")
	f.close()

def checkDownloaded(id):
	f=open(".pyload/downloadedIds", 'r')
	readid=f.readline()
	while readid != '':
		if readid.find(id)>-1:
			f.close()
			#print("break")
			return True
			break
		else:
			readid=f.readline()
	else:
		f.close()
		return False

def getLinks():
	#get the uploaded part of the text
	startindex=cont.find("ul.to")
	endindex=cont.find("\"", startindex, len(cont))

	indices=[startindex]
	oldstartindex=startindex
	starts=[]
	ends=[endindex]
	links=[]
	final=[]

	#find all other uploaded parts
	while startindex>0:
		startindex=cont.find("ul.to", startindex+5, len(cont))
		if startindex == -1:
			for i in range(len(indices)):
				if i % 2 == 0:
					starts.append(indices[i])
			break
		else:
			indices.append(startindex)
	for i in range(len(starts)-1):
		endindex=cont.find(("\""), starts[i+1], len(cont))
		ends.append(endindex)
	for i in range(len(starts)):
		links.append("http://" + cont[starts[i]:ends[i]])

	#check if its a single file or a partitioned file, only take single file if available
	for x in links:
		if x.find(".avi")>0:
			final.append(x)
			break
		elif x.find(".mkv")>0:
			final.append(x)
			break
		elif x.find(".mp4")>0:
			final.append(x)
			break	
		else:
			final = links	
	return final

def checkSeries(title):
	result=False
	for x in series:
		if title.find(x.lower())>-1:
			result=True
			break
	return result

def checkMovies():
	result=False
	if title.find("1080p.bluray")>-1:
		for x in movies:
			if title.find(x.lower())>-1:
				result=True
	return result
	
def writeLog(title):
	f=open(".pyload/download_log.txt", 'a')
	f.write("downloaded " + title + " at " + str(datetime.now().time()) + " " + str(datetime.now().date()) +"\n")
	f.close()
	
def writeLinks(links):
	f=open(".pyload/temp_links.txt", 'a')
	for line in links:
		f.write(line+"\n")
	f.close()
	toDownload=[]

def replace_links_file():
	subprocess.call("rm .pyload/links.txt", shell=True)
	subprocess.call("mv .pyload/temp_links.txt .pyload/links.txt", shell=True)  
	

"""def writeSeries():
	f=open("series", 'w')
	f.writelines(getLinks())
	f.close()"""


#######################
# the script
#######################

wrzko = feedparser.parse(url)
toDownload=[]
init()

for entry in wrzko.entries:

	title=entry.title.lower()
	#print(title)
	id=entry.id[entry.id.find("p=")+2:len(entry.id)]
	cont=str(entry.content)

	#download the entry if it is a desired serie
	if checkSeries(title) and not checkDownloaded(id):
		print("doing it for " + title)
		links = getLinks()
		if title.find("&") >-1:
			title=title[0:title.find("&")]
		toDownload.append("["+title[0:30]+"]")
		for x in links:
			### for jdownloader direct launch
			#theCall="JDownloader -H -d -add " + x
			#subprocess.call(theCall, shell=True) 
			#time.sleep(1)
			toDownload.append(x)
		writeId(id)
		writeLog(title)
		writeLinks(toDownload)
		time.sleep(1)
		#downloading=True
	#else:
		#print("noooo")


	
	if checkMovies() and not checkDownloaded(id):
		links = getLinks()
		toDownload.append("["+title+"]")
		for x in links:
			### for jdownloader direct launch
			#theCall="JDownloader -H -d -add " + x
			#subprocess.call(theCall, shell=True) 
			#time.sleep(1)
			toDownload.append(x)
		writeId(id)
		writeLog(title)
		writeLinks(toDownload)
		time.sleep(1)
		#downloading=True
	#else:
		#print("noooo")


"""
if not downloading:
	subprocess.call("/usr/share/pyload/pyLoadCore.py -q", shell=True) 
	time.sleep(5)
	subprocess.call("rm .pyload/files.db", shell=True) 
	time.sleep(1)
	subprocess.call("/usr/share/pyload/pyLoadCore.py --daemon", shell=True) 
	"""

replace_links_file()

print("script executed at " + str(datetime.now().time()) + " " + str(datetime.now().date()))

