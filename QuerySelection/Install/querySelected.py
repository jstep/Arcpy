def querySelected():
    """Builds a definition query to display only the currently 
    selected features for that layer.
    """
    import arcpy, os, sys
    sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.
    import getSelectionSet
    mxd = arcpy.mapping.MapDocument("CURRENT")
    ids, name, df, oid = getSelectionSet.getSelectionSet()
    lyr = arcpy.mapping.ListLayers(mxd, name, df)[0]
    
    # Build SQL clause to use in definition query.
    whereClause = "{} in ({})".format(oid, ','.join(str(id) for id in ids))

    # Apply the definition query.
    lyr.definitionQuery = whereClause

    arcpy.RefreshActiveView()