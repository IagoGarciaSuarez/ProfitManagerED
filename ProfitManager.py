import os
import time
from datetime import datetime, timedelta
import threading
import json
from player import Player

READING_RATE = 300

start = """
Welcome to ProfitManager.
To start a session, first select the job you will be doing.
1.  Trading
2.  Mining
3.  Exploring
4.  Combat
5.  Transport

You can change the job at anytime typing "job".
If you want to check every available command, type "?".
"""
help =  """
        e -> Close the program safely and print the recorded stats.
        s -> Start recording a session for the job you selected.
        ss -> Stop the current session safely and print the recorded stats.
        job -> Change the job [1: Trading, 2: Mining, 3: Exploring, 4: Combat, 5: Transport] 
               
"""

sessionOn = False

def Start():
        #Job selection
        while 1: 
                #try:
                job = input(start)
                if job == "e":
                        exit()
                if int(job) in Player.jobs:
                        statsOptions(int(job))
                        break
                #except Exception as e:
                #        print(str(e))
                #        exit()
        
        

def FindJournal():
        driveRoot = "C:\\"
        username = os.getlogin()
        journalName = "Journal." + time.strftime("%y%m%d", time.localtime())
        #journalPath = os.path.join(driveRoot, "Users", username, "Saved Games", "Frontier Developments", "Elite Dangerous")
        journalPath = os.path.join('/', "home", username, "Escritorio", "Mis Cosas", "Projects", "ProfitManagerED")
        journalFound = False
        for filename in os.listdir(journalPath):
                if journalName in filename and os.path.isfile(os.path.join(journalPath, filename)):
                        lastJournal = os.path.join(journalPath, filename)
                        journalFound = True

        if not journalFound:
                noGameOpenError()

        return lastJournal

def noGameOpenError():
        print("[ERROR]: You need to start a game in Elite Dangerous before attempting to start a session.\n")
        exit()

def readJournal(lastJournal, user, stopWaiting):
        global sessionOn
        sessionOn = True
        while sessionOn:
                for line in reversed(list(open(lastJournal, "r"))):
                        data = json.loads(line)
                        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        #                if timestamp < user.getStart_time():
        #                        break
        #                if data["event"] == "Shutdown":
        #                        noGameOpenError()

                        #Statistics calculation for Trading and Mining
                        if data["event"] == "MarketSell":
                                if user.getJob() in [1, 2]:
                                        user.addMarketSell(int(data['TotalSale']))
                        if data["event"] == "MarketBuy":
                                if user.getJob() in [1, 2]:
                                        user.addMarketBuy(int(data['TotalCost']))
                        if data["event"] == "Docked":
                                user.addDock()
                stopWaiting.wait(5)
                

def statsOptions(job):
        global sessionOn
        stopWaiting = threading.Event()
        
        while 1:        
                option = input()

                if option == "?":
                        print(help) 

                elif option == "s":
                        if sessionOn:
                                print("[ERROR] An active recording session already exists. Type \"e\" to stop the program safely, or \"ss\" to stop the session.\n")
                        else:
                                sessionOn = True
                                lastJournal = FindJournal()
                                print("[RECORDING] Type \"e\" to stop the program safely, or \"ss\" to stop the session.\n")
                                with open(lastJournal) as file:                        
                                        while 1:
                                                data = json.loads(file.readline())
                                                if data["event"] == "LoadGame":
                                                        user = Player(job, data["Credits"])

                                                if data["event"] == "Location":
                                                        break
                                        file.close()

                                readingThread = threading.Thread(target = readJournal, args =(lastJournal, user, stopWaiting))
                                readingThread.start()

                elif option == "ss" and sessionOn:
                        print("Session stopped. Write an option")
                        stopWaiting.set()
                        sessionOn = False
                        user.stats()

                elif option == "e":
                        if sessionOn:
                                stopWaiting.set()
                                sessionOn = False
                                user.stats()
                        exit()

Start()

