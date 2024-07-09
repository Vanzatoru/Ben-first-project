#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      George
#
# Created:     13/08/2019
# Copyright:   (c) George 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math



def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson(masterDateList,marketMonitorList,curMarket,curBar,numDays):
    y = list()
    x = list()
    corrList = list()
    for i in range(0,len(marketMonitorList)):
        if len(y) > 0 : y.clear()
        if len(x) > 0 : x.clear()
        x_date = marketMonitorList[curMarket].marketData.date
        x_close = marketMonitorList[curMarket].marketData.close

        if i != curMarket:
            y_date = marketMonitorList[i].marketData.date
            y_close = marketMonitorList[i].marketData.close
            for j in range(curBar - numDays, curBar):
                if masterDateList[j] in y_date:
                    y.append(y_close[j])
                else:
                    y.append(y_close[-1])
            for j in range(curBar - numDays, curBar):
                if masterDateList[j] in x_date:
                    x.append(x_close[j])
                else:
                    x.append(x_close[-1])
            n = len(x)
            avg_x = average(x)
            avg_y = average(y)
            diffprod = 0
            xdiff2 = 0
            ydiff2 = 0
            for idx in range(n):
                xdiff = x[idx] - avg_x
                ydiff = y[idx] - avg_y
                diffprod += xdiff * ydiff
                xdiff2 += xdiff * xdiff
                ydiff2 += ydiff * ydiff

            corrList.append( diffprod / math.sqrt(xdiff2 * ydiff2))
    return(corrList)

