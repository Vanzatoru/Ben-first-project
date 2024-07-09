#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'PythonTurtFunc_1R' #System Name here
initCapital = 1000000
commission = 0
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = True
useLagerre       = False
useParabolic     = False
useStochastic    = False
useRSI           = False
useMACD          = False
useDominantCycle = False

from IncludeCode import includeImports,includeCodeDict,includeCode_A,includeCode_B
from IncludeCode import includeCode_C,includeCode_D,includeCode_E
from IncludeCode import includeCode_Last1,includeCode_Last2,includeCode_Last3
from IncludeCode import includeCode_Last4
from ltlClass import ltlClass

exec(includeImports)
exec(includeCodeDict)
#-------------------------------------------------------------------------------------------------
marketList = getData(isStock=False) # loads data from .csv or .por file and sets attributes
#-------------------------------------------------------------------------------------------------

exec(includeCode_A)
exec(includeCode_B)


#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

useLTLFilter = True
use2NasLoss = True
maxUnits = 999999
totalUnits = 0


longExit2 = shortExit2 = 0;
long2NLoss = short2NLoss = 0

theoMP = list()
theoEP = list()
theoWL = list()
NValue = list()
ltl = False
ltlList = list()

canTrade = True


curTradesList = list() #user defined list
for curMarket in range(0,numMarkets):
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLagerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
    theoWL.append(-1)
    theoMP.append(0)
    theoEP.append(0)
    NValue.append(-999999)
    marketVal4.append(1)
    ltlList.append(ltlClass()) #instantiating a list of ltlClass (lastTradeLoser)

