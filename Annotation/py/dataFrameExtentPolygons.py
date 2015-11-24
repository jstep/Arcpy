import arcpy, json, os, sys

#Function that arranges data frames based on the field info within the PageLayoutElements table
def arrangeDFs(row, dfName):
  rowInfo = json.loads(row.getValue(dfName))
  try:
    df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
    df.elementPositionX = rowInfo[0]
    df.elementPositionY = rowInfo[1]
    df.elementWidth = rowInfo[2]
    df.elementHeight = rowInfo[3]
    newExtent = df.extent
    newExtent.XMin = rowInfo[4]
    newExtent.YMin = rowInfo[5]
    newExtent.XMax = rowInfo[6]
    newExtent.YMax = rowInfo[7]
    df.extent = newExtent
    df.scale = rowInfo[8]
    df.rotation = rowInfo[9]
  except IndexError:
  	pass

################################################################################

mxd = arcpy.mapping.MapDocument('CURRENT')
ddp = mxd.dataDrivenPages
inset = "Inset" + "1" # Change value to '1', '2', '3', or '4' to control which inset polygons are made for.
df_lst = arcpy.mapping.ListDataFrames(mxd, inset)

feature_info = []

# Determine page orientation to append to output filename. Fallback to DDP count.
if mxd.pageSize.width > mxd.pageSize.height:
    orient = "_L_"
elif mxd.pageSize.width < mxd.pageSize.height:
    orient = "_P_"
else:
    orient = "square"

# Loop each DDP.
for page in range(1, ddp.pageCount + 1):
    ddp.currentPageID = page
    # ArrangeDFs.
    pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
    pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0] #Reference pageLayoutTable
    #Move all data frames off the layout and into their default positions
    pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "District = '" + pageName + "'")
    pageLayoutRow = pageLayoutCursor.next()

    for df in df_lst:
        arrangeDFs(pageLayoutRow, df.name)
        # Only creates geometry for data frames on the page.
        if (df.elementPositionX > 0 and df.elementPositionX < 11 and 
            df.elementPositionY > 0 and df.elementPositionY < 8.5):
            XMin = df.extent.XMin 
            YMin = df.extent.YMin 
            XMax = df.extent.XMax 
            YMax = df.extent.YMax 
            # A list of features and coordinate pairs
            df_info = [[XMin, YMin],[XMax, YMin],[XMax, YMax],[XMin, YMax]]
            feature_info.append(df_info)
    
    # A list that will hold each of the Polygon objects
    features = []
    
    for feature in feature_info:
        # Create a Polygon object based on the array of points
        # Append to the list of Polygon objects
        features.append(
            arcpy.Polygon(
                arcpy.Array([arcpy.Point(*coords) for coords in feature])))
    
# Persist a copy of the Polygon objects using CopyFeatures
outDir = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\James\DataFrame_Polygon_Boxes"
poly_filename = outDir + r"/dataframePolygons" + orient + inset + ".shp"
if os.path.exists(poly_filename):
	os.remove(poly_filename)
arcpy.CopyFeatures_management(features, poly_filename)

del coords, feature_info, features, feature, poly_filename, outDir, mxd, df_lst, df_info, df, inset, XMax, XMin, YMax, YMin, page, orient, ddp, pageName, pageLayoutCursor, pageLayoutTable, pageLayoutRow 