import arcpy

mxd = arcpy.mapping.MapDocument('CURRENT')

# lyr = arcpy.mapping.ListLayers(mxd)[0]
lyrLst = arcpy.mapping.ListLayers(mxd)

for lyr in lyrLst:
    if lyr.supports("WORKSPACEPATH"):
        if lyr.isBroken:
            mxd.findAndReplaceWorkspacePaths(lyr.workspacePath, r"C:\Users\jastepha\Desktop\testOutput\cat\bar\baz", True)
            print "Layer {} repaired.".format(lyr.name)

arcpy.RefreshTOC()