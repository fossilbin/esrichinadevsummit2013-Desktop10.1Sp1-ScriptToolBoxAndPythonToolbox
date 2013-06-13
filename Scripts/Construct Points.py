#-*- coding: UTF-8 -*-
####
##说明：该工具模拟Editor下面的Construct Points工具；arcpy有bug（getLength的值与shape_Area的值不同），
##这里采用通过'shape@length'获取的长度值而不是geo.getLength()获取的长度。

from arcpy import *

#type是类型，value是与类型相匹配的值
inLines = GetParameterAsText(0)
outLocation = GetParameterAsText(1)
outName = GetParameterAsText(2)
type = GetParameterAsText(3)
value = float(GetParameterAsText(4))
endOption = GetParameterAsText(5)

#Parameters
env.overwriteOutput = True
desc = Describe(inLines)
sr = desc.SpatialReference

result = CreateFeatureclass_management(outLocation,outName,"POINT",inLines,"","",sr)
fdList = [fd.name for fd in desc.fields if fd.editable and fd.type != 'Geometry'] + ['shape@','shape@length']

#Cursors
sCur = da.SearchCursor(inLines,fdList)
iCur = da.InsertCursor(result.getOutput(0),fdList[:-1])

#Construct Points From Lines
for row in sCur:
    geo,length = row[-2:]
    if type == 'Number of Points':
        pointsNumber = value
        step = length / (pointsNumber + 1)
        print step
        for i in range(int(pointsNumber)):
            position = step + step * i
            pnt = geo.positionAlongLine(position)
            iCur.insertRow(row[:-2] + (pnt,))
                
    elif type == 'Distance':
        step = value
        pointsNumber = int(length / step)
        for i in range(pointsNumber):
            position = step + step * i
            pnt = geo.positionAlongLine(position)
            iCur.insertRow(row[:-2] + (pnt,))
            
    if endOption == 'Start':
        iCur.insertRow(row[:-2] + (geo.firstPoint,))
    elif endOption == 'End':
        iCur.insertRow(row[:-2] + (geo.lastPoint,))
    elif endOption == 'Both':
        iCur.insertRow(row[:-2] + (geo.firstPoint,))
        iCur.insertRow(row[:-2] + (geo.lastPoint,))

del sCur,iCur
SetParameterAsText(6,result.getOutput(0))