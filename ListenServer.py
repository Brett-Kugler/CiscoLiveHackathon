from twisted.web import server, resource
from twisted.internet import reactor
import sys
import requests
import logging
import plotlyInterface

def doRequestsDebug():
    # These two lines enable debugging at httplib level (requests->urllib3->httplib)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    import httplib
    httplib.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig() 
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

class ListenServer(resource.Resource):
    isLeaf = True
    numberRequests = 0
    
    def __init__(self):
        self.activeEvent=False
        self.plotDataList=[]
        self.noMoreWrites = False

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        return "I am request #" + str(self.numberRequests) + "\n"

    def render_POST(self, request):
        global messageCount
        global readingList
        if "/rumble" in request.path:
            # do light
            val=request.args['value'][0]
            msg="[{0}]".format(messageCount)+" Vibration Sensor: Got "+ str(val) + " from sensor.            " + "\r"
            sys.stdout.write(msg)
            messageCount+=1
            reactor.callFromThread(self.evaluateEventTrigger,int(val))
            return "ok"

    def evaluateEventTrigger(self, newInput):
        global readingList
        #global pI

        readingList.insert(0,newInput)
        variance=0
        self.sendToGraph(newInput,pI=None)

        # look at the last 10 readings to determine variance
        if len(readingList)>10:
            readingList.pop()
        for val in readingList:
            variance+=abs(500-val)

        triggerVal=variance/len(readingList)

        if triggerVal > 100:
            if not self.activeEvent:
                print "\nWe have an event"
                self.activeEvent=True
                self.sendToCMx(self.activeEvent)
        else:
            if self.activeEvent:
                self.activeEvent=False
                self.sendToCMx(self.activeEvent)
                print "\nEvent is over"


    def sendToCMx(self,active):
        # Notify CMx host of our status
        headers={'Accept':'application/json'}
        payload = {'quake': str(active)}
        r=requests.get("http://10.10.30.189:3000/quake", params=payload, headers=headers, verify=False, auth=None)

    def sendToGraph(self,data,pI):
        if len(self.plotDataList)<180:
            self.plotDataList.append(data)
        else:
            if not self.noMoreWrites:
                self.noMoreWrites=True
                f=open('datastream.txt','w')
                for entry in self.plotDataList:
                    f.write(str(entry)+",")
                f.close()
        #pI.plotData(data)

messageCount=0
readingList=[]

# Enable or Disable this call for requests debug
doRequestsDebug()
#pI = plotlyInterface.plotlyInterface()
#pI.setup()
#pI.openStream()
print "Starting Web Server"
reactor.listenTCP(8080, server.Site(ListenServer()))
reactor.run()
#pI.closeStream()