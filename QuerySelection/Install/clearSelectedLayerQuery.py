def clearSelectedLayerQuery():
    """Clear definition query from the layer selected in the T.O.C."""
    try:
        import arcpy, pythonaddins
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        lyr.definitionQuery = ""
        print "Definition query for '{}'' layer cleared.".format(lyr.name)
        arcpy.RefreshActiveView()
    except AttributeError as e:
        pythonaddins.MessageBox("Please select a layer in the T.O.C to clear it's query", "Error")
        print e