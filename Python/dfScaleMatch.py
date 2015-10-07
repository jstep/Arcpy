import arcpy
import collections
import re

mxd = arcpy.mapping.MapDocument("current")  #CURRENT.
ddp = mxd.dataDrivenPages
df = arcpy.mapping.ListDataFrames(mxd, "MainDF")[0]
dfScale = int(df.scale)
annoLyr = arcpy.mapping.ListLayers(mxd,"Anno*")[0]

for lyr in annoLyr:
    if lyr.supports("DATASOURCE"): # Weeds out 'default' sub-layer.
        lyrScale = int(re.match('.*?([0-9]+)$', str(lyr.name)).group(1)) # Matches digits at end of string.
        if lyrScale:
            if lyrScale == dfScale:
                lyr.visible = True
            else:
                lyr.visible = False
        else:
            lyr.visible = False
arcpy.RefreshTOC()
del lyr, annoLyr, mxd, ddp, df, dfScale, lyrScale