#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary - predfined for Pinnalce and CSI data
#---------------------------------------------------------------------------------
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Quandl",myComNameList,numSectors)
#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
exec(includeCode_C)
def longEntrySys1(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    print("****  ",(mp < 0 and buyLevel < ltlBenchMark))
    if ((mp < 0 and buyLevel < ltlBenchMark) or mp == 0 or (theoMP == -1 and buyLevel >= ltlBenchMark)) and \
    myHigh[curBar] >= buyLevel and mp < 1 and \
    theoWL == -1 and canTrade and totalUnits < maxUnits:
        price = max(myOpen[curBar],buyLevel)
        marketVal4[curMarket] = 1
        marketVal3[curMarket] = price
        marketVal1[curMarket] = NValue[curMarket]
        tradeName = "TurtSys1:B"
        long2NLoss = roundToNearestTick(price - 2 * NValue[curMarket],-1,myMinMove)
        marketVal2[curMarket] = long2NLoss
        totalUnits +=1
        enterLongPosition(price,posSize,tradeName,sysMarkDict)
#       unPackDict(sysMarkDict)
        execution = 1
        return execution

def longAddOn(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if myHigh[curBar] >= longAddOnPrice and mp >= 1 and marketVal4[curMarket] < 4 and canTrade and totalUnits < maxUnits :
        price = max(myOpen[curBar],longAddOnPrice)
        tradeName = "TurtAdd:B"+str(marketVal4[curMarket])
        marketVal4[curMarket] += 1
        long2NLoss = roundToNearestTick(price - 2 * marketVal1[curMarket],-1,myMinMove)
        marketVal2[curMarket] = long2NLoss
        totalUnits +=1
        enterLongPosition(price,posSize,tradeName,sysMarkDict)
        execution = 1
        return execution
def longEntrySys2(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if myHigh[curBar] >= buyLevel2 and mp < 1 and canTrade and totalUnits < maxUnits :
        price =max(myOpen[curBar],buyLevel2)
        tradeName = "TurtSys2:B"
        marketVal1[curMarket] = NValue[curMarket]
        marketVal3[curMarket] = price
        marketVal4[curMarket] = 1
        long2NLoss = price - 2 * marketVal1[curMarket]
        long2NLoss = roundToNearestTick(long2NLoss,1,myMinMove)
        marketVal2[curMarket] = long2NLoss
        totalUnits +=1
        enterLongPosition(price,posSize,tradeName,sysMarkDict)
        execution = 1
        return execution


def longExitSys1(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if mp >= 1 and myLow[curBar] <= longExit and longExit > shortLevel and \
    longEntryName == "TurtSys1:B" and barsSinceEntry > 1:
        price = min(myOpen[curBar],longExit)
        tradeName = "TurtSys1-Lx"
        numShares = curShares
        totalUnits -= numShares
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution


def longExitSys2(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
#    print(myDate[curBar]," ",longEntryName," ",longExit2," ",long2NLoss)
    if mp >= 1 and myLow[curBar] <= longExit2 and longExit2 > long2NLoss and \
    longEntryName == "TurtSys2:B" and barsSinceEntry > 1:
        price = min(myOpen[curBar],longExit2)
        tradeName = "TurtSys2:Lx"
        marketVal4[curMarket] = 0
        numShares = curShares
        totalUnits -= numShares
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution

def long2NExit(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if mp >= 1 and myLow[curBar] <= long2NLoss and barsSinceEntry > 1:
        price = min(myOpen[curBar],long2NLoss)
        tradeName = "Turt2N:Lx"
        marketVal4[curMarket] = 0
        numShares = curShares
        totalUnits -= numShares
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution


def shortEntrySys1(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if ((mp >-1 and shortLevel > ltlBenchMark) or mp == 0 or (theoMP == 1 and shortLevel <= ltlBenchMark)) and \
    myLow[curBar] <= shortLevel and mp >-1 and \
    theoWL == -1 and canTrade and totalUnits < maxUnits:
        price = min(myOpen[curBar],shortLevel)
        tradeName = "TurtSys1:S"
        marketVal4[curMarket] = 1
        marketVal1[curMarket] = NValue[curMarket]
        marketVal3[curMarket] = price
        numShares = posSize
        short2NLoss = price + 2 * NValue[curMarket]
        short2NLoss = roundToNearestTick(short2NLoss,1,myMinMove)
        marketVal2[curMarket] = short2NLoss
        totalUnits +=1
        enterShortPosition(price,posSize,tradeName,sysMarkDict)
        execution = 1
        return execution


def shortAddOn(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if myLow[curBar] <= shortAddOnPrice and mp <=-1 and marketVal4[curMarket] < 4 and canTrade and totalUnits < maxUnits:
        price = min(myOpen[curBar],shortAddOnPrice)
        tradeName = "TurtAdd:S"
        marketVal4[curMarket] += 1
        numShares = posSize
        short2NLoss = price + 2 * marketVal1[curMarket]
        short2NLoss = roundToNearestTick(short2NLoss,1,myMinMove)
        marketVal2[curMarket] = short2NLoss
        totalUnits +=1
        enterShortPosition(price,posSize,tradeName,sysMarkDict)
        execution = 1
        return execution


def shortEntrySys2(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if myLow[curBar] <= shortLevel2 and mp >-1 and canTrade and totalUnits < maxUnits:
        price = min(myOpen[curBar],shortLevel2)
        tradeName = "TurtSys2:S"
        marketVal1[curMarket] = NValue[curMarket]
        marketVal3[curMarket] = price
        marketVal4[curMarket] = 1
        numShares = posSize
        short2NLoss = price + 2 * NValue[curMarket]
        short2NLoss = roundToNearestTick(short2NLoss,1,myMinMove)
        marketVal2[curMarket] = short2NLoss
        totalUnits +=1
        enterShortPosition(price,posSize,tradeName,sysMarkDict)
        execution = 1
        return execution


def shortExitSys1(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if mp <= -1 and myHigh[curBar] >= shortExit and shortEntryName == "TurtSys1:S" and barsSinceEntry > 1:
        price = max(myOpen[curBar],shortExit)
        tradeName = "TurtSys1:Sx"
        numShares = curShares
        totalUnits -= numShares
        marketVal4[curMarket] = 0
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution


def shortExitSys2(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if mp <= -1 and myHigh[curBar] >= shortExit2 and shortExit2 < short2NLoss and \
    shortEntryName == "TurtSys2:S" and barsSinceEntry > 1:
        price = max(myOpen[curBar],shortExit2)
        tradeName = "TurtSys2:Sx"
        marketVal4[curMarket] = 0
        numShares = curShares
        totalUnits -= numShares
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution

def short2NExit(sysMarkDict):
    global barsSinceEntry,barsSinceExit,curShares,todaysCTE,totalUnits
    execution = 0
    if mp <= -1 and myHigh[curBar] >= short2NLoss and barsSinceEntry > 1:
        price = max(myOpen[curBar],short2NLoss)
        tradeName = "Turt2N:Sx"
        marketVal4[curMarket] = 0
        numShares = curShares
        totalUnits -= numShares
        exitPosition(price, curShares, tradeName, sysMarkDict)
        execution = 1
        return execution


for curPortBar in range(barCount,endBarCount+1):
    portManager.portDate.append(masterDateList[curPortBar])
    if curPortBar % 225 == 0 : print("Working on bar #: ",curPortBar)
    for curMarket in range(0,numMarkets):
        exec(includeCode_D)
    #---------------------------------------------------------------------------------------------------
    #  Assign lists based on marketMonitor here - assigning temp lists here is great idea
    #--------------------------------------------------------------------------------------------------
        curTradesList = marketMonitorList[curMarket].tradesList
        curMarketData = marketMonitorList[curMarket].marketData
    #---------------------------------------------------------------------------------
    # Do not change code below
    #---------------------------------------------------------------------------------

        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            exec(includeCode_E)
#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

            longEntryName = ""
            shortEntryName = ""

            if mp >= 1: longEntryName = curTradesList[-abs(mp)].tradeName
            if mp <=-1: shortEntryName = curTradesList[-abs(mp)].tradeName
            if firstMarketLoop == False and curMarket == 0:
                totalUnits = 0
                for myCom in range(0,numMarkets):
                    if len(marketMonitorList[myCom].mp)!=0:
                        totalUnits += abs(marketMonitorList[myCom].mp[-1])
                if totalUnits >= maxUnits:
                    canTrade = False
                else:
                    canTrade = True

# Calculate N - first simple average - 2nd and beyond use weighting calculation
            if NValue[curMarket] == -999999:
                NValue[curMarket] = sAverage(myTrueRange,20,curBar,1)
            else:
                NValue[curMarket] = (19 * NValue[curMarket] + myTrueRange[curBar-1])/20
            unitSize = (0.01*(initCapital + dailyPortCombEqu))/(NValue[curMarket]*myBPV)
            unitSize = trunc(unitSize)
# System #1 entry levels
            buyLevel= highest(myHigh,20,curBar,2) + myMinMove
            shortLevel = lowest(myLow,20,curBar,2) - myMinMove
# System #2 entry Levels
            buyLevel2= highest(myHigh,55,curBar,2) + myMinMove
            shortLevel2 = lowest(myLow,55,curBar,2) - myMinMove
# System #1 exit levels
            shortExit = highest(myHigh,10,curBar,2) + myMinMove
            longExit =  lowest(myLow,10,curBar,2) - myMinMove
# System #2 exit levels
            shortExit2 = highest(myHigh,20,curBar,2) + myMinMove
            longExit2 =  lowest(myLow,20,curBar,2) - myMinMove

            if mp >= 1 :
                long2NLoss = marketVal2[curMarket]
            if mp <= -1 :
                short2NLoss = marketVal2[curMarket]

            posSize = 1 * unitSize
            posSize = 1

            stopAmt = 2*NValue[curMarket]

            ltl=ltlList[curMarket].lastTradeLoser(myOpen,myHigh,myLow,curBar, \
            buyLevel,shortLevel,False,stopAmt,stopAmt,True,\
            longExit,shortExit,not(use2NasLoss))
#            ltl=ltlList[curMarket].lastTradeLoser(myOpen,myHigh,myLow,curBar, \
#            buyLevel,shortLevel,False,stopAmt,stopAmt,True,longExit,shortExit,not(use2NasLoss

            ltlBenchMark = ltlList[curMarket].ltlBenchMark
            theoMP = ltlList[curMarket].theoMP
            theoEP = ltlList[curMarket].theoEP
            theoEX = ltlList[curMarket].theoEX
            print(myDate[curBar]," TheoPOS is ",theoMP," at ",theoEP," exit ",theoEX," loser ?",ltl)
            if ltl:
                theoWL = -1
            else:
                theoWL = 1

            if not(useLTLFilter):
                theoWL = -1
                if mp < 0: ltlBenchMark = 99999999
                if mp > 0: ltlBenchMark = 0

            if useLTLFilter and mp !=0: ltlBenchMark = entryPrice[-1*abs(mp)]
            if useLTLFilter and use2NasLoss and mp !=0: ltlBenchMark = marketVal2[curMarket]

###  Long Break Out Logic here
            prevMP = mp
            if mp >= 1:
 #               print(myDate[curBar]," ",long2NLoss," ",longExit2)

                if long2NLoss < longExit:
                    if(longExitSys1(sysMarkDict)):
                        unPackDict(sysMarkDict)
                    else:
                        if(long2NExit(sysMarkDict)):
                            unPackDict(sysMarkDict)

                if(longExitSys2(sysMarkDict)):
                    unPackDict(sysMarkDict)


            if mp <=-1:
                if short2NLoss > shortExit:
                    if(shortExitSys1(sysMarkDict)):
                        unPackDict(sysMarkDict)
                    else:
                        if(short2NExit(sysMarkDict)):
                            unPackDict(sysMarkDict)
                if(shortExitSys2(sysMarkDict)):
                    unPackDict(sysMarkDict)
            if canTrade:
                if prevMP <= 0:
                    if(longEntrySys1(sysMarkDict)):
                     unPackDict(sysMarkDict)
                longAddOnPrice = marketVal3[curMarket] + (marketVal4[curMarket])*0.5*marketVal1[curMarket]
                longAddOnPrice = roundToNearestTick(longAddOnPrice,1,myMinMove)
                if(longAddOn(sysMarkDict)):
                    unPackDict(sysMarkDict)
                if(longEntrySys2(sysMarkDict)):
                    unPackDict(sysMarkDict)


                if prevMP >= 0:
                    if(shortEntrySys1(sysMarkDict)):
                        unPackDict(sysMarkDict)
                shortAddOnPrice = marketVal3[curMarket] - (marketVal4[curMarket])*0.5*marketVal1[curMarket]
                shortAddOnPrice = roundToNearestTick(shortAddOnPrice,-1,myMinMove)
                if(shortAddOn(sysMarkDict)):
                    unPackDict(sysMarkDict)
                if(shortEntrySys2(sysMarkDict)):
                    unPackDict(sysMarkDict)

#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)

