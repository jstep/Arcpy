import arcpy
import pythonaddins

class PDF_Export(object):
    """Implementation for PDF_Export_Addin_addin.button_2 (Button)"""
    def __init__(self, colorspace, dpi, outDir):
        self.enabled = False
        self.checked = False
        self.colorspace = colorspace
        self.dpi = dpi
        self.outDir = outDir
    def onClick(self):
        import arcpy
        mxd = arcpy.mapping.MapDocument('CURRENT')
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        # Search Cursor for page name
        indexTable = indexTable = ddp.indexLayer.dataSource
        sqlClause = "\"District\" = '" + pageName + "'"
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
        PDFOut = self.outDir + name + "_" + pageName + "_" + str(self.dpi) + self.colorspace + "_" + orient
        # PDF Export
        arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=self.dpi,image_quality="BEST",colorspace=self.colorspace, convert_markers=True)
        # Delete variables
        del mxd, ddp, pageName, self.outDir, orient, self.dpi, self.colorspace, indexTable, sqlClause, nameSearchCursor, nameRow, name

class CMYK288dpi(object):
    """Implementation for ClassBased_PDF_Export_addin.CMYK288dpi (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Get an instance of the PDF_Export class.
        pdf_export =  PDF_Export("CMYK", 288, r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\PDF_prelim_Report_288CMYK\Proofing\\")
        # Call onClick method.
        pdf_export.onClick()

class RGB144dpi(object):
    """Implementation for ClassBased_PDF_Export_addin.RGB144dpi (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Get an instance of the PDF_Export class.
        pdf_export =  PDF_Export("RGB", 144, r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\PDF_prelim_Report_144RGB\\")
        # Call onClick method.
        pdf_export.onClick()

class RGB72dpi(object):
    """Implementation for ClassBased_PDF_Export_addin.RGB72dpi (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Get an instance of the PDF_Export class.
        pdf_export =  PDF_Export("RGB", 72, r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\PDF_prelim_Report_72RGB\\")
        # Call onClick method.
        pdf_export.onClick()