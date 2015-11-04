def getSelectionSet():
    """Returns a layer's selection as a Python set of feature IDs.
    Provides an easy way to retrieve the layer's current selection.
    """
    mxd = arcpy.mapping.MapDocument("CURRENT")
    lyrLst = arcpy.mapping.ListLayers(mxd)
    fidLst = []
    for lyr in lyrLst:
        try:
            desc = arcpy.Describe(lyr)
            if desc.FIDSet:
                fidLst.append(desc.FIDSet.replace(";", ","))

        except:
            pass

    # Check for multiple layers selected.
    if len(fidLst) > 1:
        raise TypeError("Please select features from a single layer.")
        
    return fidLst # separate items
