import arcpy
import datetime
import logging
import logging.handlers
import os
import shutil
import sys
import time

########################### User defined functions ###########################

def exporter(mxdPath, user_dpi, edabbr):
    log = logging.getLogger("script_log")
    try:
        mxd = arcpy.mapping.MapDocument(mxdPath)
        dpi = user_dpi
        colorspace = "CMYK"
        ddp = mxd.dataDrivenPages
        pageName = edabbr
        pageID = ddp.getPageIDFromName(edabbr)
        ddp.currentPageID = pageID

        outDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PDF")
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        log.info("outDir variable set to {}".format(outDir))

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
        log.info("MXD page size: {}x{}. Orient set to: {}".format(mxd.pageSize.width, mxd.pageSize.height, orient))

        # Join output directory with formatted file name.
        PathOut = os.path.join(outDir,"{}_{}_{}_{}".format(pageName,str(dpi),colorspace,orient))
        log.info("PDF saved to: {}".format(PathOut))

        # Export
        arcpy.mapping.ExportToPDF(mxd, PathOut, resolution=dpi,image_quality="BEST",colorspace=colorspace, convert_markers=True)

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
    user_edabbr = sys.argv[3]

    # Log files folder will be created at same directory level as script. 
    logPath = os.path.join(os.path.dirname(mxd), "Logfiles-PDF_Export")
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # Make a global logging object.
    logName = os.path.join(logPath,(now.strftime("%Y-%m-%d_%H-%M.log")))

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
        exporter(mxd, user_dpi, user_edabbr)

    except Exception as e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')