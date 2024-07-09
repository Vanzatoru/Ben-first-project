import operator

class sectorClass(object):
    def __init__(self):
        self.sectName = ""
        self.sectMarket = list()
        self.sectSysMarket = list()

    def assignSectors(self,sectorName,symbolsString,symbolList):
        self.sectName = sectorName
        for chars in range(0,len(symbolsString)):
            if symbolsString[2*chars:2*chars+2] in symbolList:
                self.sectMarket.append(symbolsString[2*chars:2*chars+2])

def defineSectorUniverse(sectorList,dataVendor,myComNameList,numSectors):
    for whichSect in range(0,numSectors):
        sectors = sectorClass()
        if dataVendor == "Pinnacle":
            if whichSect == 0 : sectors.assignSectors("Currency","BNSNANDXFNJNCN",myComNameList)
            if whichSect == 1 : sectors.assignSectors("Energies","ZUZHZNZB",myComNameList)
            if whichSect == 2 : sectors.assignSectors("Metals","ZGZIZKZPZA",myComNameList)
            if whichSect == 3 : sectors.assignSectors("Grains","ZSZWZCZLZMZR",myComNameList)
            if whichSect == 4 : sectors.assignSectors("Financials","USTYTUFBECES",myComNameList)
            if whichSect == 5 : sectors.assignSectors("Softs","SBKCCCCTLBJO",myComNameList)
            if whichSect == 6 : sectors.assignSectors("Meats","ZTZZZF",myComNameList)
        if dataVendor == "CSI":
            if whichSect == 0 : sectors.assignSectors("Currency","BPSFADDXECJYCD",myComNameList)
            if whichSect == 1 : sectors.assignSectors("Energies","CLHONGRB",myComNameList)
            if whichSect == 2 : sectors.assignSectors("Metals","GCSIHGPLPA",myComNameList)
            if whichSect == 3 : sectors.assignSectors("Grains","S_W_C_BOSMRR",myComNameList)
            if whichSect == 4 : sectors.assignSectors("Financials","USTYTUFVED",myComNameList)
            if whichSect == 5 :  sectors.assignSectors("Softs","SBKCCCCTLBOJ",myComNameList)
            if whichSect == 6 :sectors.assignSectors("Meats","LCLHFC",myComNameList)
        if dataVendor == "Quandl":
            if whichSect == 0 : sectors.assignSectors("Currency","BPSFADDXECJYCD",myComNameList)
            if whichSect == 1 : sectors.assignSectors("Energies","CLHONGRB",myComNameList)
            if whichSect == 2 : sectors.assignSectors("Metals","GCSIHGPLPA",myComNameList)
            if whichSect == 3 : sectors.assignSectors("Grains","S_W_C_BOSMRR",myComNameList)
            if whichSect == 4 : sectors.assignSectors("Financials","USTYTUFVED",myComNameList)
            if whichSect == 5 :  sectors.assignSectors("Softs","SBKCCCCTLBOJ",myComNameList)
            if whichSect == 6 :sectors.assignSectors("Meats","LCLHFC",myComNameList)
        sectorList.append(sectors)


    for i in range(0,len(sectorList)):
        if sectorList[i].sectMarket != []: print(sectorList[i].sectMarket)


def numPosCurrentSector(sectorList,curMarket,symbolList,positionList):
    for sector in range(0,len(sectorList)):
        whichSector = -1
        if curMarket in sectorList[sector].sectMarket:
            whichSector = sector
            break
    numSectorPos = 0
    if whichSector != -1:
        for sectorMarkets in range (0,len(sectorList[whichSector].sectMarket)):
            for symbols in range(0,len(symbolList)):
                tempMarket1 = sectorList[whichSector].sectMarket[sectorMarkets]
                tempMarket2 = symbolList[symbols]
                if tempMarket1 == tempMarket2:
                    if positionList != []:
                        curMktPos = symbols - len(symbolList)
                        if positionList[curMktPos] > 0:
                            numSectorPos +=1
    return(numSectorPos)

def getCurrentSector(curMarket,sectorList):
    for sector in range(0,len(sectorList)):
        whichSector = -1
        if curMarket in sectorList[sector].sectMarket:
            whichSector = sector
            break
    return(whichSector)

def parseSectors(sectorList,systemMarketList):
    masterDateList = list()
    pEquityTuple = list()
    combinedEquity = list()
    sectorPlotMonthRet = list()
    sectorPlotMonthDates = list()
    binBottom = list()
    sectorPlotBin = list()
    sectorPlotBinStrs = list()
    begDate = 99999999
    endDate = 0

    fileName1 = systemMarketList[0].systemName + "-Sectors.txt"
    target1 = open(fileName1,"w")
    print("Sector Analysis Report")
    lineOutPut = "Sector Analysis Report"
    target1.write(lineOutPut)
    target1.write("\n")

    for numSect in range(0,len(sectorList)):
        for numSysMarket in range(0,len(systemMarketList)):
            if systemMarketList[numSysMarket].symbol in sectorList[numSect].sectMarket:
