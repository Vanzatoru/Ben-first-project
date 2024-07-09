#-------------------------------------------------------------------------------
# Name:        tradeProcessing
# Purpose:
#
# Author:      George
#
# Created:     21/01/2021
# Copyright:   (c) George 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tradeClass import tradeInfo

#-------------------------------------------------------------------------------------------------
# Pay no attention to these  functions - unless you want to I G N O R E
#-------------------------------------------------------------------------------------------------
def exitPos(myExitPrice,myExitDate,tempName,myCurShares,sysMarkDict):
    entryPrice = sysMarkDict.get("entryPrice")
    entryQuant = sysMarkDict.get("entryQuant")
    tempEntryQuant = entryQuant.copy()
    curShares = sysMarkDict.get("curShares")
    mp = sysMarkDict.get("mp")
    marketMonitor = sysMarkDict.get("marketMonitor")
    myBPV = sysMarkDict.get("myBPV")
    cumuProfit = sysMarkDict.get("cumuProfit")
    if mp < 0:
        trades = tradeInfo('liqShort',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit,profitPerEntry = trades.calcTradeProfit('liqShort',mp,entryPrice,myExitPrice,entryQuant,myCurShares)
        profit = profit  * myBPV
        profit = profit - myCurShares *sysMarkDict.get("commission")
        if len(profitPerEntry) > 0:
            for numEnt in range(0,len(profitPerEntry)):
                profitPerEntry[numEnt] = profitPerEntry[numEnt]*myBPV - tempEntryQuant[numEnt] * sysMarkDict.get("commission")
        trades.tradeProfit = profit
        trades.profitPerEntry =profitPerEntry.copy()
        cumuProfit += profit
        trades.cumuProfit = cumuProfit
    if mp > 0:
        trades = tradeInfo('liqLong',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit,profitPerEntry = trades.calcTradeProfit('liqLong',mp,entryPrice,myExitPrice,entryQuant,myCurShares)
        profit = profit * myBPV
        profit = profit - myCurShares * sysMarkDict.get("commission")
        if len(profitPerEntry) > 0:
            for numEnt in range(0,len(profitPerEntry)):
                profitPerEntry[numEnt] = profitPerEntry[numEnt]*myBPV - tempEntryQuant[numEnt] * sysMarkDict.get("commission")
        trades.tradeProfit = profit
        trades.profitPerEntry =profitPerEntry.copy()
        cumuProfit += profit
        trades.cumuProfit = cumuProfit
    sysMarkDict["cumuProfit"] = cumuProfit
    sysMarkDict["mp"] = mp
    curShares = 0
    for remShares in range(0,len(entryQuant)):
        curShares += entryQuant[remShares]
    return (profit,trades,curShares)

def bookTrade(entryOrExit,lOrS,price,date,tradeName,shares,sysMarkDict):
    mp=sysMarkDict.get("mp")
    curShares = sysMarkDict.get("curShares")
    barsSinceEntry = sysMarkDict.get("barsSinceEntry")
    entryPrice = sysMarkDict.get("entryPrice")
    entryQuant = sysMarkDict.get("entryQuant")
    if entryOrExit == -1:
        profit,trades,curShares = exitPos(price,date,tradeName,shares,sysMarkDict)
        mp = 0
    else:
        profit = 0;
        curShares = curShares + shares
        barsSinceEntry = 1
        entryPrice.append(price)
        entryQuant.append(shares)
        if lOrS == 1:
            mp += 1
            trades = tradeInfo('buy',date,tradeName,entryPrice[-1],shares,1)
        if lOrS ==-1:
            mp -= 1
            trades = tradeInfo('sell',date,tradeName,entryPrice[-1],shares,1)

    return(profit,curShares,trades,mp)

def enterLongPosition(myPrice,myNumShares,myTradeName,sysMarkDict):
    todaysCTE = sysMarkDict.get("todaysCTE")
    barsSinceEntry = sysMarkDict.get("barsSinceEntry")
    barsSinceExit = sysMarkDict.get("barsSinceExit")
    curShares = sysMarkDict.get("curShares")
    mp = sysMarkDict.get("mp")
    marketMonitor = sysMarkDict.get("marketMonitor")
    sectorTradesTodayList = sysMarkDict.get("sectorTradesTodayList")
    curSector = sysMarkDict.get("curSector")
    myDate = sysMarkDict.get("myDate")
    curBar = sysMarkDict.get("curBar")

    if mp == 0 and curSector !=999:
        sectorTradesTodayList[curSector] +=1
    if mp <= -1:
        profit,curShares,trades,mp = bookTrade(-1,0,myPrice,myDate[curBar],"LiqShortPos",curShares,sysMarkDict)
        marketMonitor.tradesList.append(trades)
        todaysCTE = profit
        sysMarkDict["mp"] = mp
        sysMarkDict["curShares"] = curShares
    cumuProfit = sysMarkDict.get("cumuProfit")
    profit,curShares,trades,mp = bookTrade(1,1,myPrice,myDate[curBar],myTradeName,myNumShares,sysMarkDict)
    barsSinceEntry = 1
    marketMonitor.setSysMarkTrackingInfo(myTradeName,cumuProfit,mp,barsSinceEntry,0,curShares,trades)
    sysMarkDict["todaysCTE"] = todaysCTE
    sysMarkDict["barsSinceEntry"] = barsSinceEntry
    sysMarkDict["barsSinceExit"] = barsSinceExit
    sysMarkDict["curShares"] = curShares
#    sysMarkDict["cumuProfit"] = cumuProfit
    sysMarkDict["mp"] = mp
#- get out of the market - close out long or short positions... - Anthony
def exitPosition(myPrice, myNumShares, myTradeName,sysMarkDict):
    curShares = sysMarkDict.get("curShares")
    mp = sysMarkDict.get("mp")
    myDate = sysMarkDict.get("myDate")
    curBar = sysMarkDict.get("curBar")
    sectorTradesTodayList = sysMarkDict.get("sectorTradesTodayList")
    curSector = sysMarkDict.get("curSector")
    marketMonitor = sysMarkDict.get("marketMonitor")
    if myTradeName != "Lx-EOFData" and myTradeName != "Sx-EOFData" and curSector != 999:
        sectorTradesTodayList[curSector] -=1
    profit,curShares,trades,mp = bookTrade(-1,0,myPrice,myDate[curBar],myTradeName,myNumShares,sysMarkDict)
    cumuProfit = sysMarkDict.get("cumuProfit")
    sysMarkDict["curShares"] = curShares
    sysMarkDict["mp"] = mp
    sysMarkDict["todaysCTE"] = profit
    sysMarkDict["barsSinceEntry"] = 0
    sysMarkDict["barsSinceExit"] = 1
    marketMonitor.setSysMarkTrackingInfo(myTradeName,cumuProfit,mp,0,1,myNumShares,trades)

#- get the system into a short position and reverse long position if one exists - Anthony
def enterShortPosition(myPrice,myNumShares,myTradeName,sysMarkDict):
    todaysCTE = sysMarkDict.get("todaysCTE")
    barsSinceEntry = sysMarkDict.get("barsSinceEntry")
    barsSinceExit = sysMarkDict.get("barsSinceExit")
    curShares = sysMarkDict.get("curShares")
    mp = sysMarkDict.get("mp")
    marketMonitor = sysMarkDict.get("marketMonitor")
    sectorTradesTodayList = sysMarkDict.get("sectorTradesTodayList")
    curSector = sysMarkDict.get("curSector")
    myDate = sysMarkDict.get("myDate")
    curBar = sysMarkDict.get("curBar")

    if mp == 0 and curSector != 999:
         sectorTradesTodayList[curSector] +=1
    if mp >= 1:
        profit,curShares,trades,mp = bookTrade(-1,0,myPrice,myDate[curBar],"LiqLongPos",curShares,sysMarkDict)
        marketMonitor.tradesList.append(trades);todaysCTE = profit
        sysMarkDict["mp"] = mp
        sysMarkDict["curShares"] = curShares
    profit,curShares,trades,mp = bookTrade(1,-1,myPrice,myDate[curBar],myTradeName,myNumShares,sysMarkDict)
    barsSinceEntry = 1
    cumuProfit = sysMarkDict.get("cumuProfit")
    marketMonitor.setSysMarkTrackingInfo(myTradeName,cumuProfit,mp,barsSinceEntry,barsSinceExit,curShares,trades)
    sysMarkDict["todaysCTE"] = todaysCTE
    sysMarkDict["barsSinceEntry"] = barsSinceEntry
    sysMarkDict["barsSinceExit"] = barsSinceExit
    sysMarkDict["curShares"] = curShares
#    sysMarkDict["cumuProfit"] = cumuProfit
    sysMarkDict["mp"] = mp


#---------- Done with trade functions - I G N O R E
