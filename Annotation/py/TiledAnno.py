import arcpy
import os

mxd = arcpy.mapping.MapDocument("CURRENT")
ddp = mxd.dataDrivenPages
pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
df_lst = arcpy.mapping.ListDataFrames(mxd)
onMapDFs = []
# List of data frames on the current page.
for df in df_lst:
    if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
        onMapDFs.append(df)

GroupAnno = "GroupAnno"
anno_suffix = "Anno"
indexLyrName = "DF_Polygons_{}".format(pageName)
tileIndexPoly = arcpy.mapping.ListLayers(mxd, indexLyrName)[0]

parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
workspace = arcpy.env.workspace = os.path.join(parentDir, "anno_fgdb")

for df in onMapDFs:
    # arcpy.activeView = df.name
    try:
        fgdb = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, str(df.name), int(round(df.scale))))
        if os.path.exists(fgdb):
            arcpy.TiledLabelsToAnnotation_cartography(mxd.filePath, str(df.name), tileIndexPoly, fgdb, GroupAnno + str(df.name) + "_", anno_suffix, round(df.scale), "", "", "", "", "STANDARD", "GENERATE_UNPLACED_ANNOTATION")
    except Exception as e:
        print e

# Turn off all labels.
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("LABELCLASSES"):
        lyr.showLabels = False

# Remove DF Polygons.
for df in df_lst:
    for lyr in arcpy.mapping.ListLayers(mxd,"", df):
        if lyr.name.lower().startswith("df_polygons"):
            arcpy.mapping.RemoveLayer(df, lyr)

del anno_suffix, ddp, df, df_lst, fgdb, GroupAnno, indexLyrName, lyr, mxd, onMapDFs, pageName, parentDir, tileIndexPoly