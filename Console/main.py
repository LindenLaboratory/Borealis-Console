#IMPORTS
import io
from machine import Pin, PWM
import utime
from PicoOLED1point3spi import OLED_1inch3
import micropython
import network
import urequests as requests
import json

#SETUP
b0 = Pin(15, Pin.IN, Pin.PULL_UP)
b1 = Pin(17, Pin.IN, Pin.PULL_UP)
error = "404"
username = ""
money = 0.00
line = 1
bindex = -1

#FUNCTIONS
    #ABSTRACTION FUNCTIONS
def truncation(txt):
    if len(txt) > 16:
        txt = txt[:13] + "..."
    return txt
def split_text(text):
    initial_chunks = text.split('\n')
    final_chunks = []
    for chunk in initial_chunks:
        while len(chunk) > 16:
            if len(final_chunks) == 3:
                final_chunks.append(truncation(chunk[:16]))
                return final_chunks
            final_chunks.append(chunk[:16])
            chunk = chunk[16:]
        final_chunks.append(chunk)
        if len(final_chunks) == 4:
            break
    if len(final_chunks) > 4:
        final_chunks = final_chunks[:3]
        final_chunks.append(truncation(final_chunks.pop()))
    return final_chunks
    #DISPLAY FUNCTIONS
def display_clear_all(display):
    display.fill(0x0000)
def display_clear_line1(display):
    display.fill_rect(0, 0, 128, 16, display.black)
def display_clear_line2(display):
    display.fill_rect(0, 16, 128, 16, display.black)
def display_clear_line3(display):
    display.fill_rect(0, 32, 128, 16, display.black)
def display_clear_line4(display):
    display.fill_rect(0, 48, 128, 16, display.black)
def display_line1(display, txt):
    txt = truncation(txt)
    display_clear_line1(display)
    display.text(txt, 0, 4, display.white)
def display_line2(display, txt):
    txt = truncation(txt)
    display_clear_line2(display)
    display.text(txt, 0, 20, display.white)
def display_line3(display, txt):
    txt = truncation(txt)
    display_clear_line3(display)
    display.text(txt, 0, 36, display.white)
def display_line4(display, txt):
    txt = truncation(txt)
    display_clear_line4(display)
    display.text(txt, 0, 52, display.white)
def display_splash(display,a,b):
    display_clear_all(display)
    display.rect(0, 0, 128, 64, display.white)
    spacea = round(((16-len(a))/2))*" "
    spaceb = round(((16-len(b))/2))*" "
    a = spacea + a + spacea
    b = spaceb + b + spaceb
    display.text(a, 0, 22, display.white)
    display.text(b, 0, 40, display.white)
    utime.sleep(0.1)
    display.show()
    utime.sleep(5)
    display_clear_all(display)
    display.show()
    utime.sleep(0.1)
def display_disconnected(display,line):
    global error
    eval(f'display_line{str(line)}(display, "Failed")')
    display.show()
    utime.sleep(1)
    display_clear_all(display)
    display.rect(0, 0, 128, 64, display.white)
    display.text("  Disconnected  ", 0, 22, display.white)
    display.text(f"      e{error}      ", 0, 40, display.white)
    utime.sleep(0.1)
    display.show()
    while b0.value() == 1 and b1.value() == 1:
        pass
        utime.sleep(0.5)
def display_text(display,txt):
    display.clear()
    chunks = split_text(txt)
    display_line1(display,chunks[0])
    display_line2(display,chunks[1])
    display_line3(display,chunks[2])
    display_line4(display,chunks[3])
    display.show()

    #NETWORK FUNCTIONS
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Borealis', 'pico-pico')
    for _ in range(5):
        utime.sleep(1)
        if wlan.isconnected():
            return True
    return False
def getaccount():
    with open("account.txt","r") as f:
        username = f.readline().replace("\n","")
    if username == "":
        return None
    else:
        return username
def get(endpoint):
    response = requests.get(f'http://192.168.4.1{endpoint}')
    return response.text
def send(jsondata=None):
    request_header={
        'X-HTTP-Method-Override': 'GET'
    }
    if jsondata is None:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
            data["log"] = data["log"]
        jsondata = data
    response = requests.post('http://192.168.4.1/', json=jsondata,headers=request_header)
def execute(item):
    pass

#MAINLOOP
    #SETUP
print("FEEDBACK Mode Activated")
display = OLED_1inch3()
    #MAINLOOP
def mainloop():
    while True:
        display_splash(display,"App Store","v0.0.1")
        apps,code = get("/app/list").split(";,").split(":.")
        while True:
            if b0.value() == 0 and  b1.value() == 0:
                break
            elif b1.value() == 0:
                if bindex < len(apps):
                    bindex += 1
                else:
                    bindex = 0
                display_text(display,apps[bindex])
            elif b0.value() == 0:
                if bindex >= 0:
                    execute(code[bindex])
                    break
            else:
                utime.sleep(0.5)
    #CONNECTION
while True:
    display_clear_all(display)
    try:
        line = 1
        display_line1(display, "Connecting...")
        display.show()
        print("Connecting...")
        if connect() == False:
            print("Disconnected")
            display_disconnected(display,line)
            continue
        print("Connected")
        display_line1(display, "Connected")
        display.show()
        line,error = 2,"503"
        username = getaccount()
        if username == None:
            print("Getting Account")
            display_line2(display, "Getting Account")
            display.show()
            logged = get("/log").split("\n")[-10:]
            print(logged)
            for i in logged:
                if "Account '" in i and "' Created" in i:
                    username = i.split("'")[1]
            if username == None:
                print("Failed")
                error = "404"
                display_disconnected(display,line)
                continue
            else:
                with open("account.txt","w") as f:
                    f.write(username)
        else:
            print("Syncing Account")
            display_line2(display,"Syncing Account")
            display.show()
            send({"account":getaccount()})
        print(f"Account Synced (username: {username})")
        display_line2(display, "Account Synced")
        display.show()
        line,error = 3,"503"
        print("Fetching Stats")
        display_line3(display, "Fetching Stats")
        display.show()
        money = get(f"/account?v=0&u={username}").split("\n\n")[0]
        display_line3(display, "Stats Fetched")
        display.show()
        display_line4(display, "Booting...")
        display.show()
        utime.sleep(1)
        error = "500"
        display_splash(display,"Borealis","v1.2.1")
        display_splash(display,username,money)
        mainloop()
        continue
    except Exception as e:
        print(e)
        display_disconnected(display,line)
        continue