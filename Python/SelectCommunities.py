import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
ddp = mxd.dataDrivenPages
pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # ED NAME
pageNameField = ddp.pageNameField.name # DIST_NAME

EDLyr = ddp.indexLayer
targetED = pageName
communitiesLyr = arcpy.mapping.ListLayers(mxd, "indea_background_ebc_communities_active")[0]
commLyr_fieldname = "featname"


# Select target ED.
arcpy.SelectLayerByAttribute_management(EDLyr, "NEW_SELECTION","{0} = '{1}'".format(pageNameField, targetED))
# Select points within target ED.
arcpy.SelectLayerByLocation_management(communitiesLyr,"COMPLETELY_WITHIN", EDLyr, 0, "NEW_SELECTION")

# Create list of selected points.
commLst = []
for row in arcpy.da.SearchCursor(communitiesLyr, commLyr_fieldname):
	commLst.append(row[0])

# Build query from list.
query = "{0} IN ({1})".format(commLyr_fieldname, ', '.join("'" + comm + "'" for comm in commLst))

# Apply definition query to communities layer.
communitiesLyr.definitionQuery = query

# Clear the selections.
# arcpy.SelectLayerByAttribute_management(EDLyr, "CLEAR_SELECTION")
# arcpy.SelectLayerByAttribute_management(communitiesLyr, "CLEAR_SELECTION")
