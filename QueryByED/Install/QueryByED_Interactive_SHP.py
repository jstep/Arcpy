import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
ddp = mxd.dataDrivenPages
pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # ED NAME
pageNameField = ddp.pageNameField.name # DIST_NAME

EDLyr = ddp.indexLayer
targetED = pageName

# Function to clear all queries.
def clearAllQueries():
    for lyr in arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT")):
        if lyr.supports("DEFINITIONQUERY"):
            lyr.definitionQuery = ""
            print "Query for {0} layer cleared.".format(lyr.name)
    arcpy.RefreshActiveView()
# Function to clear selections.
def clearAllSelections():
    for lyr in arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT")):
        if lyr.supports("DATASOURCE"):
            arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION") 

# From clearAllFuncs module.
clearAllQueries()
clearAllSelections()

# Dictionary of the point layers (keys) and their building use codes (values).
poiLyrDict = {
        "Airports": [
            r'%Aero_Air%',
            r'%Aero_Water%'
        ],
        "Fire Hall": [
            r'%Fire%'
        ],
        "Golf Course": [
            r'%Rec_Golf%'
        ],
        "Hall": [
            r'%Civ_CommHall%',
            r'%Com_Church%',
            r'%Com_Centre%'
        ],
        "Hospital": [
            r'%Hosp_Care%',
            r'%Hosp_Ext%',
            r'%Hosp_Hosp%'
        ],
        "School": [
            r'%PostSec_Acad%',
            r'%PostSec_Coll%',
            r'%PostSec_Inst%',
            r'%PostSec_PSec%',
            r'%PostSec_Univ%',
            r'%Sch_Std%'
        ]
}

# Select target ED.
arcpy.SelectLayerByAttribute_management(EDLyr, "NEW_SELECTION","{0} = '{1}'".format(pageNameField, targetED))
# Select points within target ED.
for key in poiLyrDict:
    poiLyr = arcpy.mapping.ListLayers(mxd, key)[0]
    arcpy.SelectLayerByLocation_management(poiLyr, "COMPLETELY_WITHIN", EDLyr, 0, "ADD_TO_SELECTION")


for key, values in poiLyrDict.iteritems():
    oidLst = [] # Create list for selected points OIDs.
    poiLyr = arcpy.mapping.ListLayers(mxd, key)[0]
    bldgQuery = " OR ".join('"bldguses" LIKE %s' % "'" + value + "'" for value in values)
    for row in arcpy.da.SearchCursor(poiLyr, "OID@"):
        oidLst.append(row[0])
    if oidLst:
        ptQuery = '\"{0}\" IN ({1})'.format("FID", ', '.join(str(oid) for oid in oidLst)) # Build query from list. May need to change FID.
        arcpy.mapping.ListLayers(mxd, key)[0].definitionQuery = "(" + ptQuery + ") AND (" + bldgQuery + ")" # Apply definition query to layer.
    else:
        ptQuery = '\"{0}\" IN (-1)'.format("FID") # Build query for empty set. May need to change FID.
        arcpy.mapping.ListLayers(mxd, key)[0].definitionQuery = "(" + ptQuery + ") AND (" + bldgQuery + ")"# Apply definition query to layer.


arcpy.RefreshActiveView()

# Clear the selections.
arcpy.SelectLayerByAttribute_management(EDLyr, "CLEAR_SELECTION")

# Delete variables.
# del mxd, ddp, pageName, pageNameField, EDLyr, targetED, key, oidLst, poiLyr, row



# "bldguses" LIKE '%Aero_Air%' OR bldguses LIKE '%Aero_Water%'