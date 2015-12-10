import arcpy
import json
import os
import pythonaddins

###################### Function Definitions #################################

def arrangeDFs(row, dfIndex, dfName):
  """Function that arranges data frames based on the field info within the PageLayoutElements table. List order must match setDF order."""          
  try:
    mxd = arcpy.mapping.MapDocument("CURRENT")
    rowInfo = json.loads(row.getValue(dfName))
    df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
    nArrowLst = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*North*") + arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", "*north*")
    nArrow = nArrowLst[dfIndex]
    scaleText = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale text*")[dfIndex]
    scaleBar = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale bar*")[dfIndex]
  
    df.elementPositionX        = rowInfo[0]
    df.elementPositionY        = rowInfo[1]
    df.elementWidth            = rowInfo[2]
    df.elementHeight           = rowInfo[3]
    newExtent                  = df.extent
    newExtent.XMin             = rowInfo[4]
    newExtent.YMin             = rowInfo[5]
    newExtent.XMax             = rowInfo[6]
    newExtent.YMax             = rowInfo[7]
    df.extent                  = newExtent
    df.scale                   = rowInfo[8]
    df.rotation                = rowInfo[9]
    nArrow.elementWidth        = rowInfo[10]
    nArrow.elementHeight       = rowInfo[11]
    nArrow.elementPositionX    = rowInfo[12]
    nArrow.elementPositionY    = rowInfo[13]
    scaleText.elementWidth     = rowInfo[14]
    scaleText.elementHeight    = rowInfo[15]
    scaleText.elementPositionX = rowInfo[16]
    scaleText.elementPositionY = rowInfo[17]
    scaleBar.elementWidth      = rowInfo[18]
    scaleBar.elementHeight     = rowInfo[19]
    scaleBar.elementPositionX  = rowInfo[20]
    scaleBar.elementPositionY  = rowInfo[21]
     
    del rowInfo, nArrowLst, nArrow, scaleText, scaleBar, df, newExtent
  except Exception as e:
    pass

  return

# def fetchFGDB():
#     pass

def resetLayoutItems():
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df_lst = arcpy.mapping.ListLayoutElements(mxd, "DATAFRAME_ELEMENT")
    insetDF_lst = arcpy.mapping.ListDataFrames(mxd, "*Inset*")
    bottomMarginElems = [item0 for item0 in arcpy.mapping.ListLayoutElements(mxd) if (item0.elementPositionY >= 0.5 and item0.elementPositionY <  3.0)]
    topMarginElems = [item1 for item1 in arcpy.mapping.ListLayoutElements(mxd) if item1.elementPositionY > 69.0 and item1.elementPositionY <  72.0]
    lstTopBottomDF = df_lst + insetDF_lst + bottomMarginElems + topMarginElems
    outsideMarginElems = [item2 for item2 in arcpy.mapping.ListLayoutElements(mxd) if item2 not in lstTopBottomDF]

    # Reset index data frames.
    for index, inset in enumerate(insetDF_lst):
        inset.elementPositionX = -5.0
        inset.elementPositionY = 0.0 + (inset.elementHeight * int(index)) + (int(index) * 0.5)
        inset.elementHeight = 4.0
        inset.elementWidth = 4.0
        for i, elem in enumerate(outsideMarginElems):
            if hasattr(elem, 'parentDataFrameName'):
                if elem.parentDataFrameName == inset.name:
                    elem.elementPositionX = inset.elementPositionX - 3.0
                    elem.elementPositionY = inset.elementPositionY + (inset.elementHeight / 2)

    # Move SVA box and items off the page.
    svaLst = arcpy.mapping.ListLayoutElements(mxd, wildcard="*SVA*")
    for item in svaLst:
        item.elementPositionX = mxd.pageSize[0] + 2.0
        item.elementPositionY = 5.0

