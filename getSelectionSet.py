def getSelectionSet():
    """Returns a layer's selection as a Python set of feature IDs.
    Provides an easy way to retrieve the layer's current selection.
    """
    mxd = arcpy.mapping.MapDocument("CURRENT")
    lyrLst = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrLst:
        try:
            desc = arcpy.Describe(lyr)
            if desc.FIDSet:
                return desc.FIDSet
        except:
            pass

