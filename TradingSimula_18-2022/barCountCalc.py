def barCountCalc(masterDateList,startDate,stopDate,rampUp):

    barCount= 0;endBarCount = 0
    lenOfData = len(masterDateList)
    if startDate < masterDateList[0] or startDate >= masterDateList[-1]:
        print("Bad Start Date ",startDate," needs YYYYMMDD defaulting to good Start Date: ",masterDateList[int(lenOfData/2)])
        startDate = masterDateList[int(lenOfData/2)]
        answer = input("Bad Start Date please input YYYYMMDD format")
        if answer != "":
            newStartDate = int(answer)
            if newStartDate > masterDateList[0] and newStartDate <= masterDateList[-100]:
                startDate =  newStartDate
    while (barCount<len(masterDateList) and masterDateList[barCount]) <= startDate:
        barCount +=1
 #   barCount -=1
    if barCount < rampUp:
        while barCount <= rampUp:
            barCount +=1
    endBarCount = barCount + 1
    maxNumBars = len(masterDateList)
    while masterDateList[endBarCount] <= stopDate and endBarCount < maxNumBars-1:
        endBarCount +=1
    #endBarCount -=1
    return(barCount,endBarCount)
