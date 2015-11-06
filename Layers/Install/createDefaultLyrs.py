import arcpy
import os
import pythonaddins

sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.
from autoPath import autoPath

arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.path.join(autoPath(), "default_Layers")
workspace = arcpy.env.workspace
os.chdir(workspace)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

annoLst = []
for lyr in arcpy.mapping.ListLayers(mxd,data_frame=arcpy.mapping.ListDataFrames(mxd)[0]):
    if lyr.supports("DATASOURCE"):
        arcpy.env.workspace = os.path.dirname(lyr.dataSource)
        annoLst.append(arcpy.ListFeatureClasses(feature_type="Annotation"))

# Create layerfile for all layers in TOC that support layerfile creation.
for i, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
	for lyr in [item for item in arcpy.mapping.ListLayers(mxd, data_frame=arcpy.mapping.ListDataFrames(mxd)[i]) if item not in annoLst]:
	    if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer and "index" not in lyr.name and lyr.supports("DATASETNAME"):
	    	lyrString = "default_%s_%s.lyr" % (lyr.name, df.name)
	        arcpy.SaveToLayerFile_management(lyr,workspace + "\\" + lyrString, "ABSOLUTE")
