from brothers import Brother
from calendarGenerator import Week_Day, Weekend_Day, Week, Calendar
from openpyxl import load_workbook
import re
import constants

weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
otherDays = ["Friday", "Saturday", "Sunday"]

# generate list of assignable week time slots
def generateTimes():
    dutyTimes = [];
    time2IndDict = {}
    for day in weekDays:
        for i in range(1,4) :
            weekStr = day + " " + str(i)
            dutyTimes.append(weekStr)
            rowNum = weekDays.index(day) + constants.MON_ROW
            colNum = i + constants.W1_COL - 1
            time2IndDict[weekStr] = (colNum, rowNum)
    #add weekend time slots
    for day in otherDays:
        dutyTimes.append(day)
        colNum = constants.W1_COL
        rowNum = otherDays.index(day) + constants.FRI_ROW
        time2IndDict[day] = (colNum, rowNum)
    return (dutyTimes, time2IndDict)

def findLastRowNumber(sheet):
    n = 2   #first response since row 1 is header
    col = constants.NAME_COL
    while(sheet.cell(n,col).value is not None):
        n += 1
    return n

def generateBrothers(sheet):
    brothers = []
    firstRow = 2
    lastRow = findLastRowNumber(sheet)
    for i in range(firstRow,lastRow):
        name = sheet.cell(i,constants.NAME_COL).value
        isOnEB = sheet.cell(i, constants.EB_COL).value == "Yes"
        isOnRC = sheet.cell(i, constants.RC_COL).value == "Yes"
        dutiesDone = sheet.cell(i, constants.DUTY_COL).value
        times = [];
        timeCol = constants.TIME_COL

        for day in weekDays :
            for waiterNum in range(1,4):
                if sheet.cell(i, timeCol).value == "Yes" :
                    times.append(day + " " + str(waiterNum))
                timeCol += 1
        for day in otherDays :
            if sheet.cell(i, timeCol).value == "Yes":
                times.append(day)
            timeCol += 1
        bro = Brother(name, times, dutiesDone, isOnEB, isOnRC)
        brothers.insert(0,bro)
    return brothers

def generateWeek(sheet, dutyTimes, brothers, time2IndDict, RCFilter = False):
    #find people to fill in slots
    for time in dutyTimes:
        # finds best fit for time slot, schedule it in the sheet
        scheduleBestFit(sheet,time, brothers, time2IndDict, RCFilter)

def scheduleBestFit(sheet, time, brothers, time2IndDict, RCFilter):
    #find available brothers
    availbros = []
    for bro in brothers:
        if (time in bro.availableTimes):
            availbros.append(bro);
    #sort for brothers with least WD done
    availbros.sort()
    #if set, ignore all brothers with the attribute "on RC"
    if RCFilter:
        for bro in availbros :
            if bro.isOnRC:
                availbros.remove(bro)
        if(availbros[0].isOnRC):
            availbros.remove(availbros[0])

    #add the brother to the calendar sheet
    if availbros.__len__() > 0:
        availbros[0].dutiesDone += 1
        row, col = time2IndDict[time]
        c = sheet.cell(col, row, value=availbros[0].name)
    else :
        print("no one available for time: ", time)

def updateDutiesDone(sheet, Brothers):
    row = findLastRowNumber(sheet) - 1
    col = constants.DUTY_COL
    for bro in Brothers:
        c = sheet.cell(row,col, value=bro.dutiesDone)
        row -= 1

calendar = Calendar([]);
filePath = constants.FILE_PATH
#parse form responses
wb = load_workbook(filePath)
timeSheet = wb['Time Sheet']
cmdSheet = wb['Master Sheet']
dutyTimes, dict = generateTimes()
Brothers = generateBrothers(timeSheet)



sheetName = cmdSheet.cell(1,2).value
isRCWeek = cmdSheet.cell(2,2).value != "No"
if(sheetName in wb.sheetnames):
    print("already have sheet generated, ignoring command")

else:
    source = wb['Blank Week']
    wsTest = wb.copy_worksheet(source)
    wsTest.title = sheetName
    # generate a copy of master sheet
    #wsCopy = wb.copy_worksheet(wb['Master Sheet'])
    #wsCopy.title = "Copy before " + sheetName

    generateWeek(wsTest, dutyTimes, Brothers, dict, isRCWeek)
    updateDutiesDone(timeSheet, Brothers)
    wb.save(filePath)

