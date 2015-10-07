"""******************************************************************
shpToTxtCoords.py
Version: ArcGIS 10.2.1

Description: Writes the X and Y coordinates of a polygon shapefile's
verticies with a descriptive label to a text file.  

Author: James Stephaniuk

Date: April 23, 2015
******************************************************************"""

import arcpy

# Map document - MXD.
mxd = arcpy.mapping.MapDocument('CURRENT')
# Polygon feature class. Target feature must be the first item in TOC.
fc = arcpy.mapping.ListLayers(mxd)[0]

# Create 'describe' object.
desc = arcpy.Describe(fc)
# Get shape field name and layer name of feature class.
if hasattr(desc, "ShapeFieldName") and hasattr(desc, "baseName"):
    ShapeFieldName = desc.ShapeFieldName
    layerName = desc.baseName

# Output save path for text file.
outDir = r"P:\\15045 - ED Redistribution - Event Specific\\R2015\21-Electoral_Boundaries_Commission_Support_Doc\\WBS 8 - Geography\\James\\XY\\"

# Column of shapefile for text file label. 
inField = "DIST_NAM_1"

# Create update cursor on feature class.
uCursor = arcpy.UpdateCursor(fc)

# Open text file with overwrite permissions (w). Creates a text file if one does not exist already.
# f = open(r"P:\\15045 - ED Redistribution - Event Specific\\R2015\21-Electoral_Boundaries_Commission_Support_Doc\\WBS 8 - Geography\\James\\XY\\Melnick_Final.txt", 'w')
f = open("{}{}.txt".format(outDir, layerName), 'w')
for shp in uCursor:
    polygon = shp.getValue(ShapeFieldName)
    for point in polygon:
        for p in point:
        	# Convert x-y coordinates to strings for file writing.
            x = str(p.X)
            y = str(p.Y)
            # Write inField, x, y to text file.
            f.write(shp.getValue(inField) + ",")
            f.write(x + ",")
            f.write(y + "\n")
# Close text file.
f.close()
