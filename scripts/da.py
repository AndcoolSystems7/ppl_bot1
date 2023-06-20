import donationalerts as da
import logging
import asyncio
import numpy
import os
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

alert = da.Alert("jCzYqIMrhfX1cn3GeK3B")

if not os.path.isfile("data/donations.npy"):
    donateList = [["rorik", 50]]
    numpy.save(arr=numpy.array(donateList), file="data/donations.npy")
else: 
    donateList_npy = numpy.load("data/donations.npy")
    donateList = donateList_npy.tolist()
    
print(donateList)
async def test():
    while True:
        global alert
        alert = da.Alert("jCzYqIMrhfX1cn3GeK3B")
        await asyncio.sleep(30)

@alert.event()
def new_donation(event):
    global donateList
    finded = False
    for x in range(len(donateList)):
        if event.username in donateList[x][0]:
            donateList[x][1] = int(event.amount_main) + int(donateList[x][1])
            finded = True

    if not finded: donateList.append([event.username, int(event.amount_main)])


    for x_s in range(len(donateList)):
        for x in range(len(donateList) - 1):
            if int(donateList[x][1]) < int(donateList[x + 1][1]):
                topid = donateList[x][0]
                topsc = donateList[x][1]

                donateList[x][1] = donateList[x + 1][1]
                donateList[x][0] = donateList[x + 1][0]

                donateList[x + 1][1] = topsc
                donateList[x + 1][0] = topid
    numpy.save(arr=numpy.array(donateList), file="data/donations.npy")



    print(donateList)

if __name__ == '__main__':
    asyncio.run(test())