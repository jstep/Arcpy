import arcpy
import datetime
import getpass
import logging
import logging.handlers
import os
import shutil
import sys
import time

########################### User defined functions ###########################

def exporter(mxdPath, user_dpi):
    log = logging.getLogger("script_log")
    try:
        mxd = arcpy.mapping.MapDocument(mxdPath)
        dpi = user_dpi
        colorspace = "CMYK"
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        
        log.info("MXD path: {}".format(mxd.filePath))
        log.info("DPI: {}".format(str(dpi)))
        log.info("Colorspace: {}".format(colorspace))
        log.info("Page Name: {}".format(pageName))

        curDirPath = os.path.dirname(mxd.filePath)
        parDirPath = os.path.abspath(os.path.join(curDirPath, os.pardir))
        outDir = os.path.join(parDirPath, "PDF_Draft_Exports")
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        log.info("Output directory set to {}".format(outDir))

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
        
        log.info("MXD page size: {} x {}. Orient set to: {}".format(mxd.pageSize.width, mxd.pageSize.height, orient))

        # Join output directory with formatted file name.
        PathOut = os.path.join(outDir,"{}_{}_{}_{}".format(pageName,str(dpi),colorspace,orient))
        
        # Export
        log.info("")
        log.info("PDF being created...")
        arcpy.mapping.ExportToPDF(mxd, PathOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)
        log.info("PDF saved to: {}".format(PathOut))
        
        del mxd, ddp, pageName, outDir, orient, dpi, colorspace
    except Exception as e:
        log.info("An error occured: {}".format(e))


def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    if minutes >= 60:
        hours, minutes_rem = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes_rem, seconds_rem)
    else:
        minutes, seconds_rem = divmod(x, 60)
        return "00:%02d:%02d" % (minutes, seconds_rem)


##############################################################################


if __name__ == "__main__":
    startTime = time.time()
    now = datetime.datetime.now()

############################ USER VARIABABLES ################################
    mxd = sys.argv[1]
    user_dpi = sys.argv[2]

    # Log files folder will be created in the pdf folder one level up. 
    curDirPath = os.path.dirname(mxd)
    parDirPath = os.path.abspath(os.path.join(curDirPath, os.pardir))
    logPath = os.path.join(parDirPath, "Logfiles-PDF_Export")
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # Make a global logging object.
    logName = os.path.join(logPath,(getpass.getuser() + now.strftime("_%Y-%m-%d_%H-%M.log")) )

    log = logging.getLogger("script_log")
    log.setLevel(logging.INFO)

    h1 = logging.FileHandler(logName)
    h2 = logging.StreamHandler()

    f = logging.Formatter("[%(levelname)s] [%(asctime)s] [%(lineno)d] - %(message)s",'%m/%d/%Y %I:%M:%S %p')

    h1.setFormatter(f)
    h2.setFormatter(f)

    h1.setLevel(logging.INFO)
    h2.setLevel(logging.INFO)

    log.addHandler(h1)
    log.addHandler(h2)

    log.info('----------------------------------------------------')
    log.info('Script: {0}'.format(os.path.basename(sys.argv[0])))
    log.info('----------------------------------------------------')

    try:
        ########################### Function calls ###########################
        exporter(mxd, user_dpi)

    except Exception as e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')