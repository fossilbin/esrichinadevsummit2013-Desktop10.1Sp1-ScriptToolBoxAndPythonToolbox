#-*- coding: UTF-8 -*-
####
##说明：该工具模拟Editor下面的Construct Points工具；arcpy有bug（getLength的值与shape_Area的值不同），
##这里采用通过'shape@length'获取的长度值而不是geo.getLength()获取的长度。

from arcpy import *

map_document = GetParameterAsText(0)
out_jpeg = GetParameterAsText(1)
data_frame = GetParameterAsText(2)
df_export_width = int(GetParameterAsText(3))
df_export_height = int(GetParameterAsText(4))
resolution = GetParameterAsText(5)
world_file = GetParameter(6)
color_mode = GetParameterAsText(7)
jpeg_quality = GetParameterAsText(8)
progressive = GetParameter(9)

mxd = mapping.MapDocument(map_document)

if data_frame:
    df = mapping.ListDataFrames(mxd,data_frame)[0]
    mapping.ExportToJPEG(mxd,out_jpeg,df,df_export_width,df_export_height,resolution,False,color_mode,jpeg_quality,progressive)
else:
    mapping.ExportToJPEG(mxd,out_jpeg,'PAGE_LAYOUT',640,480,resolution,False,color_mode,jpeg_quality,progressive)
    
