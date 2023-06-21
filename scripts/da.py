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
    donateList = []
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


@alert.event()
def new_donation(event):
    global donateList
    global alerting_id
    finded = False
    id = -1
    idd = -1
    if event.message != None: 
        try: id = int(event.message.split(" ")[0])
        except:pass
    if True:#if event.username != "AndcoolSystems":
        for x in range(len(donateList)):
            if event.username == donateList[x][0]:
                
                id = int(donateList[x][2])
                try: 
                    if event.additional_data['is_commission_covered'] == 1:
                        add = (float(event.amount_main) / 100) * 11.12
                except: add = 0

                donateList[x][1] = float(event.amount_main) + float(donateList[x][1]) + add
                try: donateList[x][2] = int(event.message.split(" ")[0])
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

    print(donateList)
    global da_event
    if id != -1:
        if da_event == -1: da_event = [[float(event.amount_main), int(id)]]
        else:
            da_event.append([float(event.amount_main), int(id)])
def get_list():
    global donateList
    return donateList 

def get_event():
    global da_event
    return da_event

def reset_event():
    global da_event
    da_event = -1