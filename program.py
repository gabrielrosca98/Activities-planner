import requests
import time
import xml.etree.ElementTree as ET
import uuid
header = {'Content-Type' : "application/xml", 'Accept' : "application/xml"}
finSlot = 0
def finalReservationMake():
    availableSlotsHotel = freeRes(3010)
    availableSlotsBand  = freeRes(3020)
    slotToReserve = min(set(availableSlotsHotel).intersection(set(availableSlotsBand)))
    resp = makeRes(slotToReserve, 3010)
    if "200" not in resp:
        return False
    else:
        resp = makeRes(slotToReserve, 3020)
        if "200" not in resp:
            cancelRes(slotToReserve, 3010)
            return False
        else:
            finSlot = slotToReserve
            return True
    return False

def makeRes(slotToReserve, option):
    uniqueId = uuid.uuid1()
    fileReserve = open("makeReservation.xml").read()
    tree = ET.parse('makeReservation.xml')
    root = tree.getroot()
    userName = root.find('username').text
    passwordString = root.find('password').text
    req_id = root.find('request_id')
    req_id.text = str(uniqueId)
    root.find('slot_id').text = str(slotToReserve)
    tree.write('makeReservation.xml')
    urlOption = "http://jewel.cs.man.ac.uk:" + str(option) + "/queue/enqueue"
    fileReserve = open("makeReservation.xml").read()
    requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    while requestMessage.text == 'Service Unavailable' or requestMessage.text == 'Message Unavailable':
        time.sleep(1)
        print "Loading"
        requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    print requestMessage
    urlText = requestMessage.text[9:len(requestMessage.text) - 10] + "?username=" + userName + "&password=" + passwordString
    print urlText
    time.sleep(50)
    response = requests.get(urlText)
    while response.text == 'Service unavailable' or response.text == 'Message unavailable':
        time.sleep(1)
        print "Loading"
        response = requests.get(urlText)
    print response
    print response.text
    return response.text
    #[response.text.find("<reserve>") + 9:response.text.find("</reserve>")]

def cancelRes(slotToCancel, option):
    uniqueId = uuid.uuid1()
    fileReserve = open("cancelReservation.xml").read()
    tree = ET.parse('cancelReservation.xml')
    root = tree.getroot()
    userName = root.find('username').text
    passwordString = root.find('password').text
    req_id = root.find('request_id')
    req_id.text = str(uniqueId)
    root.find('slot_id').text = str(slotToCancel)
    tree.write('cancelReservation.xml')
    #print root.find('slot_id').text
    urlOption = "http://jewel.cs.man.ac.uk:" + str(option) + "/queue/enqueue"
    fileReserve = open("cancelReservation.xml").read()
    requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    while requestMessage.text == 'Service Unavailable' or requestMessage.text == 'Message Unavailable':
        time.sleep(1)
        print "Loading"
        requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    print requestMessage
    urlText = requestMessage.text[9:len(requestMessage.text) - 10] + "?username=" + userName + "&password=" + passwordString
    print urlText
    time.sleep(100)
    response = requests.get(urlText)
    while response.text == 'Service unavailable' or response.text == 'Message unavailable':
        time.sleep(1)
        print "Loading"
        response = requests.get(urlText)
    print response
    print response.text
    return response.text
    #[response.text.find("<cancel>") + 8:response.text.find("</cancel>")]

def myReserv(option):
    uniqueId = uuid.uuid1()
    fileReserve = open("myReservation.xml").read()
    tree = ET.parse('myReservation.xml')
    root = tree.getroot()
    userName = root.find('username').text
    passwordString = root.find('password').text
    req_id = root.find('request_id')
    req_id.text = str(uniqueId)
    tree.write('myReservation.xml')
    urlOption = "http://jewel.cs.man.ac.uk:" + str(option) + "/queue/enqueue"
    fileReserve = open("myReservation.xml").read()
    requestMessage = requests.put(str(urlOption), data = fileReserve, headers = header)
    while requestMessage.text == 'Service Unavailable' or requestMessage.text == 'Message Unavailable':
        time.sleep(1)
        print "Loading"
        requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    print requestMessage
    urlText = requestMessage.text[9:len(requestMessage.text) - 10] + "?username=" + userName + "&password=" + passwordString
    print urlText
    time.sleep(20)
    response = requests.get(urlText)
    while response.text == 'Service unavailable' or response.text == 'Message unavailable':
        time.sleep(1)
        print "Loading"
        response = requests.get(urlText)
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    myReservedSlots = []
    for child in root.iter('slot_id'):
        myReservedSlots.append(int(child.text))
    return myReservedSlots

def freeRes(option):
    uniqueId = uuid.uuid1()
    fileReserve = open("checkReservation.xml").read()
    tree = ET.parse('checkReservation.xml')
    root = tree.getroot()
    userName = root.find('username').text
    passwordString = root.find('password').text
    req_id = root.find('request_id')
    req_id.text = str(uniqueId)
    tree.write('checkReservation.xml')
    urlOption = "http://jewel.cs.man.ac.uk:" + str(option) + "/queue/enqueue"
    fileReserve = open("checkReservation.xml").read()
    requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    while requestMessage.text == 'Service Unavailable' or requestMessage.text == 'Message Unavailable':
        time.sleep(1)
        print "Loading"
        requestMessage = requests.put(urlOption, data = fileReserve, headers = header)
    print requestMessage
    urlText = requestMessage.text[9:len(requestMessage.text) - 10] + "?username=" + userName + "&password=" + passwordString
    time.sleep(1)
    response = requests.get(urlText)
    while response.text == 'Service unavailable' or response.text == 'Message unavailable':
        time.sleep(1)
        print "Loading"
        response = requests.get(urlText)
    print urlText
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    availableSlots = []
    for child in root.iter('slot_id'):
        availableSlots.append(int(child.text))
    return availableSlots

slotsBookeHotel = myReserv(3010)
slotsBookeBand = myReserv(3020)
for indexBook in range(0, len(slotsBookeBand)):
    cancelRes(slotsBookeBand[indexBook], 3020)
for indexBook in range(0, len(slotsBookeHotel)):
    cancelRes(slotsBookeHotel[indexBook], 3010)
while finalReservationMake() == False:
    print "Trying"
freeSlot1 = freeRes(3010)
freeSlot2 = freeRes(3020)
checkNewSlot = min(set(freeSlot1).intersection(set(freeSlot2)))
if checkNewSlot < finSlot:
    resp = makeRes(checkNewSlot, 3010)
    if "200" not in resp:
        print "Failed first slot(3010)"
    else:
        resp = makeRes(checkNewSlot, 3020)
        if "200" not in resp:
            cancelRes(checkNewSlot, 3010)
            print "Failed second slot(3020) "
        else:
            cancelRes(finSlot, 3010)
            cancelRes(finSlot, 3020)
            print "Reserved new slot " + str(checkNewSlot)
