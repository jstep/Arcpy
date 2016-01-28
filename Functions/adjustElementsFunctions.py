def adjustScaleElements():
    """Function to place each scale element to a predefined location (bottom left) within its parent dataframe."""
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df_lst = arcpy.mapping.ListDataFrames(mxd)[1:]
    scaleTextLst = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale text*")
    scaleBarLst = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale bar*")
    scaleNorth = scaleTextLst + scaleBarLst

    # Reset inset data frames.
    for index, df in enumerate(df_lst):
        for i, elem in enumerate(scaleTextLst):
            if hasattr(elem, 'parentDataFrameName') and elem.parentDataFrameName == df.name:
                if elem.parentDataFrameName == df.name:
                    elem.elementPositionX = df.elementPositionX + 0.25
                    elem.elementPositionY = df.elementPositionY + 0.70
        for i, elem in enumerate(scaleBarLst):
            if hasattr(elem, 'parentDataFrameName') and elem.parentDataFrameName == df.name:
                if elem.parentDataFrameName == df.name:
                    elem.elementPositionX = df.elementPositionX + 0.25
                    elem.elementPositionY = df.elementPositionY + 0.25



# Puts graphical north arrow elements (with center anchor points) to the top right of inset dataframes with 1/4 inch padding.
def adjustNorthElements():
    """Function to place each north arrow element to a predefined location (bottom left) within its parent dataframe."""
    mxd = arcpy.mapping.MapDocument("CURRENT")
    insetLst = arcpy.mapping.ListDataFrames(mxd)[1:]
    northArrowLst = arcpy.mapping.ListLayoutElements(mxd, wildcard="*north*")

    # Reset inset data frames.
    for index, df in enumerate(insetLst):
        northArrowLst[index].elementHeight = 0.5666
        northArrowLst[index].elementWidth = 0.272
        northArrowLst[index].elementPositionY = df.elementPositionY + df.elementHeight - (northArrowLst[index].elementHeight / 2) - 0.25
        northArrowLst[index].elementPositionX = df.elementPositionX + df.elementWidth - (northArrowLst[index].elementWidth / 2) - 0.25


# Print number of scale bars, scale texts, and data frames. Should be 17 for all.
print "Number of Scale Bars: {}".format(len(arcpy.mapping.ListLayoutElements(arcpy.mapping.MapDocument("CURRENT"), wildcard="*scale bar*")))
print "Number of Scale Texts: {}".format(len(arcpy.mapping.ListLayoutElements(arcpy.mapping.MapDocument("CURRENT"), wildcard="*scale text*")))
print "Number of North Arrows: {}".format(len(arcpy.mapping.ListLayoutElements(arcpy.mapping.MapDocument("CURRENT"), wildcard="*north*")))
print "Number of Data Frames: {}".format(len(arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))))