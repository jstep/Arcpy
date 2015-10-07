import arcpy, os, sys

mxd       = arcpy.mapping.MapDocument('CURRENT')
ddp       = mxd.dataDrivenPages
df_lst    = arcpy.mapping.ListDataFrames(mxd)
inset_lst = arcpy.mapping.ListDataFrames(mxd)[1:]

feature_info = []

# A list that will hold each of the Polygon objects
features = []

# Determine page orientation to append to output filename. Fallback to DDP count.
if mxd.pageSize.width > mxd.pageSize.height:
    orient = "_L"
elif mxd.pageSize.width < mxd.pageSize.height:
    orient = "_P"
else:
    orient = "_sq"
    
for df in inset_lst:
    # Only creates geometry for data frames on the page.
    if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and 
        df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
        XMin = df.extent.XMin 
        YMin = df.extent.YMin 
        XMax = df.extent.XMax 
        YMax = df.extent.YMax 
        # A list of features and coordinate pairs
        df_info = [[XMin, YMin],[XMax, YMin],[XMax, YMax],[XMin, YMax]]
        feature_info.append(df_info)



    for feature in feature_info:
        # Create a Polygon object based on the array of points
        # Append to the list of Polygon objects
        features.append(
            arcpy.Polygon(
                arcpy.Array([arcpy.Point(*coords) for coords in feature])))
    
# Persist a copy of the Polygon objects using CopyFeatures
outDir = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\James\py" # TODO: Change out location.
poly_filename = outDir + r"/dataframePolygon.shp"
if os.path.exists(poly_filename):
	os.remove(poly_filename)
arcpy.CopyFeatures_management(features, poly_filename)

del coords, feature_info, features, feature, poly_filename, outDir, mxd, df_lst, df_info, df, XMax, XMin, YMax, YMin, orient, ddp 