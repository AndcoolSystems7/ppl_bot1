import donationalerts as daa
import logging
import asyncio
import numpy
import os
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

alert = daa.Alert("jCzYqIMrhfX1cn3GeK3B")

if not os.path.isfile("data/donations.npy"):
    donateList = [  ["ReZoort", "300", "1017884431"],
                    ["rorik", "50", "1418299420"], 
                    ["ModErator", "25", "1255297867"],
                    ]
    numpy.save(arr=numpy.array(donateList), file="data/donations.npy")
else: 
    donateList_npy = numpy.load("data/donations.npy")
    donateList = donateList_npy.tolist()
    
print(donateList)
async def test():
    while True:
        global alert
        alert = daa.Alert("jCzYqIMrhfX1cn3GeK3B")
        await asyncio.sleep(30)

@alert.event()
def new_donation(event):
    logging.info(event)
    global donateList
    finded = False
    if event.username != "AndcoolSystems":
        for x in range(len(donateList)):
            if event.username in donateList[x][0]:
                donateList[x][1] = int(event.amount_main) + int(donateList[x][1])
                try: donateList[x][2] = int(event.message.split(" ")[0])
                except: pass
                finded = True
        try: 
            if not finded: donateList.append([event.username, int(event.amount_main), int(event.message.split(" ")[0])])
        except: 
            if not finded: donateList.append([event.username, int(event.amount_main), -1])

        
        for x_s in range(len(donateList)):
            for x in range(len(donateList) - 1):
                if int(donateList[x][1]) < int(donateList[x + 1][1]):
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

if __name__ == '__main__':
    asyncio.run(test())