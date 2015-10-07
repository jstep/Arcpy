"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ExtentBoxexRemovePts.py
# Remove specific points from Inset Extent boxes.
# 
#
# Assumptions: 
# Main map (the one with the extent boxes) is first in TOC
#

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import arcpy

# Adds this script to system path. Used for separation of main script from other code packages.
sys.path.append(os.path.dirname(__file__)) 

from poiDict import poiLyrDict
import clearAllFuncs

# Reference current mxd.
mxd = arcpy.mapping.MapDocument("CURRENT")
# Create list of all data frames (df's).
dfLst = arcpy.mapping.ListDataFrames(mxd)
# Reference main df.
mainDF = dfLst[0]
# Create list of inset df's.
insetLst = dfLst[1:]


# # Create list of Points of Interest layers.
# poiLst = []
# lyrLst = arcpy.mapping.ListLayers(mxd, "*", mainDF)
# for lyr in lyrLst: 
# 	if lyr.name in poiLyrDict:
		

# # Skeleton code to access dict key/value pairs.
# # for key in poiLyrDict:
# #     print key + " has the values of: "
# #     for item in poiLyrDict[key]: 
# #         print item

#########################################
############### Extents #################
#########################################

# Create list of all data frames (df's).
dfLst = arcpy.mapping.ListDataFrames(mxd)
# Create list of inset df's.
insetLst = dfLst[1:]
# Create dictionary for extent(s) of box(es)/inset(s). Extent format: XMin, XMax, YMin, YMax (as tuple).
insetExtentDict = {}
for x in range(len(insetLst)):
	insetExtentDict["Inset{0}".format(x)] = insetLst[x].extent.XMin, insetLst[x].extent.XMax, insetLst[x].extent.YMin, insetLst[x].extent.YMax
	# insetExtentDict["Inset{0}".format(x)] = insetLst[x].extent # Dict populated with extent object instead of extent values.

lyrLst = arcpy.mapping.ListLayers(mxd, "*", mainDF)
for lyr in lyrLst: 
	if lyr.name in poiLyrDict:
		# Select by location (extents)

# Remove points in target extent box.
	# Select specific points in extent box (from extentDict)
		# if XMin < point.x < XMax and YMin < point.y < YMax:
			# Apply queries.