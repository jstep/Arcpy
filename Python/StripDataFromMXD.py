import arcpy
mxdPath = "C:\Users\jastepha\Desktop\EDVA Maps\MXD_templates\EDVA_Map_Template_4Sheet.mxd"
mxd = arcpy.mapping.MapDocument(mxdPath)
dfLst = arcpy.mapping.ListDataFrames(mxd)
for df in dfLst:
    for lyr in arcpy.mapping.ListLayers(mxd, data_frame=df):
        if lyr.supports("DATASOURCE"):
            if not "Index" in lyr.dataSource:
                arcpy.mapping.RemoveLayer(df, lyr)

mxdSave = mxdPath.split(".")[0] + "_No_Layers.mxd"
mxd.saveACopy(mxdSave)