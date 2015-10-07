import arcpy
import pythonaddins
import os

try:
    mxd = arcpy.mapping.MapDocument('CURRENT')
    ddp = mxd.dataDrivenPages
    dpi = arcpy.GetParameterAsText(0)
    colorspace = arcpy.GetParameterAsText(2)
    pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
    # Search Cursor for page name
    indexTable = ddp.indexLayer.dataSource
    sqlClause = "\"" + ddp.pageNameField.name + "\" = '" + pageName + "'"
    nameSearchCursor = arcpy.SearchCursor(indexTable, sqlClause)
    nameRow = nameSearchCursor.next()
    fieldName = arcpy.GetParameterAsText(1)
    name = nameRow.getValue(fieldName)

    # Logic to determine orientation of page.
    if mxd.pageSize.width > mxd.pageSize.height:
        orient = "L"
    elif mxd.pageSize.width < mxd.pageSize.height:
        orient = "P"
    else:
        orient = ""

    outDir = arcpy.GetParameterAsText(3)
    # Join output directory with formatted file name.
    PDFOut = os.path.join(outDir,"{}_{}_{}_{}_{}".format(name, pageName,str(dpi),colorspace,orient))
    # PDF Export
    arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)

    del mxd, ddp, pageName, outDir, orient, dpi, colorspace, indexTable, sqlClause, nameSearchCursor, nameRow, name
except AttributeError:
    pythonaddins.MessageBox("Data Driven Pages must be enabled for button to function", "DDP not enabled")
    