import arcpy
import os
import pythonaddins

arcpy.env.overwriteOutput = True
# arcpy.env.workspace = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\Layer_Packages_for_PDF_Notes-Changes\Default_Layers"
arcpy.env.workspace = pythonaddins.OpenDialog("Select location to save default layers", False, os.path.basename, "Select Folder")
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
