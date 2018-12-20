class Week_Day:
    def __init__(self, brother1, brother2, brother3):
        self.waiter1 = brother1;
        self.waiter2 = brother2;
        self.waiter3 = brother3;
    def isBrotherInDay(self, brother):
        return (brother == self.waiter1 or brother == self.waiter2 or brother == self.waiter3)
class Weekend_Day:
    def __init__(self, brother):
        self.waiter = brother;
    def isBrotherInDay(self, brother):
        return brother == self.brother;

class Week:
    def __init__(self, mon, tue, wed, thu, fri, sat, sun):
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun
    def isBrotherInWeek(self, brother):
        if self.mon.isBrotherInDay(brother):
            return True;
        if self.tue.isBrotherInDay(brother):
            return True;
        if self.wed.isBrotherInDay(brother):
            return True;
        if self.thu.isBrotherInDay(brother):
            return True;
        if self.fri.isBrotherInDay(brother):
            return True;
        if self.sat.isBrotherInDay(brother):
            return True;
        if self.sun.isBrotherInDay(brother):
            return True;
        return False;
class Calendar:
    def __init__(self, weeks):
        self.weeks = weeks;

