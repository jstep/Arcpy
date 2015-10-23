import arcpy
import pythonaddins
import os

def exporter(colorspace, dpi):
    try:
        mxd = arcpy.mapping.MapDocument('CURRENT')
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)

        outDir = pythonaddins.OpenDialog("Path to PDF output", False, os.path.dirname(mxd.filePath), "Select Folder")
        if not outDir:
            outDir = os.path.dirname(mxd.filePath)

        # Logic to determine orientation of page.
        if mxd.pageSize.width == 72.0 and mxd.pageSize.height == 72.0:
            orient = "4sheet"
        elif mxd.pageSize.width == 36.0 and mxd.pageSize.height == 36.0:
            orient = "1sheet"
        elif mxd.pageSize.width == 72.0 and mxd.pageSize.height == 36.0:
            orient = "2sheet_horizontal"
        elif mxd.pageSize.width == 36.0 and mxd.pageSize.height == 72.0:
            orient = "2sheet_vertical"
        else :
            orient = "{}x{}".format(str(mxd.pageSize[0]), str(mxd.pageSize[1]))

        # Join output directory with formatted file name.
        PDFOut = os.path.join(outDir,"{}_{}_{}_{}".format(pageName,str(dpi),colorspace,orient))
        # PDF Export
        arcpy.mapping.ExportToPDF(mxd, PDFOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)

        pythonaddins.MessageBox("PDF saved to \n{}\n as\n {}".format(outDir, os.path.split(PDFOut)[1]),"PDF Save Location")

        del mxd, ddp, pageName, outDir, orient, dpi, colorspace
    except Exception as e:
        pythonaddins.MessageBox(e, "Error Message")
        print e


###############################################################################################################################

# Button Classes.

class CMYK288(object):
    """Implementation for PDF_Export_Addin_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("CMYK", 144)

class RGB144(object):
    """Implementation for PDF_Export_Addin_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("RGB", 144)
        