#                    print(sectorList[numSect].sectName," ",systemMarketList[numSysMarket].symbol," ",systemMarketList[numSysMarket].profitLoss)
                 sectorList[numSect].sectSysMarket.append(systemMarketList[numSysMarket])
    for numSect in range(0,len(sectorList)):
        if sectorList[numSect].sectSysMarket != []:
            masterDateList[:] = []
            pEquityTuple[:] = []
            sectorPlotMonthRet[:] = []
            sectorPlotMonthDates[:] = []
            binBottom[:] = []
            sectorPlotBin[:] = []
            sectorPlotBinStrs[:] = []
            portPeakEquity = -999999999999
            portMinEquity = -999999999999
            portPeakEquity = -999999999999
            portMinEquity = -999999999999
            sectorPlotHH = -999999999999
            sectorPlotLL = 999999999999
            portMaxDD = 0
            print("################################################")
            lineOutPut = "################################################"
            target1.write(lineOutPut)
            target1.write("\n")
            lineOutPut = sectorList[numSect].sectName + "     ------------------------------------"
            target1.write('%-10s -------------------------------------\n' % sectorList[numSect].sectName)
       #     target1.write(lineOutPut)
       #     target1.write("\n")
            print('%-10s ' % (sectorList[numSect].sectName),"------------------------------------")
            for numSysMarket in range(0,len(sectorList[numSect].sectSysMarket)):
                print('%-8s %10.0f %10.0f ' % (sectorList[numSect].sectSysMarket[numSysMarket].symbol,sectorList[numSect].sectSysMarket[numSysMarket].profitLoss,
                sectorList[numSect].sectSysMarket[numSysMarket].maxxDD))
                target1.write('%-8s %10.0f %10.0f \n' % (sectorList[numSect].sectSysMarket[numSysMarket].symbol,sectorList[numSect].sectSysMarket[numSysMarket].profitLoss,
                sectorList[numSect].sectSysMarket[numSysMarket].maxxDD))
       #         lineOutPut = ""
       #         lineOutPut = sectorList[numSect].sectSysMarket[numSysMarket].symbol + "      " + str(round((sectorList[numSect].sectSysMarket[numSysMarket].profitLoss),2)) +  "  " +str(round((sectorList[numSect].sectSysMarket[numSysMarket].maxxDD),2))
       #         target1.write(lineOutPut)
       #         target1.write("\n")
                masterDateList += sectorList[numSect].sectSysMarket[numSysMarket].equity.equityDate
            masterDateList = removeDuplicates(masterDateList)
            masterDateList = sorted(masterDateList)
            lineOutPut = "------------------------------------------------"
            target1.write(lineOutPut)
            target1.write("\n")
            print("------------------------------------------------")
            priorIdxlist = list()
            priorIdxList = [0] * len(sectorList)
            plotYearsBack = 40000 #20211231 - 40000 = 20171231
            targetSectorBeginDate = masterDateList[-1] - plotYearsBack - masterDateList[-1] % 100 + 100
            for i in range(0,len(masterDateList)):
                cumuVal = 0
                for j in range(0,len(sectorList[numSect].sectSysMarket)):
                    skipDay = 0
                    try:
                        idx = sectorList[numSect].sectSysMarket[j].equity.equityDate.index(masterDateList[i])
                    except ValueError:
                        skipDay = 1
                        marketDayCumu = 0
                        skipDate = masterDateList[i]
                        skipMkt = sectorList[numSect].sectSysMarket[j].symbol
                        numDaysInEquityStream = len(sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal)
                        marketBeginDate = sectorList[numSect].sectSysMarket[j].equity.equityDate[0]
                        if (masterDateList[i] > marketBeginDate and i < numDaysInEquityStream):
                            marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[priorIdxList[j]]
                        else:
                            if masterDateList[i] < marketBeginDate:
                                marketDayCumu = 0
                            else:
                                marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[-1]
                        pEquityTuple += ((i,j,marketDayCumu),)
                        cumuVal += marketDayCumu
                    if skipDay == 0:
                        priorIdxList[j] = idx
                        marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[idx]
                        pEquityTuple += ((i,j,marketDayCumu),)
                        cumuVal += sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[idx]
                if masterDateList[i] > targetSectorBeginDate:
                    if masterDateList[i] % 100 < masterDateList[i-1] % 100:
                        sectorPlotMonthRet.append(prevCumuVal)
                        sectorPlotMonthDates.append(masterDateList[i-1])
                        sectorPlotHH = max(sectorPlotHH,prevCumuVal)
                        sectorPlotLL = min(sectorPlotLL,prevCumuVal)
                combinedEquity.append(cumuVal)
                prevCumuVal = cumuVal
                if cumuVal > portPeakEquity: portPeakEquity = cumuVal
                portMinEquity = max(portMinEquity,portPeakEquity - cumuVal)
                portMaxDD = portMinEquity
