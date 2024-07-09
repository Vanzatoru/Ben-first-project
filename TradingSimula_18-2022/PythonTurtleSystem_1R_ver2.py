#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'PythonTurt_1R_ver2' #System Name here
initCapital = 1000000
commission = 0
anyLossIsALoser = True
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = True
useLaguerre       = False
useParabolic     = False
useStochastic    = False
useRSI           = False
useMACD          = False
useDominantCycle = False

from IncludeCode import includeImports,includeCodeDict,includeCode_A,includeCode_B
from IncludeCode import includeCode_C,includeCode_D,includeCode_E
from IncludeCode import includeCode_Last1,includeCode_Last2,includeCode_Last3
from IncludeCode import includeCode_Last4

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

longExit2 = shortExit2 = 0;
long2NLoss = short2NLoss = 0

theoMP = list()
theoEP = list()
theoWL = list()
theo2NLoss = list()

NValue = list()
real2NLoss = list()
tradesString = list()

curTradesList = list() #user defined list
for curMarket in range(0,numMarkets):
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
    theoWL.append(-1)
    theoMP.append(0)
    theoEP.append(0)
    theo2NLoss.append(0)
    real2NLoss.append(0)
    NValue.append(-999999)
    tradesString.append("")


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

            if mp == 1: longEntryName = curTradesList[-1].tradeName
            if mp ==-1: shortEntryName = curTradesList[-1].tradeName

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

#           posSize = unitSize
            posSize = 1

##            if mp >= 1 :
##                long2NLoss = marketVal2[curMarket]
##            if mp <= -1 :
##                short2NLoss = marketVal2[curMarket]

###  Okay let's simulate the 20 day break out entry and exit logic
###  Long Break Out Logic here


            if theoMP[curMarket] == 1 and longExit > theo2NLoss[curMarket] and \
            myLow[curBar] <= longExit:
                tempPrice = min(longExit,myOpen[curBar])
                tradesString[curMarket] += " "+str(myDate[curBar]) + " Lxit at " + str(tempPrice) +'\n'
                if tempPrice >= theoEP[curMarket]:
                    theoWL[curMarket] = 1
                else:
                    if anyLossIsALoser:
                        theoWL[curMarket] = -1
                    else:
                        theoWL[curMarket] = 1
                theoMP[curMarket] = 0


            if theoMP[curMarket] == 1 and myLow[curBar] <= theo2NLoss[curMarket]:
                theoWL[curMarket] = -1
                theoMP[curMarket] = 0
                tradesString[curMarket] +=" "+str(myDate[curBar]) +  " Lxit at 2N "  +'\n'


###  Short Break Out Logic here


            if theoMP[curMarket] ==-1 and shortExit < theo2NLoss[curMarket] and \
            myHigh[curBar] >= shortExit:
                tempPrice = max(shortExit,myOpen[curBar])
                if tempPrice <= theoEP[curMarket]:
                    theoWL[curMarket] = 1
                else:
                    if anyLossIsALoser:
                        theoWL[curMarket] = -1
                    else:
                        theoWL[curMarket] = 1
                theoMP[curMarket] = 0
                tradesString[curMarket] += " "+str(myDate[curBar]) + " Sxit at " + str(tempPrice) +'\n'


            if theoMP[curMarket] == -1 and myHigh[curBar] >= theo2NLoss[curMarket]:
                theoWL[curMarket] = -1
                theoMP[curMarket] = 0
                tradesString[curMarket] +=" "+str(myDate[curBar]) +  " Sxit at 2N "  +'\n'

            if myHigh[curBar] >= buyLevel  and theoMP[curMarket] !=1:
                theoEP[curMarket] = max(buyLevel,myOpen[curBar])
                tradesString[curMarket] += " "+ str(myDate[curBar]) + " Buy at " + str(theoEP[curMarket])
                theoMP[curMarket] = 1
                theo2NLoss[curMarket] = theoEP[curMarket] - 2 * NValue[curMarket]

            if myLow[curBar] <= shortLevel and theoMP[curMarket] !=-1:
                theoEP[curMarket] = min(shortLevel,myOpen[curBar])
                theoMP[curMarket] = -1
                tradesString[curMarket] += " "+ str(myDate[curBar]) + " Short at " + str(theoEP[curMarket])

                theo2NLoss[curMarket] = theoEP[curMarket] + 2 * NValue[curMarket]


            if myDate[curBar]  == 99999999 and curMarket == 0:
                for mkt in range(0,numMarkets):
                    print(myComLongNameList[mkt])
                    print(tradesString[mkt])
