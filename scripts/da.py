import donationalerts as daa
import logging
import asyncio
import numpy
import os
from io import BytesIO
from PIL import Image
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

alert = daa.Alert("jCzYqIMrhfX1cn3GeK3B")
alerting_id = -1
if not os.path.isfile("data/donations.npy"):
    donateList = [["ReZoort", 501.0, 1017884431],
                  ["veel1en", 400.99, 1084649863],
                  ["rorik", 350.0, 1418299420],
                  ["ModErator5937", 275.0, 1255297867],
                  ["Гамдав", 50.0, 995824148]]
    numpy.save(arr=numpy.array(donateList), file="data/donations.npy")
else: 
    donateList_npy = numpy.load("data/donations.npy")
    donateList = donateList_npy.tolist()
    for x_s in range(len(donateList)):
        for x in range(len(donateList) - 1):
            if float(donateList[x][1]) < float(donateList[x + 1][1]):
                topid = donateList[x][0]
                topsc = donateList[x][1]
                topidd = donateList[x][2]

                donateList[x][2] = donateList[x + 1][2]
                donateList[x][1] = donateList[x + 1][1]
                donateList[x][0] = donateList[x + 1][0]

                donateList[x + 1][2] = topidd
                donateList[x + 1][1] = topsc
                donateList[x + 1][0] = topid
bot = None


def init(bot1, dp1):
    global bot
    global dp
    bot = bot1
    dp = dp1

print(donateList)

da_event = -1

def sortir(donateList):
    for x_s in range(len(donateList)):
        for x in range(len(donateList) - 1):
            if float(donateList[x][1]) < float(donateList[x + 1][1]):
                topid = donateList[x][0]
                topsc = donateList[x][1]
                topidd = donateList[x][2]

                donateList[x][2] = donateList[x + 1][2]
                donateList[x][1] = donateList[x + 1][1]
                donateList[x][0] = donateList[x + 1][0]

                donateList[x + 1][2] = topidd
                donateList[x + 1][1] = topsc
                donateList[x + 1][0] = topid
    return donateList

@alert.event()
def new_donation(event):

    global donateList
    global alerting_id
    finded = False
    id = -1
    idd = -1
    username = event.username
    last_balance = 0
    balance_now = 0
    if event.message != None: 
        try: id = int(event.message.split(" ")[0])
        except:pass
    if True: #if event.username != "AndcoolSystems":
        for x in range(len(donateList)):
            if event.username == donateList[x][0]:
                last_balance = float(donateList[x][1])
                id = int(donateList[x][2])
                try: 
                    if event.additional_data['is_commission_covered'] == 1:
                        add = (float(event.amount_main) / 100) * 11.12
                    else: add = 0
                except: add = 0

                donateList[x][1] = float(event.amount_main) + float(donateList[x][1]) + add
                try: 
                    if int(donateList[x][2]) == -1: donateList[x][2] = int(event.message.split(" ")[0])
                except: pass
                finded = True
                idd = x
        to_pop = []
        if idd != -1 and donateList[idd][2] != -1:
            for x in range(len(donateList)):
                if int(donateList[x][2]) == int(donateList[idd][2]) and x != idd:
                    donateList[idd][1] = float(donateList[idd][1]) + float(donateList[x][1])
                    
                    to_pop.append(x)
                    #print(x)
            pop_c = 0
            for x_pop in to_pop:
                donateList.pop(x_pop - pop_c)
                pop_c += 1
        
        try: 
            if not finded: donateList.append([event.username, float(event.amount_main), int(event.message.split(" ")[0])])
        except: 
            if not finded: donateList.append([event.username, float(event.amount_main), -1])

        balance_now = float(donateList[idd][1])
        for x_s in range(len(donateList)):
            for x in range(len(donateList) - 1):
                if float(donateList[x][1]) < float(donateList[x + 1][1]):
                    topid = donateList[x][0]
                    topsc = donateList[x][1]
                    topidd = donateList[x][2]

                    donateList[x][2] = donateList[x + 1][2]
                    donateList[x][1] = donateList[x + 1][1]
                    donateList[x][0] = donateList[x + 1][0]

                    donateList[x + 1][2] = topidd
                    donateList[x + 1][1] = topsc
                    donateList[x + 1][0] = topid

        numpy.save(arr=numpy.array(donateList), file="data/donations.npy")


    global da_event
    if id != -1:
        if da_event == -1: da_event = [[float(event.amount_main), int(id), username, last_balance, balance_now]]
        else:
            da_event.append([float(event.amount_main), int(id), username, last_balance, balance_now])


def get_list():
    global donateList
    return donateList 

def set_list(donateList1):
    global donateList
    donateList = donateList1
    numpy.save(arr=numpy.array(donateList), file="data/donations.npy")
def get_event():
    global da_event
    return da_event

def reset_event():
    global da_event
    da_event = -1