import arcpy
import os
import pythonaddins

# Restore Page Layout (from PageLayoutElements table) before running this script.

mxd = arcpy.mapping.MapDocument('CURRENT')
ddp = mxd.dataDrivenPages
pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
df_lst = arcpy.mapping.ListDataFrames(mxd)
onMapDFs = []
# List of data frames on the current page.
for df in df_lst:
    if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
        onMapDFs.append(df)

feature_info = []
for df in onMapDFs:
    # Only creates geometry for data frames on the page. Also creates FGDB.
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
    features.append(arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in feature])))
    

# Persist a copy of the Polygon objects using CopyFeatures
poly_filename = "DF_Polygons_{}".format(pageName)
parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
outDir = os.path.join(parentDir, "anno_fgdb")
if not os.path.exists(outDir):
	os.makedirs(outDir)
workspace = arcpy.env.workspace = outDir

arcpy.CopyFeatures_management(features, poly_filename)

# Create FGDB(s).
for df in onMapDFs:
    arcpy.CreateFileGDB_management(workspace, "{}_{}_{}".format(pageName, df.name, str(int(round(df.scale)))), "CURRENT")

del coords, feature_info, features, feature, poly_filename, outDir, mxd, df_lst, df_info, df, XMax, XMin, YMax, YMin, ddp, pageName 

