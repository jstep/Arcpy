# Start of write scale/rotation to Index table feature.
indexTable = arcpy.mapping.ListLayers(mxd,"Index Layer")[0]
fieldNames = ["scale", "rotation"]
sqlClause = "\"District\" = '" + pageName + "'"

# Assign first (i.e. zeroth) dataframe to variable. Should be 'MainDF'.
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Create an Update Cursor object on the DDP Index Layer for the current page row. 
scaleRotationUpdateCursor = arcpy.da.UpdateCursor(indexTable, fieldNames, sqlClause)
scaleRotationUpdateRow = scaleRotationUpdateCursor.next()

# Set Index Layer scale field equal to MainD
scaleRotationUpdateRow[0] = df.scale
scaleRotationUpdateRow[1] = df.rotation
scaleRotationUpdateCursor.updateRow(scaleRotationUpdateRow)

del scaleRotationUpdateRow, scaleRotationUpdateCursor # End of scale/rotation feature