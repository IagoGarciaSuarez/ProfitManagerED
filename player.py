from datetime import datetime, timedelta
stats = """
        Job             ------- {job}
        Total profits   ------- {totalProfits}
        Profits/h:      ------- {hourProfits}
        Profit/30min:   ------- {halfHourProfits}
        Profit/Dock:    ------- {dockProfits}
               
"""

class Player():
    jobs = {1: "Trading", 2: "Mining", 3: "Exploring", 4: "Combat", 5: "Transport"}

    def __init__(self, job = 0, nCredits = 0):
        self._start_time = datetime.now() - timedelta(hours = 1)
        self._nCredits = nCredits
        self._job = job
        #Market stats
        self._totalMarketSell = 0
        self._totalMarketBuy = 0
        self._nSells = 0
        self._nBuys = 0
        #Mission stats
        self._totalMissionRewards = 0
        self._totalMissionCosts = 0
        self._nMissionsAccepted = 0
        self._nMissionsCompleted = 0

        self._nDocks = 0

    def getStart_time(self):
        return self._start_time
    
    def getCurrent_time(self):
        return datetime.now() - timedelta(hours = 1)

    def getJob(self):
        return self._job

    def addMarketSell(self, marketSellCr):
        self._nSells += 1
        self._totalMarketSell += marketSellCr

    def addMarketBuy(self, marketBuyCr):
        self._nBuys += 1
        self._totalMarketBuy += marketBuyCr

    def getTotalProfits(self):
        totalProfits = (self._totalMarketSell - self._totalMarketBuy)
        return totalProfits

    def getHourProfits(self):
        difference = self.getCurrent_time()-self.getStart_time()
        return self.getTotalProfits()/(difference.total_seconds()/3600)

    def getHalfHourProfits(self):
        return self.getHourProfits()/2

    def getProfitsHalf(self):
        return self._totalProfits/2
    
    def getDocks(self):
        return self._nDocks

    def addDock(self):
        self._nDocks += 1

    def getDockProfits(self):
        return self.getTotalProfits()/self.getDocks()

    def stats(self):
        print(stats.format(job = self.jobs[self._job], 
        totalProfits = format(self.getTotalProfits(), ","),
        hourProfits = format(int(self.getHourProfits()), ","), 
        halfHourProfits = format(int(self.getHalfHourProfits()), ","), 
        dockProfits = format(int(self.getDockProfits()), ",")))