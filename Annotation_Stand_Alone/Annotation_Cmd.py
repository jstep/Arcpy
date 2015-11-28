#############################################################################
#
# Author: James Stephaniuk
#
# Date: November 25, 2015
#
# Usage: Run this script from the command line.             
# Navigate to this script's folder in the command line and type:
# python [script name] "[mxd path]"
#
##############################################################################

import arcpy
import datetime
import getpass
import glob
import logging
import logging.handlers
import os
import shutil
import sys
import time


def createExtentBoxes(mxdPath):
    try:
        # Restore Page Layout (from PageLayoutElements table) before running this script.
        mxd = arcpy.mapping.MapDocument(mxdPath)
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        df_lst = arcpy.mapping.ListDataFrames(mxd)

        log.info("MXD path: {}".format(mxd.filePath))
        log.info("Page Name: {}".format(pageName))


        onMapDFs = []
        # List of data frames on the current page.
        for df in df_lst:
            if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
                onMapDFs.append(df)

        feature_info = []
        for df in onMapDFs:
            # Only creates geometry for data frames on the page. Also creates FGDB.
            XMin = df.extent.XMin 
            YMin = df.extent.YMin 
            XMax = df.extent.XMax 
            YMax = df.extent.YMax 
            # A list of features and coordinate pairs
            df_info = [[XMin, YMin],[XMax, YMin],[XMax, YMax],[XMin, YMax]]
            feature_info.append(df_info)

        # A list that will hold each of the Polygon objects
        features = []
        for feature in feature_info:
            # Create a Polygon object based on the array of points
            # Append to the list of Polygon objects
            features.append(arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in feature])))
            

        # Persist a copy of the Polygon objects using CopyFeatures
        poly_filename = "DF_Polygons_{}".format(pageName)
        parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
        edDir = os.path.join(parentDir, pageName)
        outDir = os.path.join(edDir, "anno_fgdb")
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        workspace = arcpy.env.workspace = outDir
        log.info("Output directory set to {}".format(outDir))

        poly_shp = os.path.join(workspace, poly_filename)
        for filename in glob.glob(poly_shp + "*"):
            os.remove(filename)

        arcpy.CopyFeatures_management(features, poly_filename)
        log.info("'{}' saved to: {}".format(poly_filename, outDir))

        # Create FGDB(s).
        for df in onMapDFs:
            fgdb = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, df.name, str(int(round(df.scale)))))
            if os.path.exists(fgdb):
                shutil.rmtree(fgdb)
            arcpy.CreateFileGDB_management(workspace, "{}_{}_{}".format(pageName, df.name, str(int(round(df.scale)))), "CURRENT")
            log.info("FGDB created: {}".format(fgdb))

        mxd.save()

        del coords, feature_info, features, feature, poly_filename, outDir, mxd, df_lst, df_info, df, XMax, XMin, YMax, YMin, ddp, pageName 
    except Exception as e:
        log.info("An error occured: {}".format(e))

def generateTiledAnno(mxdPath):

    mxd = arcpy.mapping.MapDocument(mxdPath)
    ddp = mxd.dataDrivenPages
    pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
    df_lst = arcpy.mapping.ListDataFrames(mxd)

    # TODO:
    # Switch on standard labels (from predefined list)
    # e.g.
    # layersToLabel = [
                # 'ED Boundary',
                # 'Indian Reserve',
                # 'Parks',
                # 'Roads Internal Left'
                # ]
                # etc...


    # List of data frames on the current page.
    onMapDFs = []
    for df in df_lst:
        if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
            onMapDFs.append(df)

    tileIndexPoly = arcpy.ListFeatureClasses("DF_Polygons*")[0]
    GroupAnno = "GroupAnno"
    anno_suffix = "Anno"
    
    parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
    workspace = arcpy.env.workspace = os.path.join(parentDir, "anno_fgdb")

    for df in onMapDFs:
        # arcpy.activeView = df.name
        try:
            fgdb = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, str(df.name), int(round(df.scale))))
            if os.path.exists(fgdb):
                arcpy.TiledLabelsToAnnotation_cartography(
                    mxd.filePath,
                    str(df.name),
                    tileIndexPoly,
                    fgdb,
                    GroupAnno + str(df.name) + "_",
                    anno_suffix,
                    round(df.scale),
                    feature_linked="STANDARD",
                    generate_unplaced_annotation="GENERATE_UNPLACED_ANNOTATION")
        except Exception as e:
            print e

    # Turn off all labels.
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("LABELCLASSES"):
            lyr.showLabels = False

    for df in df_lst:
        # Remove DF Polygons.
        for lyr in arcpy.mapping.ListLayers(mxd,"", df):
            if lyr.name.lower().startswith("df_polygons"):
                arcpy.mapping.RemoveLayer(df, lyr)

        # Remove empty annotation groups.
        groupLayers = [x for x in arcpy.mapping.ListLayers(mxd) if x.isGroupLayer and GroupAnno in x.name] 
        for group in groupLayers:
            count = 0
            for item in group:
                count += 1
            if count == 0:
                arcpy.mapping.RemoveLayer(df, group)

    mxd.save()

    # del anno_suffix, ddp, df, df_lst, fgdb, GroupAnno, lyr, mxd, onMapDFs, pageName, parentDir, tileIndexPoly, group, groupLayers, count

def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    if minutes >= 60:
        hours, minutes_rem = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes_rem, seconds_rem)
    else:
        minutes, seconds_rem = divmod(x, 60)
        return "00:%02d:%02d" % (minutes, seconds_rem)

def getPageName(mxdPath):
    mxd = arcpy.mapping.MapDocument(mxdPath)
    ddp = mxd.dataDrivenPages
    pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
    return pageName

##############################################################################

if __name__ == "__main__":
    startTime = time.time()
    now = datetime.datetime.now()

############################ USER VARIABABLES ################################
    mxd = sys.argv[1]

    pageName = getPageName(mxd)

    # Log files folder will be created in the ddp edabbr folder.
    curDirPath = os.path.dirname(mxd)
    parDirPath = os.path.abspath(os.path.join(curDirPath, os.pardir))
    logPath = os.path.join(parDirPath, pageName, "Logfiles-Anno")
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
        createExtentBoxes(mxd)
        generateTiledAnno(mxd)

    except Exception as e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')