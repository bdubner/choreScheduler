class Brother:
    def __init__(self, name, times, dutiesDone, isOnEB, isOnRC):
        self.availableTimes = times;
        self.name = name;
        self.dutiesDone = dutiesDone;
        self.isOnEB = isOnEB;
        self.isOnRC = isOnRC;
    def __lt__(self, other):
        selfDone = self.dutiesDone
        otherDone = other.dutiesDone
        if(selfDone is None):
            selfDone = 0;
        if(otherDone is None):
            otherDone = 0;
        if(self.isOnEB) : selfDone = selfDone * 2
        if (other.isOnEB): otherDone = otherDone * 2
        return selfDone < otherDone