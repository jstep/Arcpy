import os 

# Create an output location variable
outputDirectory = r"C:\temp"  

# Open a text file to append info to
insetTxt = outputDirectory + r"\insetInfo.txt"
FILE = open(insetTxt, "a")

try:
    mxd = arcpy.mapping.MapDocument("current")
    df = arcpy.mapping.ListDataFrames(mxd, "Inset*")[0]
    ddp = mxd.dataDrivenPages
    infoList = []
    infoList.append("\n")
    # The following is information you would like to record
    # The text is written so it can be pasted directly into your script
    # This example assumes that 'pgIndex' is the variable for the current page id
    # and that 'dataFrame' is the variable for the data frame containing the inset map
    infoList.append("if (pgIndex == " + str(ddp.currentPageID) + "):\n")
    infoList.append("\tdataFrame.elementPositionX = " + str(df.elementPositionX) + "\n") 
    infoList.append("\tdataFrame.elementPositionY = " + str(df.elementPositionY) + "\n")
    infoList.append("\tdataFrame.elementHeight = " + str(df.elementHeight) + "\n") 
    infoList.append("\tdataFrame.elementWidth = " + str(df.elementWidth) + "\n")
    infoList.append("\tinsetExtent_" + str(ddp.currentPageID) + " = arcpy.Extent(" +
                    str(df.extent.XMin) + ", " + str(df.extent.YMin) + ", " + 
                    str(df.extent.XMax) + ", " + str(df.extent.YMax) + ")" + "\n")           
    infoList.append("\tdataFrame.extent = insetExtent_" + str(ddp.currentPageID) + "\n")
     
    FILE.writelines(infoList)
except:
    print "Writing to file failed"

# Close the text file
FILE.close()