#IMPORTS
import network
import urequests as requests
import json
from machine import Pin
import time

#SETUP
led = Pin(2, Pin.OUT)
b0,b1,b2 = True,False,False
bindex,bnum = -1,0
modules = ["ping","receive","send"]
module = ""

#FUNCTIONS
def getaccount():
    with open("account.txt","r") as f:
        username = f.readline().replace("\n","")
    if username == "":
        return None
    else:
        return username

def connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect('Borealis', 'pico-pico')

def get(endpoint):
    connect()
    response = requests.get(f'http://192.168.4.1{endpoint}')
    return response.text

def send(jsondata=None):
    connect()
    if jsondata is None:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
            data["log"] = data["log"]
        jsondata = data
    response = requests.post('http://192.168.4.1/', json=jsondata)

def display(string):
    print(string)
    #display code here

#MODULES
pinglst = []
receivelst = []
sendlst = []

def pingGET():
    try:
        username = getaccount()
        if username == None:
            accountlnk = get("/log").split("\n")[-1]
            if "Account '" in accountlnk and "' Created" in accountlnk:
                username = accountlnk.split("'")[1]
                with open("account.txt","w") as f:
                    f.write(username)
            else:
                return ["Connected","No Account Found"]
        money = get(f"/account?v=0&u={username}").split("\n\n")[0]
        return [f"Connected\n{username}",money]
        
    except:
        username = getaccount()
        if username:
            return [f"Disconnected\n{username}"]
        return ["Disconnected"]
def ping(item):
    global bnum
    bnum = 0
    
def receiveGET():
    pingget = "\n".split(get("/log"))
    return pingget[-10:]
def receive(item):
    send({"log":item})
    
def sendGET():
    sendget = get(f"/account?v=0&u={getaccount()}").split("\n\n")[1]
    return sendget
def send(item):
    send({"log":item})

#MAINLOOP
print("FEEDBACK Mode Activated")
# Start loop here
while True:
    if b0 and b1:
        b2 = True
        b0,b1 = False,False 
    elif b0:
        if bindex < len(modules) - 1:
            bindex += 1
        else:
            bindex = 0
    elif b1:
        if bnum < len(globals()[module + "lst"])-1:
            bnum += 1
        else:
            bnum = 0
        b1 = False
    else:
        continue
    module = modules[bindex]
    try:
        if b0 and not b2:
            item = eval(f"{module}GET()")[bnum]
            b0 = False
        else:
            item = globals()[module + "lst"][bnum]
        #OUTPUT
        display(item)
        if b2:
            eval("{module}(item)")
            b2 = False
    except Exception as e:
        bindex = 0
        print("Error path A: "+str(e))
# End loop here
