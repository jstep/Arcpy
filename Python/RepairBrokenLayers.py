import arcpy
import os

mxd = arcpy.mapping.MapDocument('CURRENT')

lyrLst = arcpy.mapping.ListLayers(mxd)

# Change to location of your geodatabase.
gdbPath = r"P:\15030_32_EBC_Digital_Mapping\MapData\2015 By Election Data\Replicate.gdb"

for lyr in lyrLst:
    if lyr.isBroken:
        if lyr.supports("DATASETNAME"):
            mxd.findAndReplaceWorkspacePaths(lyr.workspacePath, gdbPath + lyr.datasetName, False)
            print "Layer {} repaired.".format(lyr.name)

arcpy.RefreshTOC()