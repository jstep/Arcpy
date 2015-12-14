import arcpy
import os
import pythonaddins

def exporter(colorspace, dpi):
    try:
        mxd = arcpy.mapping.MapDocument('CURRENT')
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)

        curDirPath = os.path.dirname(mxd.filePath)
        parDirPath = os.path.abspath(os.path.join(curDirPath, os.pardir))
        outDir = os.path.join(parDirPath, pageName, "PDF_Draft_Exports")
        if not os.path.exists(outDir):
            os.makedirs(outDir)

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
        
        # Export.
        arcpy.mapping.ExportToPDF(mxd, PathOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)

        pythonaddins.MessageBox("Saved to \n{}\n as\n {}".format(outDir, os.path.split(PathOut)[1]),"Save Location")

        del mxd, ddp, pageName, outDir, orient, dpi, colorspace
    except Exception as e:
        pythonaddins.MessageBox(e, "Error Message")
        print e
class CMYK(object):
    """Implementation for PDF_Export_Addin_addin.cmyk (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("CMYK", 144)

class RGB(object):
    """Implementation for PDF_Export_Addin_addin.rgb (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Call to exporter function.
        exporter("RGB", 144)