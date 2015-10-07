import arcpy, os

# Create an output directory variable
outDir = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\PDF_prelim_Report_144RGB"

# Create a new, empty pdf document in the specified output directory
# This will be your final product
finalpdf_filename = outDir + r"\FinalMapBook.pdf"
if os.path.exists(finalpdf_filename): # Check to see if file already exists, delete if it does
  os.remove(finalpdf_filename)
finalPdf = arcpy.mapping.PDFDocumentCreate(finalpdf_filename)


# Create a Data Driven Pages object from the mxd you wish to export
#
# mxdPath = r"C:\Project\MapBook\zipCodePopulation.mxd"
tempMap = arcpy.mapping.MapDocument("CURRENT")
tempDDP = tempMap.dataDrivenPages

# Create objects for the layout elements that will be moving, e.g., inset data frame, scale text
dataFrame = arcpy.mapping.ListDataFrames(tempMap, "Inset*")[0]  
  
# Instead of exporting all pages at once, you will need to use a loop to export one at a time  
# This allows you to check each index and execute code to add inset maps to the correct pages
#
for pgIndex in range(1, tempDDP.pageCount + 1, 1):
  
  # Create a name for the pdf file you will create for each page
  temp_filename = r"C:\temp\temp_pdfs\MB_" + \
                            str(pgIndex) + ".pdf"
  if os.path.exists(temp_filename):
    os.remove(temp_filename)
  
  # The following if statements check the current page index against given values
  # If the current page index matches, it will execute code to set up that page
  # If not, the page remains as is
  # Note: If you created a text file containing this information, this is where
  # you would paste in that code

  # insetTxt = outputDirectory + r"\insetInfo.txt"
  # FILE = open(insetTxt, "r")
  # print FILE.read()

  # with open("pdfExport.py", "a") as myfile:
  #     myfile.write("appended text")



if (pgIndex == 1):
  dataFrame.elementPositionX = 3.5488
  dataFrame.elementPositionY = 0.722900000001
  dataFrame.elementHeight = 2.25
  dataFrame.elementWidth = 6.75
  insetExtent_1 = arcpy.Extent(1265548.52465, 452412.503969, 1276874.11938, 456713.049333)
  dataFrame.extent = insetExtent_1

if (pgIndex == 2):
  titleTxt.elementHeight = 0.217200000001
  titleTxt.elementWidth = 1.7795
  titleTxt.elementPositionX = 0.600399999999
  titleTxt.elementPositionY = 8.0929
  dataFrame.elementPositionX = 7.1837
  dataFrame.elementPositionY = 5.7
  dataFrame.elementHeight = 2.0
  dataFrame.elementWidth = 3.0
  insetExtent_2 = arcpy.Extent(-12516515.0504, -9130142.60932, 15058937.6944, 10039268.1626)
  dataFrame.extent = insetExtent_2




  # Code to export current page and add it to mapbook
  tempDDP.exportToPDF(temp_filename, "RANGE", pgIndex)
  finalPdf.appendPages(temp_filename)
  

  # Clean up your page layout by moving the data frame and resetting its extent after exporting the page
  # This will reset the page to the basic layout before exporting the next page
  #
  
  dataFrame.elementPositionX = 10 # Move inset data frame off the page
  dataFrame.scale = 350000000 # Change scale so extent indicator no longer visible in main data frame
  arcpy.RefreshActiveView()

# Clean up
#
del tempMap

# Update the properties of the final pdf
#
finalPdf.updateDocProperties(pdf_open_view="USE_THUMBS",
                             pdf_layout="SINGLE_PAGE")

# Save your result
#
finalPdf.saveAndClose()
