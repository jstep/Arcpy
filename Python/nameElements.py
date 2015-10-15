import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")

dfs_lst = arcpy.mapping.ListDataFrames(mxd) # List of all dataframes. MainDF and Insets.
mainDF = arcpy.mapping.ListDataFrames(mxd)[0] # Assumes main data frame is first in TOC.
insetDF_lst = arcpy.mapping.ListDataFrames(mxd, "*Inset*")
mapElem_lst = arcpy.mapping.ListLayoutElements(mxd,"MAPSURROUND_ELEMENT", "*SCALE*") + arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", "*NORTH*")
          
def nameMapElements(elementList):
	"""Append parent data frame name to map elements."""
    for index, elem in enumerate(elementList):
	    if type(elem) in ["MAPSURROUND_ELEMENT", "LEGEND_ELEMENT", "TEXT_ELEMENT"]:
	        elem.name = elem.name + elem.parentDataFrameName

nameMapElements(mapElem_lst)
nameMapElements(insetDF_lst) # Won't do anything because they are of type "DATAFRAME_ELEMENT".