def svaBoxAdjust():
    # Author: James Stephaniuk
    # October 19, 2015
    #
    # Populates and aligns a graphic box with data from an shapefile attribute table.

    mxd = arcpy.mapping.MapDocument("CURRENT")
    ddp = mxd.dataDrivenPages
    pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # e.g. VMP
    pageNameField = ddp.pageNameField.name # edabbr

    # Feature class name.
    mapLyr = arcpy.mapping.ListLayers(mxd,"SVAs")[0]

    # SVA container (graphic box) name. Match this name to the SVA Box element name in ArcMap.
    svaBox = "svaBox"

    # Graphic box layout settings.
    padding = 0.2 # Distance (in inches) around edge of box to inner elements.
    spacer = 0.1  # Distance (in inches) between inner elements.

    # SVA source feature class field names. Add the field names from the layer that you want to populate the SVA Table.
    svaTxtField  = "va"
    facilityName = "sectname"
    addrNo       = "bldgstart"
    addrName     = "stdaddr"
    city         = "city_1"
    fieldLst = [svaTxtField, facilityName, addrNo, addrName, city]

    # SVA text element names. Match these names to the element names in ArcMap.
    SVATitleText  = "SVATitle"
    svaTitleElem0 = "SVA_TitleElem0"
    svaTitleElem1 = "SVA_TitleElem1"
    svaTitleElem2 = "SVA_TitleElem2"
    svaTitleElem3 = "SVA_TitleElem3"
    svaTxtElem0   = "SVA_textElem0"
    svaTxtElem1   = "SVA_textElem1"
    svaTxtElem2   = "SVA_textElem2"
    svaTxtElem3   = "SVA_textElem3"

    mainTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", SVATitleText)[0]
    svaTitle      = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem0)[0]
    facTitle      = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem1)[0]
    addrTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem2)[0]
    cityTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem3)[0]
    svaTxtElem    = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem0)[0]
    facTxtElem    = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem1)[0]
    addrTxtElem   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem2)[0]
    cityTxtElem   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem3)[0]

    elemLst = [svaTxtElem, facTxtElem, addrTxtElem, cityTxtElem]

    # Captions cannot be empty therefore a single char. Set all font sizes to same.
    for elem in elemLst:
        elem.text = " "

    # Populate columns.
    whereClause = "ed = "+ "'" + pageName + "'"
    rows = sorted(arcpy.da.SearchCursor(mapLyr.dataSource, fieldLst, whereClause))

    for row in rows:
        svaTxtElem.text  += "{}\n".format(row[0])
        facTxtElem.text  += "{}\n".format(row[1])
        addrTxtElem.text += "{} ".format(row[2])
        addrTxtElem.text += "{}\n".format(row[3])
        cityTxtElem.text += "{}\n".format(row[4])

    # Slice off leading space char.
    for elem in elemLst:
        elem.text = elem.text[1:]
        elem.text = '\n'.join(' '.join(line.split()) for line in elem.text.split('\n')) # Removes two or more spaces. Splits text into lines. Then splits each line by whitespace and rejoins with single spaces. Then rejoins the lines.

    svaBox = arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", svaBox)[0]

    # Position main title elem.
    mainTitle.elementPositionX = svaBox.elementPositionX + padding
    mainTitle.elementPositionY = svaBox.elementPositionY - padding

    # Position the titles and text elements relative to main title and each other.
    # Col 1
    widthCol1 = max(svaTitle.elementWidth, svaTxtElem.elementWidth) 
    svaTitle.elementPositionX = svaTxtElem.elementPositionX = mainTitle.elementPositionX
    svaTitle.elementPositionY = mainTitle.elementPositionY - svaTitle.elementHeight - padding # Uses padding instead of spacer to give main title more room.
    svaTxtElem.elementPositionY = svaTitle.elementPositionY - svaTitle.elementHeight
    # Col 2
    widthCol2 = max(facTitle.elementWidth, facTxtElem.elementWidth)
    facTitle.elementPositionY = svaTitle.elementPositionY
    facTxtElem.elementPositionY = svaTxtElem.elementPositionY
    facTitle.elementPositionX = svaTitle.elementPositionX + widthCol1 + spacer
    facTxtElem.elementPositionX = svaTxtElem.elementPositionX + widthCol1 + spacer
    # Col 3
    widthCol3 = max(addrTitle.elementWidth, addrTxtElem.elementWidth)
    addrTitle.elementPositionY = facTitle.elementPositionY
    addrTxtElem.elementPositionY = facTxtElem.elementPositionY
    addrTitle.elementPositionX = facTitle.elementPositionX + widthCol2 + spacer
    addrTxtElem.elementPositionX = facTxtElem.elementPositionX + widthCol2 + spacer
    # Col 4
    widthCol4 = max(cityTitle.elementWidth, cityTxtElem.elementWidth)
    cityTitle.elementPositionY = addrTitle.elementPositionY
    cityTxtElem.elementPositionY = addrTxtElem.elementPositionY
    cityTitle.elementPositionX = addrTitle.elementPositionX + widthCol3 + spacer
    cityTxtElem.elementPositionX = addrTxtElem.elementPositionX + widthCol3 + spacer

    # Set the svaBox height and width derived from text elements heights and widths.
    tallestTxtElem = max(svaTxtElem.elementHeight, facTxtElem.elementHeight, addrTxtElem.elementHeight, cityTxtElem.elementHeight)
    tallestTitleElem = max(svaTitle.elementHeight, facTitle.elementHeight, addrTitle.elementHeight, cityTitle.elementHeight)
    colsWidths = widthCol1 + widthCol2 + widthCol3 + widthCol4
    textWidth = colsWidths + (spacer * 3)
    svaBox.elementHeight = tallestTxtElem + tallestTitleElem + mainTitle.elementHeight + (padding * 2) + spacer # Height of all elements, spacers, and padding.
    svaBox.elementWidth = max(textWidth, mainTitle.elementWidth) + (padding * 2) # Width of all elements, spacers, and padding.

    # Centre the main title.
    if mainTitle.elementWidth > textWidth:
        mainTitle.elementPositionX = svaTxtElem.elementPositionX
    else:
        mainTitle.elementPositionX = svaTxtElem.elementPositionX + (textWidth / 2) - (mainTitle.elementWidth / 2 )

    # Contrived way to remove duplicates from SVA text column. If you have a better way I'd like to see it.
    splitLst = svaTxtElem.text.split()
    setSplititLst = list(set(svaTxtElem.text.split()))
    for i, item in enumerate(splitLst):
        if item in setSplititLst:
            setSplititLst.remove(item)
        else:
            splitLst[i] =  splitLst[i].replace(splitLst[i], len(splitLst[i]) * " ")
    joinedText = "\n".join(splitLst)
    svaTxtElem.text = joinedText

