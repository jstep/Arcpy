
def Anno():
	"""Turns on the annotation for only the current DDP."""
	import arcpy
	import collections
	
	mxd = arcpy.mapping.MapDocument("current")  #CURRENT.
	try:
	    ddp = mxd.dataDrivenPages
	except:
		print "Data Driven Pages in not enabled on this map document"
	try:	
	    annoLyr = arcpy.mapping.ListLayers(mxd,"Annotation")[0]
	except:
		print "No layer named 'Annotation'"
		
	pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
	
	for lyr in annoLyr:
	    if lyr.supports("DATASOURCE"):
	        tableCount = collections.Counter(row[0] for row in arcpy.da.SearchCursor(lyr, "TileID"))
	        if tableCount:
	        	if str(arcpy.da.SearchCursor(lyr, "TileID").next()[0]) == str(pageName):
	        		lyr.visible = True
	        	else:
	        		lyr.visible = False
	        else:
	        	lyr.visible = False
	arcpy.RefreshTOC()
	del lyr
	del annoLyr
	del tableCount
	del pageName
	del mxd
	del ddp

# for lyr in annoLyr:
#     if lyr.supports("DATASOURCE"):
#         TileID =  arcpy.da.SearchCursor(lyr,"TileID", "Name = '" + pageName + "'")
#         print pageName


# #set pageName

#  # 1) Loop the Annotation Layer
#  # 2) if layer supports "DATASOURCE" (Or whatever) continue. Change this to check for NONE type.
#  # 3) if layer field of TileID= pageName 
#  # 4) set visible to true.


# mxd = arcpy.mapping.MapDocument("current")  #CURRENT.
# ddp = mxd.dataDrivenPages

# annoLyr = arcpy.mapping.ListLayers(mxd,"Annotation")[0]
# pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
# for lyr in annoLyr: #Loop each feature in Annotation.
#     if arcpy.management.GetCount(lyr)[0] == "0":
#         with arcpy.da.SearchCursor(lyr, "TileID") as cursor:
#             for row in cursor:
#                 if str(row[0]) == str(pageName):
#                     lyr.visible = True
#                 else:
#                     lyr.visible = False
# arcpy.RefreshTOC()   
# _____________________________________________________________________________________________________________

# annoLyr = arcpy.mapping.ListLayers(mxd,"Annotation")[0]
# pageName = ddp.pageRow.getValue(ddp.pageNameField.name)

# for lyr in annoLyr: # Loop Annotation layers.
# 	if lyr.supports("DATASOURCE"): # Check to avoid sub layer (usually called 'Default').
# 		# Check for empty table.
# 			tileID = arcpy.da.SearchCursor(lyr,"TileID") 
# 			if str(tileID) == str(pageName):
# 				lyr.visible = True
# 		else:
# 			lyr.visible = False
# 			break

# arcpy.RefreshTOC()


# _____________________________________________________________________________________________________________
