import arcpy
import os
import pythonaddins

def exporter(colorspace, dpi, fileType="PDF"):
    try:
        mxd = arcpy.mapping.MapDocument('CURRENT')
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)

        outDir = pythonaddins.OpenDialog("Path to output directory", False, os.path.dirname(mxd.filePath), "Select Folder")
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
        PathOut = os.path.join(outDir,"{}_{}_{}_{}".format(pageName,str(dpi),colorspace,orient))
        # Export
        if fileType == "PDF":
            arcpy.mapping.ExportToPDF(mxd, PathOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)
        elif fileType == "PNG":
            arcpy.mapping.ExportToPNG(mxd, PathOut, resolution=dpi,color_mode=colorspace)

        pythonaddins.MessageBox("Saved to \n{}\n as\n {}".format(outDir, os.path.split(PathOut)[1]),"Save Location")

        del mxd, ddp, pageName, outDir, orient, dpi, colorspace
    except Exception as e:
        pythonaddins.MessageBox(e, "Error Message")
        print e


class CMYK288(object):
    """Implementation for PDF_Export_Addin_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("CMYK", 144)


class PNG_Draft(object):
    """Implementation for PDF_Export_Addin_addin.pngDraft (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        exporter("24-BIT_TRUE_COLOR", 1152, "PNG")

class RGB144(object):
    """Implementation for PDF_Export_Addin_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("RGB", 144)