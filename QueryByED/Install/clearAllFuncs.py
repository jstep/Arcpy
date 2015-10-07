# Function to clear all queries.
import arcpy
def clearAllQueries(targetDF):
    """Clears all queries from each layer of MXD."""
    for lyr in arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"), "*", targetDF):
        if lyr.supports("DEFINITIONQUERY"):
            lyr.definitionQuery = ""
            print "Query for {0} layer cleared.".format(lyr.name)
    arcpy.RefreshActiveView()
# Function to clear selections.
def clearAllSelections(targetDF):
    """Clears all current selections from MXD."""
    for lyr in arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"), "*", targetDF):
        if lyr.supports("DATASOURCE"):
            arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")