import arcpy

mxd = arcpy.mapping.MapDocument('CURRENT')

# lyr = arcpy.mapping.ListLayers(mxd)[0]
lyrLst = arcpy.mapping.ListLayers(mxd)
replacePath = r"P:\15030_32_EBC_Digital_Mapping\MapData\2015 By Election Data\replicateSDE_Logfiles"

for lyr in lyrLst:
    if lyr.supports("WORKSPACEPATH"):
        if lyr.isBroken:
            mxd.findAndReplaceWorkspacePaths(lyr.workspacePath, replacePath, False)
            print "Layer {} repaired.".format(lyr.name)

arcpy.RefreshTOC()