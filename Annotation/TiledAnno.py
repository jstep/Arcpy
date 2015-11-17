
import arcpy
import os

mxd = arcpy.mapping.MapDocument('CURRENT')
ddp = mxd.dataDrivenPages
pageName = ddp.pageRow.getValue(ddp.pageNameField.name)


parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
workspace = arcpy.env.workspace = os.path.join(parentDir, "anno_fgdb")

GroupAnno = "GroupAnno"
anno_suffix = "Anno"

# Process: Tiled Labels To Annotation
for df in arcpy.mapping.ListDataFrames(mxd):
    fgdb = arcpy.env.workspace = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, df.name, int(round(df.scale))))
    indexPolygon = arcpy.mapping.ListLayers(mxd,"DF_Polygons*{}".format(pageName))[0]
    arcpy.TiledLabelsToAnnotation_cartography(mxd, df.name, indexPolygon, fgdb, GroupAnno, anno_suffix, df.scale, "", "", "", "", "STANDARD", "NOT_GENERATE_UNPLACED_ANNOTATION")
    

