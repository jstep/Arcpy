import arcpy
import os
import pythonaddins

sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.
from autoPath import autoPath

arcpy.env.overwriteOutput = True
grandParent = os.path.abspath(os.path.join(autoPath(), os.pardir, os.pardir))
workspace = os.path.join(grandParent, "Default_Layers")
if not os.path.exists(workspace):
    os.makedirs(workspace)

arcpy.env.workspace = workspace


mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

annoLst = []
for lyr in arcpy.mapping.ListLayers(mxd,data_frame=arcpy.mapping.ListDataFrames(mxd)[0]):
    if lyr.supports("DATASOURCE"):
        arcpy.env.workspace = os.path.dirname(lyr.dataSource)
        annoLst.append(arcpy.ListFeatureClasses(feature_type="Annotation"))

# Create layerfile for layers in TOC that support layerfile creation.
for lyr in [item for item in arcpy.mapping.ListLayers(mxd, data_frame=df) if item not in annoLst]:
    if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer and "index" not in lyr.name and lyr.supports("DATASETNAME") and not lyr.isBroken:
    	lyrString = "default_%s.lyr" % (lyr.name)
        try:
            arcpy.SaveToLayerFile_management(lyr,workspace + "\\" + lyrString, "ABSOLUTE")
        except Exception as e:
            print e
