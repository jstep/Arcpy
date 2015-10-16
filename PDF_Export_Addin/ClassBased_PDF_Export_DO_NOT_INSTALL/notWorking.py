import arcpy
import pythonaddins
import os

class Helper(object):
	def exporter(self, colorspace, dpi, outDir):
	    """Helper function for PDF_Export_addin buttons"""
	    
	    mxd = arcpy.mapping.MapDocument('CURRENT')
	    ddp = mxd.dataDrivenPages

	    dpi = dpi
	    outDir = outDir
	    colorspace = colorspace

	    pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
	    pageNameField = ddp.pageNameField.name # edabbr
	    # # Search Cursor for page name
	    # indexTable = ddp.indexLayer.dataSource
	    # sqlClause = "\"" + ddp.pageNameField.name + "\" = '" + pageName + "'"
	    # nameSearchCursor = arcpy.SearchCursor(indexTable, sqlClause)
	    # nameRow = nameSearchCursor.next()
	    # name = nameRow.getValue('edname')

	    # Logic to determine orientation of page.
	    if mxd.pageSize.width > mxd.pageSize.height:
	        orient = "L"
	    elif mxd.pageSize.width < mxd.pageSize.height:
	        orient = "P"
	    else:
	        orient = ""

	    # outDir = pythonaddins.OpenDialog("Path to PDF output", False, r"P:\15030 - Electoral Geography", "Select Folder")
	    outDir = r"C:\Users\jastepha\Desktop\tmp"
	    # Join output directory with formatted file name.
	    PDFOut = os.path.join(outDir,"{}_{}_{}_{}".format(pageName,str(dpi),colorspace,orient))
	    # PDF Export
	    arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)

	    del mxd, ddp, pageName, outDir, orient, dpi, colorspace
	    
    
class CMYK288dpi(object):
    """Implementation for PDF_Export_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        cmykHelperObj = Helper()
        cmykHelperObj.exporter("CMYK", 288, r"C:\Users\jastepha\Desktop\tmp")

class RGB144dpi(object):
    """Implementation for PDF_Export_addin.button_2 (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        rgbHelperObj = Helper()
        rgbHelperObj.exporter("RGB", 144, r"C:\Users\jastepha\Desktop\tmp")