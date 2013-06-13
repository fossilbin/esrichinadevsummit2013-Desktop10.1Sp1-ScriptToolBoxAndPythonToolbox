#-*- coding: UTF-8 -*-
####
##说明：该工具用于遍历所有的线，并将闭合的线转成面，同时属性继承过来。对于不闭合的线可以闭合并导出，
##也可以舍弃

from arcpy import *

#closeLine用于指定是否将不闭合的线闭合
inLines = GetParameterAsText(0)
outLocation = GetParameterAsText(1)
outName = GetParameterAsText(2)
closeLine = GetParameter(3)

desc = Describe(inLines)
sr = desc.SpatialReference
result = CreateFeatureclass_management(outLocation,outName,"POLYGON",inLines,"","",sr)

fdList = [fd.name for fd in desc.fields if fd.editable and fd.type != 'Geometry'] + ['shape@']

#Cursors
sCur = da.SearchCursor(inLines,fdList)
iCur = da.InsertCursor(result.getOutput(0),fdList)

#polylines to polygons
for row in sCur:
    temp = []
    for part in row[-1]:
        part = list(part)
        pnt1,pnt2 = (part[0],part[-1])
        
        if pnt1.equals(pnt2):
            temp.append(part)
        else:
            if closeLine == True:
                part.append(pnt1)
                temp.append(part)
                
    if len(temp) > 1:
        arr = Array(temp)
    elif len(temp) == 0:
        continue
    elif len(temp) == 1:
        arr = Array(temp[0])
        
    geo = Polygon(arr)
            
    iCur.insertRow(sCur[:-1] + (geo,))

del sCur,iCur
SetParameterAsText(4,result.getOutput(0))