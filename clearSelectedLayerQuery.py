def clearSelectedLayerQuery():
    """Clear definition query from the layer selected in the T.O.C."""
    import pythonaddins
    lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
    lyr.definitionQuery = ""
    print "Definition query for '{0}'' layer cleared.".format(lyr.name)
    arcpy.RefreshActiveView()