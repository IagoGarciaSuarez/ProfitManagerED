from datetime import datetime, timedelta
stats = """
------------------JOB STATS---------------------------
{}

-----------------MISSIONS STATS-----------------------
{}

"""

jobStats = """
    Job             ------- {job}
    Total profits   ------- {totalProfits}
    Profits/h:      ------- {hourProfits}
    Profit/30min:   ------- {halfHourProfits}
    Profit/Dock:    ------- {dockProfits}
"""

missionStats = """

    Missions Accepted ----- {missionsAccepted}
    Missions Completed  --- {missionsCompleted}
    Total Cr Rewards    --- {totalCrRewards}
    {reputationStats}
    {influenceStats}               
"""

repStats = """
    Rep '+' collected   --- {rep1rewards}
    Rep '++' collected  --- {rep2rewards}
    Rep '+++' collected --- {rep3rewards}
    Rep '++++' collected -- {rep4rewards}
    Rep '+++++' collected - {rep5rewards}
"""

infStats = """
    Inf '+' collected   --- {inf1rewards}
    Inf '++' collected  --- {inf2rewards}
    Inf '+++' collected --- {inf3rewards}
    Inf '++++' collected -- {inf4rewards}
    Inf '+++++' collected - {inf5rewards}
"""

class Player():
    jobs = {0: "Only missions", 1: "Trading", 2: "Mining", 3: "Exploring", 4: "Combat", 5: "Transport"}

    def __init__(self, job = 0, nCredits = 0):
        self._start_time = datetime.now() - timedelta(hours = 1)
        self._lastReadTime = self._start_time
        self._nCredits = nCredits
        self._job = job
        #Market stats
        self._totalMarketSell = 0
        self._totalMarketBuy = 0
        self._nSells = 0
        self._nBuys = 0
        #Mission stats
        self._totalMissionCrRewards = 0
        self._totalMissionCrCosts = 0
        self._nMissionsAccepted = 0
        self._nMissionsCompleted = 0
        self._nRepRewards = [0, 0, 0, 0, 0]
        self._nInfRewards = [0, 0, 0, 0, 0]


        self._nDocks = 0

    def getStart_time(self):
        return self._start_time

    def getLastRead(self):
        return self._lastReadTime

    def setLastRead(self):
        self._lastReadTime = self.getCurrent_time()
    
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
        return self.getTotalProfits()/2
    
    def getDocks(self):
        return self._nDocks

    def addDock(self):
        self._nDocks += 1

    def getDockProfits(self):
        if not self.getDocks() == 0:
            return self.getTotalProfits()/self.getDocks()
        return 0
    
    def getMissionsCompleted(self):
        return self._nMissionsCompleted

    def addMissionCompleted(self):
        self._nMissionsAccepted += 1

    def getMissionsAccepted(self):
        return self._nMissionsAccepted
    
    def addMissionAccepted(self):
        self._nMissionsAccepted += 1
    
    def addCrMissionReward(self, cr):
        self._totalMissionCrRewards += cr

    def getTotalCrMissionRewards(self):
        return self._totalMissionCrRewards

    def addRepReward(self, n):
        self._nRepRewards[n]+=1

    def getRepReward(self, n):
        return self._nRepRewards[n]

    def addInfReward(self, n):
        self._nInfRewards[n]+=1

    def getInfReward(self, n):
        return self._nInfRewards[n]

    def stats(self):
        if self.getJob() == 0:
            job_Stats = "No job selected"
        else:
            job_Stats = jobStats.format(job = self.getJob(),
            totalProfits = self.getTotalProfits(),
            hourProfits = self.getHourProfits(),
            halfHourProfits = self.getHalfHourProfits(),
            dockProfits = self.getDockProfits())

        for i in self._nRepRewards:
            if not self.getRepReward(i) == 0:
                rep_Stats = repStats.format(rep1rewards = self.getRepReward(0),
                rep2rewards = self.getRepReward(1),
                rep3rewards = self.getRepReward(2),
                rep4rewards = self.getRepReward(3),
                rep5rewards = self.getRepReward(4))
                break
            rep_Stats ="\n\tNo reputation changes."
        
        for i in self._nInfRewards:
            if not self.getInfReward(i) == 0:
                inf_Stats = infStats.format(inf1rewards = self.getInfReward(0),
                inf2rewards = self.getInfReward(1),
                inf3rewards = self.getInfReward(2),
                inf4rewards = self.getInfReward(3),
                inf5rewards = self.getInfReward(4))
                break
            inf_Stats = "\n\tNo influence changes."

        if self.getMissionsAccepted() == 0 and self.getMissionsCompleted() == 0:
            mission_Stats = "No missions accepted/completed."

        else:
            mission_Stats = missionStats.format(missionsAccepted = self.getMissionsAccepted(),
            missionsCompleted = self.getMissionsCompleted(),
            totalCrRewards = self.getTotalCrMissionRewards(),
            reputationStats = rep_Stats,
            influenceStats = inf_Stats)
        

        
        
        finalStats = stats.format(job_Stats, mission_Stats)

        return finalStats

    def user_to_json(self):
        pass