#  Okay  Let's put in some logic to create a long position
#  Long Entry System #1

            if myHigh[curBar] >= buyLevel and mp !=1 and theoWL[curMarket] == -1  :
                price = max(myOpen[curBar],buyLevel)
                tradeName = "TurtSys1:B"
                long2NLoss = price - 2 * NValue[curMarket]
                real2NLoss[curMarket] = roundToNearestTick(long2NLoss,1,myMinMove)
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

 #  Long Entry System #2
            if myHigh[curBar] >= buyLevel2 and mp !=1   :
                price =max(myOpen[curBar],buyLevel2)
                tradeName = "TurtSys2:B"
                long2NLoss = price - 2 * NValue[curMarket]
                real2NLoss[curMarket] = roundToNearestTick(long2NLoss,1,myMinMove)
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry System #1
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar] <= shortLevel and mp !=-1 and theoWL[curMarket] == -1  :
                price = min(myOpen[curBar],shortLevel)
                tradeName = "TurtSys1:S"
                short2NLoss = price + 2 * NValue[curMarket]
                real2NLoss[curMarket] = roundToNearestTick(short2NLoss,1,myMinMove)
                enterShortPosition(price, posSize, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry System #2
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar] <= shortLevel2 and mp !=-1:
                price = min(myOpen[curBar],shortLevel2)
                tradeName = "TurtSys2:S"
                short2NLoss = price + 2 * NValue[curMarket]
                real2NLoss[curMarket] = roundToNearestTick(short2NLoss,1,myMinMove)
                enterShortPosition(price, posSize, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Long Exit 1
            if mp == 1 and myLow[curBar] <= longExit and \
            longExit > real2NLoss[curMarket] and \
            longEntryName == "TurtSys1:B" and barsSinceEntry > 1:
                price = min(myOpen[curBar],longExit)
                tradeName = "TurtSys1-Lx"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Long Exit 2
            if mp == 1 and myLow[curBar] <= longExit2 and \
            longExit2 > real2NLoss[curMarket] and \
            longEntryName == "TurtSys2:B" and barsSinceEntry > 1:
                price = min(myOpen[curBar],longExit)
                tradeName = "TurtSys2:Lx"
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Long Exit 2N Loss
            if mp == 1 and myLow[curBar] <= real2NLoss[curMarket] and barsSinceEntry > 1:
                price = min(myOpen[curBar],real2NLoss[curMarket])
                tradeName = "Turt2N:Lx"
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Exit
            if mp == -1 and myHigh[curBar] >= shortExit and \
            shortExit < real2NLoss[curMarket] and \
            shortEntryName == "TurtSys1:S" and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit)
                tradeName = "TurtSys1:Sx"
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Exit System #2
            if mp == -1 and myHigh[curBar] >= shortExit2 and \
            shortExit2 < real2NLoss[curMarket] and \
            shortEntryName == "TurtSys2:S" and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit2)
                tradeName = "TurtSys2:Sx"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit 2N Loss
            if mp == -1 and myHigh[curBar] >= real2NLoss[curMarket] and barsSinceEntry > 1:
                price = max(myOpen[curBar],real2NLoss[curMarket])
                tradeName = "Turt2N:Sx"
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)


#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)

