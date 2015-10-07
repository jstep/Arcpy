import arcpy
import pythonaddins
import time

class QueryPointsByED(object):
    """Implementation for QueryByED_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        import os
    	import sys
        import time
        sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.  
    	from poiDict import poiLyrDict
        import clearAllFuncs

        # Execution time measurment.
        start = time.time()
    	mxd = arcpy.mapping.MapDocument("CURRENT")
    	ddp = mxd.dataDrivenPages
    	pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # ED NAME
    	pageNameField = ddp.pageNameField.name # DIST_NAME

    	EDLyr = ddp.indexLayer
    	targetED = pageName

        # From clearAllFuncs module.
    	clearAllFuncs.clearAllQueries(arcpy.mapping.ListDataFrames(mxd)[0])
    	# clearAllFuncs.clearAllSelections(arcpy.mapping.ListDataFrames(mxd)[0])

        sel_start = time.time()
    	# Select target ED.
    	arcpy.SelectLayerByAttribute_management(EDLyr, "NEW_SELECTION","{0} = '{1}'".format(pageNameField, targetED))
    	# Select points within target ED.
    	for key in poiLyrDict:
    		poiLyr = arcpy.mapping.ListLayers(mxd, key)[0]
    		arcpy.SelectLayerByLocation_management(poiLyr, "COMPLETELY_WITHIN", EDLyr, 0, "ADD_TO_SELECTION")
        sel_end = time.time() 

        dict_start = time.time()
    	for key, values in poiLyrDict.iteritems():
    		oidLst = [] # Create list for selected points OIDs.
    		poiLyr = arcpy.mapping.ListLayers(mxd, key)[0]
    		bldgQuery = " OR ".join('bldguses LIKE %s' % "'" + value + "'" for value in values)
    		for row in arcpy.da.SearchCursor(poiLyr, "OID@"):
    			oidLst.append(row[0])
    		if oidLst:
    			ptQuery = '{0} IN ({1})'.format("se_row_id", ', '.join(str(oid) for oid in oidLst)) # Build query from list.
    			arcpy.mapping.ListLayers(mxd, key)[0].definitionQuery = "(" + ptQuery + ") AND (" + bldgQuery + ")" # Apply definition query to layer.
    		else:
    			ptQuery = '{0} IN (-1)'.format("se_row_id") # Build query for empty set.
    			arcpy.mapping.ListLayers(mxd, key)[0].definitionQuery = "(" + ptQuery + ") AND (" + bldgQuery + ")" # Apply definition query to layer.
        dict_end = time.time() 

    	arcpy.RefreshActiveView()

    	# Clear the selections.
        clear_start = time.time()
    	arcpy.SelectLayerByAttribute_management(EDLyr, "CLEAR_SELECTION")
        clear_end = time.time() 

    	# Delete variables.
    	del mxd, ddp, pageName, pageNameField, EDLyr, targetED, key, oidLst, poiLyr, row

        # Execution time measurment.
        end = time.time() 
        print "\nSelection execution time: " + str(round(sel_end - sel_start, 2)) + "seconds."
        print "\nDictionary execution time: " + str(round(dict_end - dict_start, 2)) + "seconds."
        print "\nClear selection execution time: " + str(round(clear_end - clear_start, 2)) + "seconds."
        print "\nTotal execution time: " + str(round(end - start, 2)) + "seconds."