###################### End Function Definitions #############################

class DDP_Layout(object):
    """Implementation for Add_Ins_addin.DDPLayoutExt (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = False
    def openDocument (self):
        # Reference MXD
        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        pageNameField = ddp.pageNameField.name # edabbr
        #Reference pageLayoutTable
        pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0]

        pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
        pageLayoutRow = pageLayoutCursor.next()
        
        # Call arrangeDFs function for each dataframe.
        for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
            arrangeDFs(pageLayoutRow, dfIndex, df.name)

        return
        
    def pageIndexExtentChanged(self, new_id):
        # Reference MXD
        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        pageNameField = ddp.pageNameField.name # edabbr
        #Reference pageLayoutTable
        pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0]

        pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
        pageLayoutRow = pageLayoutCursor.next()
        
        # Call arrangeDFs function for each dataframe.
        for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
            arrangeDFs(pageLayoutRow, dfIndex, df.name)

        return

class LoadFGDBs(object):
    """Implementation for Add_Ins_addin.loadFGDBs (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # fetchFGDB()

        def fetchFGDB(df, baseDirectory, dfName):
            """Function to retrieve annotation file geodatabase for current ddp enabled map.\n
            Args:
              df (DataFrame object): A variable that references a DataFrame object.\n
              dfName (String): Name of data frame to locate folder containing file geodatabases.\n

            Returns:
              None: Returns NoneType.

            """
            try:
              # dfScale = int(round(df.scale))
              arcpy.env.workspace = os.path.join(baseDirectory, dfName + " Anno GDBs")
              targetGDB = arcpy.ListFiles("*" + pageName + "*" )[0] # + str(dfScale) + "*" ### Only list files that contain current edabbr and end in dataframe's scale.
              workspace = os.path.join(arcpy.env.workspace, targetGDB) 
              for (dirpath, dirnames, filenames) in arcpy.da.Walk(workspace):
                  for filename in filenames: 
                    annoPath = os.path.join(workspace,filename) 
                    temp_layer = "ANNO_" + filename # name of anno layer e.g. CanadaP_In_1100000.
                    arcpy.MakeFeatureLayer_management(annoPath, temp_layer)
                    annoLyr = arcpy.mapping.Layer(temp_layer)
                    target_group = arcpy.mapping.ListLayers(mxd, "Anno*", df)[0]
                    arcpy.mapping.AddLayerToGroup(df, target_group, annoLyr, "TOP") 
                    # del temp_layer
              return None
            except Exception as e:
              print e


        ########################################################################################

        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # E.g. ABM
        pageNameField = ddp.pageNameField.name # edabbr
        dfLst = arcpy.mapping.ListDataFrames(mxd)

        baseDir = False
        while baseDir == False: 
            baseDir = pythonaddins.OpenDialog("Select Path to Annotation FGDB", False, r"P:\15030_32_EBC_Digital_Mapping\MapData\2015 By Election Data\Anno GDBs", "Select")

        # Environment settings.
        arcpy.env.overwriteOutput = True
        arcpy.env.addOutputsToMap = False

        annoGroups = arcpy.mapping.ListLayers(mxd, "*anno*")
        # Clear contents from annotation group layers for each dataframe.
        for df in dfLst:
          for group in annoGroups:
            name = group.name
            for lyr in group:
                arcpy.mapping.RemoveLayer(df,lyr)

        try:
            # Execute fetchFGDB on each data frame.
            for df in dfLst:
                fetchFGDB(df, baseDir, df.name)
        except Exception as e:
            pythonaddins.MessageBox(e, "Error Message")
            print e

class RecordLayout(object):
    """Implementation for Add_Ins_addin.recordLayout (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

        def setDF(dfIndex, df):
          """Function used to create a list of a data frame's position, dimensions, extent, scale, rotation, north arrow height/position, and scale text/bar height/position. Scale is rounded to nearest 100."""
          nArrowLst = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*North*") + arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", "*north*")
          northArrow = nArrowLst[dfIndex]
          scaleText = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale Text*")[dfIndex]
          scaleBar = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale Bar*")[dfIndex]
          fieldValue = "[" + \
                       str(round(df.elementPositionX, 3)) +         "," + str(round(df.elementPositionY, 3)) +         "," + \
                       str(df.elementWidth) +                       "," + str(df.elementHeight) +                      "," + \
                       str(df.extent.XMin) +                        "," + str(df.extent.YMin) +                        "," + \
                       str(df.extent.XMax) +                        "," + str(df.extent.YMax) +                        "," + \
                       str(int(round(df.scale / 50.0) * 50.0)) +    "," + str(round(df.rotation, 2)) +                 "," + \
                       str(northArrow.elementWidth) +               "," + str(northArrow.elementHeight) +              "," + \
                       str(round(northArrow.elementPositionX, 3)) + "," + str(round(northArrow.elementPositionY, 3)) + "," + \
                       str(scaleText.elementWidth) +                "," + str(scaleText.elementHeight) +               "," + \
                       str(round(scaleText.elementPositionX, 3)) +  "," + str(round(scaleText.elementPositionY, 3)) +  "," + \
                       str(scaleBar.elementWidth) +                 "," + str(scaleBar.elementHeight) +                "," + \
                       str(round(scaleBar.elementPositionX, 3)) +   "," + str(round(scaleBar.elementPositionY, 3)) +   "]" 
          return fieldValue
            
          ##################################################################################


        #Reference mxd, ddp objects.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # E.g. ABM
        pageNameField = ddp.pageNameField.name # edabbr

        # Assign a unique to each element of the MXD.
        # mxd = arcpy.mapping.ListLayoutElements(mxd)
        # for index, elem in enumerate(layoutElems):
        #   elem.name = str(index)

        confirm = pythonaddins.MessageBox('Are you sure you want to save the page layout?\nPrevious data will be lost','Save Layout Confirmation', 4)
        if confirm == 'Yes':
          #Reference pagelayout table
          pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0] # P.L.E.
          #Update information from pagelayout table
          pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
          pageLayoutRow = pageLayoutCursor.next()

          if pageLayoutRow == None:               #INSERT A NEW ROW - INSERT CURSOR
            pageInsertCursor = arcpy.InsertCursor(pageLayoutTable.dataSource)
            pageInsertRow = pageInsertCursor.newRow()
            pageInsertRow.edabbr = pageName

            #Set Data Frame information
            for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
              # if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0]) and (df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):  #don't set values if DF is off the page
                pageInsertRow.setValue(df.name, setDF(dfIndex, df)) # Data frame name must match P.L.E. column name in order to write to it.
                 
            pageInsertCursor.insertRow(pageInsertRow)
            del pageInsertCursor, pageInsertRow

          else:                                   #UPDATE EXISTING ROW - UPDATE CURSOR
            pageUpdateCursor = arcpy.UpdateCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
            pageUpdateRow = pageUpdateCursor.next()

            #Set Data Frame information
            for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
              # if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0]) and (df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):  #don't set values if DF is off the page
                pageUpdateRow.setValue(df.name, setDF(dfIndex, df)) # Data frame name must match P.L.E. column name in order to write to it.
                       
            
            pageUpdateCursor.updateRow(pageUpdateRow)
            del pageUpdateCursor, pageUpdateRow
            
          arcpy.RefreshCatalog(pageLayoutTable.dataSource)
          del pageLayoutCursor, pageLayoutRow

class ResetLayout(object):
    """Implementation for Add_Ins_addin.resetLayout (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        resetLayoutItems()

class RestoreLayout(object):
    """Implementation for Add_Ins_addin.restoreLayout (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Reference MXD
        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        pageNameField = ddp.pageNameField.name # edabbr
        #Reference pageLayoutTable
        pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0]

        # Reset all data frames and layout elements.
        # reset = ResetLayout()
        # reset.onClick()

        pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
        pageLayoutRow = pageLayoutCursor.next()
        for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
          arrangeDFs(pageLayoutRow, dfIndex, df.name)

        arcpy.RefreshActiveView()

class SVABoxLayout(object):
    """Implementation for Add_Ins_addin.svaBoxLayout (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        svaBoxAdjust()
        arcpy.RefreshActiveView()

class SVABoxExtenstion(object):
    """Implementation for Add_Ins_addin.svaBoxExt (Extension)"""
    def __init__(self):
        self.enabled = False
    def pageIndexExtentChanged(self, new_id):
        svaBoxAdjust()
