import arcpy
from arcpy import env

env.workspace = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\local_shp\Anno GDBs\MDF Anno GDBs\D2_MDF_147250.gdb" # copy and paste directory between quotation marks.

oldScale = "147250" # e.g. "119500"
newScale = "666" # e.g. "_100000"

for fc in arcpy.ListFeatureClasses():
	arcpy.Rename_management(fc, fc.replace(oldScale, newScale))
