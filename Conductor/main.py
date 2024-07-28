#IMPORTS
import network
import time
import socket
import mode as _
import connect as __
import _thread
from machine import Pin
import json
#SETUP
addrlst = []
responses = []
amounts = []
money = ""
with open("settings.txt","r") as f: 
    NAME = f.readline().strip()
with open('commands.txt',"r") as f:
    commands = f.readlines()
FEEDBACK = True
#FUNCTIONS
def getdata(username):
    with open("accounts.csv","r") as f:
        lines = f.readlines()
        for i in lines:
            parts = i.replace("\n","").split(",")
            if parts[0] == username:
                return parts[1],parts[2],parts[3],parts[4]
def execute(string):
    dictionary = eval(string)
    def log(dictionary):
        if "log" in dictionary:
            logstr=dictionary['log']
            with open("log.txt","r") as f:
                lines = f.readlines()
                if len(lines) < 100:
                    with open("log.txt","a") as f:
                        f.write(logstr + "\n")
                else:
                    with open("log.txt","w") as f:
                        f.write("".join(lines[1:])+logstr + "\n")
            return "Data Logged"
        else:
            return "Data Logging Failed"
    def command(dictionary):
        if "command" in dictionary:
            commandstr=dictionary['command']
            commands.append(commandstr)
            return "Command Added"
        else:
            return "Command Adding Failed"
    #ANALYSIS
    log(dictionary)
    command(dictionary)
def encrypt(string):
    pause = False
    chartable,newstring = {"a":"14","b":"15","c":"20","d":"21","e":"22","f":"23","g":"24","h":"25","i":"30","j":"31","k":"32","l":"33","m":"34","n":"35","o":"40","p":"41","q":"42","r":"43","s":"44","t":"45","u":"50","v":"51","w":"52","x":"53","y":"54","z":"55","0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"10","7":"11","8":"12","9":"13"," ":"  "},""
    for char in string:
        try:
            newstring += chartable[char]
        except:
            if char == ":":
                pause = True
                continue
            elif char == "." and pause == True:
                newstring += ":."
            else:
                newstring += "&" + char
    return newstring
def terminate(seconds):
    global commands
    button = Pin(19, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0 and "terminate:.0" not in commands:
            commands.append("terminate:.0")
            for i in commands:
                if "oscmd" in i:
                    commands.remove(i)
        else:
            continue
        time.sleep(seconds)
def web_page():
    global commands
    html,timestamp,t__ = '','0',0
    for command in commands:
        if not "timestamp" in command and not "=" in command:
            html = html + encrypt(command.replace("\n","").replace("\r","")) + ";,"
        else:
            if "=" in command:
                t__ = int(command.split("=")[-1])
            else:
                timestamp_ = command.replace("\n","").replace("\r","").split(":.")[1]
                timestamp = t__+int(timestamp_.split("t")[-1])
    return html,timestamp
def ap_mode(ssid, password):
    global addrlst, FEEDBACK
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while ap.active() == False:
        pass
    print('IP Address To Connect to:: http://' + ap.ifconfig()[0])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      if str(addr).split(",")[0] not in addrlst:
          addrlst.append(str(addr).split(",")[0])
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      if "Adafruit CircuitPython" in str(request) and "POST" in str(request):
          if FEEDBACK:
              string = "{" + str(request).split("GET")[-1].split("{")[-1][:-1]
              print(string);execute(string)
          FEEDBACK = not FEEDBACK
      elif "Borealis Client" in str(request) and "POST" in str(request):
          string = "{" + str(request).split("GET")[-1].split("{")[-1][:-1]
          print(string);execute(string)
      htmlcontent,timestamp = web_page()
      sitedir = str(request).split(" HTTP/1.1")[0].split(" ")[1]
      print(sitedir)
      if sitedir == "/log":
          with open("log.txt","r") as f:
              response = "".join(f.readlines())
      elif "/account" in sitedir:
          if sitedir == "/account":
              response = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #121212;
            color: #ffffff;
            font-family: 'Nunito', sans-serif;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .input-box {
            margin: 10px 0;
            padding: 10px;
            width: 200px;
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Nunito', sans-serif;
        }
        .button {
            margin: 10px 0;
            padding: 10px;
            width: 200px;
            border: none;
            border-radius: 5px;
            background-color: #6200ee;
            color: #ffffff;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
        }
        .button:hover {
            background-color: #3700b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <input id="username" class="input-box" type="text" placeholder="Username">
        <input id="password" class="input-box" type="password" placeholder="Password">
        <button class="button" onclick="login()">Login</button>
    </div>
    <script>
        function login() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            var url = '/account?v=1&u=' + encodeURIComponent(username) + '&p=' + encodeURIComponent(password);
            window.location.href = url;
        }
    </script>
</body>
</html>
"""
          else:
              try:
                  variables = sitedir.split("?")[1].split("&")
                  variables = [var.split("=")[1] for var in variables]
                  version = variables[0]
                  username = variables[1]
                  if version == "1":
                      password = variables[2]
                      with open("accounts.csv","r") as f:
                          txt="".join(f.readlines())
                          if username in txt:
                              password_,money,responses,amounts=getdata(username)
                              if password_ != password:
                                  response = "Error: Incorrect Password"
                          else:
                              responses = ["Message "+str(i) for i in range(1,11)]
                              amounts = [str(i)+".00" for i in range(1,11)]
                              money = "2.40"
                              with open("accounts.csv","a") as f:
                                  responses = ":.".join(responses)
                                  amounts = ":.".join(amounts)
                                  f.write(f"{username},{password},{money},{responses},{amounts}")
                      if response != "Error: Incorrect Password":
                          response = "1" # show account details, allow to edit
                  else:
                      password_,money,responses,amounts=getdata(username)
                      response = f"{money}\n"+responses.replace(":.","\n")+"\n"+amounts.replace(":.","\n")
              except Exception as e:
                  response = "Error: Mistyped Address"
                  print(e)
      else:
          response = str(len(addrlst))+".:"+str(timestamp)+".:"+htmlcontent
      print(response)
      if "</html>" not in response:
          responsefinal = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/plain\r
Content-Length: {len(response)}\r
\r
{response}"""
      else:
          responsefinal = response
      conn.send(responsefinal.encode('utf-8'))
      conn.close()
#MAINLOOP
if _.var() == False:
    print(f"Borealis Online (acc #01)\nRunning on name '{NAME}'")
    _thread.start_new_thread(terminate,[0.5])
    ap_mode(NAME,
        'pico-pico')
else:
    addcmd = __.run(commands)
    if addcmd != False:
        commands = addcmd
        print(f"Borealis Online (acc #02)\nRunning on name '{NAME}'")
        _thread.start_new_thread(terminate,[0.5])
        ap_mode(NAME,
        'pico-pico')
    else:
        with open("commands.txt","w") as f:
            f.write("\n".join(addcmd))
        print("Borealis Offline")
