#-*- coding: UTF-8 -*-
####
##说明：该工具模拟Editor下面的Split工具，用于将线根据条件切成几段。

from arcpy import *

def splitByDistance(cur,dist):
    pntList = []
    for geo,length in cur:
        pnt = geo.positionAlongLine(splitValue)
        pntList.append(pnt)
    return pntList
    
def splitIntoEqualParts(cur,parts):
    pntList = []
    for geo,length in cur:
        step = length / parts
        for i in range(int(parts-1)):
            position = step + step * i
            pnt = geo.positionAlongLine(position)
            pntList.append(pnt)
    return pntList
    
def splitByPercentage(cur,percentage):
    pntList = []
    for geo,length in cur:
        pnt = geo.positionAlongLine(length * percentage)
        pntList.append(pnt)
    return pntList

splitMethod = {'Distance':splitByDistance,
                'Into Equal Parts':splitIntoEqualParts,
                'Percentage':splitByPercentage}
                
#type是类型，value是与类型相匹配的值
inLines = GetParameterAsText(0)
outFeatureClass = GetParameterAsText(1)
splitType = GetParameterAsText(2)
splitValue = float(GetParameterAsText(3))

#Cursors
sCur = da.SearchCursor(inLines,['shape@','shape@length'])
pntList = splitMethod[splitType](sCur,splitValue)
SplitLineAtPoint_management(inLines,pntList,outFeatureClass,1)
del sCur

