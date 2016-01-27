def getSelectionSet():
    """Returns a layer's selection as a Python set of feature IDs the layer's name, the data frame object, and the OID field name.
    Provides an easy way to retrieve the layer's current selection.
    """
    try:
        import arcpy
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        lyrLst = arcpy.mapping.ListLayers(mxd, "*", df) # Only list first dataframe to avoid identically named layers, where all would get selected. 
        fidLst = []
        lyrName = ""
        for lyr in lyrLst:
            try:
                if not lyr.isGroupLayer:
                    desc = arcpy.Describe(lyr)
                    if hasattr(desc, 'FIDSet'):
                        if desc.FIDSet:
                            fidLst.append(desc.FIDSet)
                            lyrName = desc.nameString.split("\\")[-1] # Handles case of layers nested in groups. Gets lyr name minus the group name(s).
                            OIDFieldName = desc.OIDFieldName
            except RuntimeError, TypeError:
                pass

        # Check for multiple layers selected.
        if len(fidLst) > 1:
            raise TypeError("Please select features from a single layer.")

        # Convert list string items to integers.
        fidLst = fidLst[0].split(";")
        fidLst = map(int, fidLst)

        # Return list of selected feature IDs, the selected layer name, the data frame it is in, and the OID field name.
        return fidLst, lyrName, df, OIDFieldName
    except IndexError as ie:
        import pythonaddins
        pythonaddins.MessageBox("{}. Please make a selection.".format(str(ie).capitalize()), "Selection Error")
    except Exception as e:
        import pythonaddins
        pythonaddins.MessageBox(e, "Error")