##            lineOutPut = "Totals: " + str(round(cumuVal,0)) + " " + str(round(portMaxDD,0))
##            target1.write(lineOutPut)
##            target1.write("\n")
##            target1.write("-------------------------------------------")
##            target1.write("\n")
            sectorYAxisBins = 20
            binIncrement = (sectorPlotHH - sectorPlotLL)/sectorYAxisBins
            binStartPoint = sectorPlotHH
            for i in range(sectorYAxisBins):
                binBottom.append(binStartPoint - binIncrement)
                binStartPoint -= binIncrement
            binBottom[sectorYAxisBins-1] = sectorPlotLL
            xAxisStr = ""
            prevSectorEquityYear = 0
            for k in range(len(sectorPlotMonthDates)):
                sectorEquityYear = int(sectorPlotMonthDates[k]/10000)
                if k > 0 and prevSectorEquityYear < sectorEquityYear:
                    xAxisStr = xAxisStr[0:len(xAxisStr)-3]
                    xAxisStr += str(sectorEquityYear)
                else:
                    xAxisStr += "-"
                if k == len(sectorPlotMonthDates) -1:
                    xAxisStr = xAxisStr[0:len(xAxisStr)-2]
                prevSectorEquityYear = sectorEquityYear
                for i in range(sectorYAxisBins):
                    val1 = binBottom[i]
                    val2 = binBottom[i] + binIncrement
                    binTop = binBottom[i] + binIncrement
                    if i == 0: binTop = binBottom[i] + binIncrement + 1
                    if sectorPlotMonthRet[k] >= binBottom[i] and sectorPlotMonthRet[k] < binTop:
                        sectorPlotBin.append(i)
            for i in range(sectorYAxisBins):
                binStr=""
                for k in range(len(sectorPlotMonthDates)):
                    if sectorPlotBin[k] == i:
                        binStr+="|"
                    else:
                        if i > 0 and sectorPlotBinStrs[i-1][k] != " ":
                            binStr +="|"
                        else:
                            binStr +=" "
                sectorPlotBinStrs.append(binStr)

            target1.write('%-8s %10.0f %10.0f \n' % ("Totals: ",cumuVal,portMaxDD))
            target1.write("------------------------------------------------\n")
            target1.write('%-10s Last 4 Years    ---------------------\n' % sectorList[numSect].sectName)
            print("Totals: ",'%10.0f %10.0f' % (cumuVal,portMaxDD))
            print("------------------------------------------------")
            print('%-10s ' % (sectorList[numSect].sectName),"Last 4 Years    --------------------")
            for i in range(sectorYAxisBins):
                if (i == 0 and binBottom[i] <= 0) or i > 0 and binBottom[i] <=0 and binBottom[i-1] >= 0:
                    target1.write("------------------------------------------------ 0\n")
                    print("------------------------------------------------ 0")
                target1.write(sectorPlotBinStrs[i])
                target1.write("\n")
                print(sectorPlotBinStrs[i])
            print(xAxisStr)
            target1.write(xAxisStr)
            target1.write("\n")

#            print("------------------------------------------------")


def sortRiskPerSector(myComNameList,sectorList,longRisk,shortRisk,maxPerSector,upOrDn):
    canBuyList = list()
    canShortList = list()
    sectMarketRisk = list()
    for cnt in range(0,len(myComNameList)):
        curSect = getCurrentSector(myComNameList[cnt],sectorList)
        sectMarketRisk.append((curSect,cnt,longRisk[cnt],shortRisk[cnt]))
        canBuyList.append(99999)
        canShortList.append(99999)

    sectMarketLongRisk = sectMarketRisk.copy()
    sectMarketShortRisk = sectMarketRisk.copy()
    sortOrder = False
    if upOrDn == -1: sortOrder = True
    sectMarketLongRisk.sort(key=operator.itemgetter(0,2),reverse = sortOrder)
    sectMarketShortRisk.sort(key=operator.itemgetter(0,3),reverse = sortOrder)
    for j in range(0,len(sectorList)):
        lsectCnt = 0
        for i in range(0,len(sectMarketLongRisk)):
            if sectMarketLongRisk[i][0] == j:
                print(sectMarketLongRisk[i][0]," ",sectMarketLongRisk[i][1]," ",int(sectMarketLongRisk[i][2]))
                if lsectCnt < maxPerSector:
                    canBuyList[i] = sectMarketLongRisk[i][1]
                lsectCnt += 1

        ssectCnt = 0
        for i in range(0,len(sectMarketShortRisk)):
            if sectMarketShortRisk[i][0] == j:
                if ssectCnt < maxPerSector:
                    canShortList[i] = sectMarketShortRisk[i][1]
                ssectCnt += 1
    return(canBuyList,canShortList)



def removeDuplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res


