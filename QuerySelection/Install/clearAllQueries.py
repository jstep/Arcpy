def clearAllQueries():
    """Removes all definition queries from layers in T.O.C.""" 
    for lyr in arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT")):
        if lyr.supports("DEFINITIONQUERY"):
            lyr.definitionQuery = ""
            print "Definition query for '{}'' layer cleared.".format(lyr.name)
    arcpy.RefreshActiveView()