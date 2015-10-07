import arcpy
import pythonaddins
import os

class CMYK288dpi(object):
    """Implementation for PDF_Export_Addin_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        import arcpy
        try:
            mxd = arcpy.mapping.MapDocument('CURRENT')
            ddp = mxd.dataDrivenPages
            dpi = 288
            colorspace = "CMYK"
            pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
            # Search Cursor for page name
            indexTable = ddp.indexLayer.dataSource
            sqlClause = "\"" + ddp.pageNameField.name + "\" = '" + pageName + "'"
            nameSearchCursor = arcpy.SearchCursor(indexTable, sqlClause)
            nameRow = nameSearchCursor.next()
            name = nameRow.getValue('DIST_NAME')
    
            # Logic to determine orientation of page.
            if mxd.pageSize.width > mxd.pageSize.height:
                orient = "L"
            elif mxd.pageSize.width < mxd.pageSize.height:
                orient = "P"
            else:
                orient = ""
    
            outDir = pythonaddins.OpenDialog("Path to PDF output", False, r"P:\15030 - Electoral Geography", "Select Folder")
            # Join output directory with formatted file name.
            PDFOut = os.path.join(outDir,"{}_{}_{}_{}_{}".format(name, pageName,str(dpi),colorspace,orient))
            # PDF Export
            arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)
    
            del mxd, ddp, pageName, outDir, orient, dpi, colorspace, indexTable, sqlClause, nameSearchCursor, nameRow, name
        except AttributeError:
            pythonaddins.MessageBox("Data Driven Pages must be enabled for button to function", "DDP not enabled")

class RGB144dpi(object):
    """Implementation for PDF_Export_Addin_addin.button (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        import arcpy
        try:
            mxd = arcpy.mapping.MapDocument('CURRENT')
            ddp = mxd.dataDrivenPages
            dpi = 145
            colorspace = "RGB"
            pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
            # Search Cursor for page name
            indexTable = ddp.indexLayer.dataSource
            # sqlClause = '"District" = \'D#\''
            sqlClause = "\"" + ddp.pageNameField.name + "\" = '" + pageName + "'"
            nameSearchCursor = arcpy.SearchCursor(indexTable, sqlClause)
            nameRow = nameSearchCursor.next()
            name = nameRow.getValue('DIST_NAME')
    
            # Logic to determine orientation of page.
            if mxd.pageSize.width > mxd.pageSize.height:
                orient = "L"
            elif mxd.pageSize.width < mxd.pageSize.height:
                orient = "P"
            else:
                orient = ""
    
            outDir = pythonaddins.OpenDialog("Path to PDF output", False, r"P:\15030 - Electoral Geography", "Select Folder")
            # Join output directory with formatted file name.
            PDFOut = os.path.join(outDir,"{}_{}_{}_{}_{}".format(name, pageName,str(dpi),colorspace,orient))
            # PDF Export
            arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)
    
            del mxd, ddp, pageName, outDir, orient, dpi, colorspace, indexTable, sqlClause, nameSearchCursor, nameRow, name
        except AttributeError:
            pythonaddins.MessageBox("Data Driven Pages must be enabled for button to function", "DDP not enabled")