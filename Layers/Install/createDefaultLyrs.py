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

for lyr in df:
    if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer and not lyr.name == "Index":
        lyrString = "default_%s.lyr" % (lyr.name)
        arcpy.SaveToLayerFile_management(lyr,workspace + "\\" + lyrString, "ABSOLUTE")