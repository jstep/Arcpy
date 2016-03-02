#############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2015 James Stephaniuk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#############################################################################
# Usage: Run this script from the command line.
# Navigate to this script's folder in the command line and type:
# python [script name] "[mxd path]".
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


def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes",   "y": "yes",  "ye": "yes",
             "no": "no",     "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def removeFGDBs(ws):
    """Remove existing FGDB(s) in workspace."""
    for gdb in arcpy.ListFiles("*.gdb"):
        gdb_path = os.path.join(ws, gdb)
        shutil.rmtree(gdb_path)


def createFGDBs(onMapDFs, workspace):
    """Create FGDB(s) to store annotation for each dataframe."""
    for df in onMapDFs:
        fgdb = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, df.name, str(int(round(df.scale)))))
        if os.path.exists(fgdb):
            shutil.rmtree(fgdb)
        arcpy.CreateFileGDB_management(workspace, "{}_{}_{}".format(pageName, df.name, str(int(round(df.scale)))), "CURRENT")
        log.info("FGDB created: {}".format(fgdb))


def createExtentBoxes(mxdPath):
    try:
        # Restore Page Layout (from PageLayoutElements table) before running this script.
        mxd = arcpy.mapping.MapDocument(mxdPath)
        ddp = mxd.dataDrivenPages
        pageName = str(ddp.pageRow.getValue(ddp.pageNameField.name))
        df_lst = arcpy.mapping.ListDataFrames(mxd)

        # Set the main dataframe variable.
        try:
            MDF = arcpy.mapping.ListDataFrames(mxd, "MDF")[0]
        except IndexError:
            MDF = arcpy.mapping.ListDataFrames(mxd)[0]

        log.info("MXD path: {}".format(mxd.filePath))
        log.info("Page Name: {}".format(pageName))

        onMapDFs = []
        # List of data frames on the current page.
        for df in df_lst:
            if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
                onMapDFs.append(df)

        feature_info = []

        XMin = MDF.extent.XMin
        YMin = MDF.extent.YMin
        XMax = MDF.extent.XMax
        YMax = MDF.extent.YMax
        # A list of features and coordinate pairs
        df_info = [[XMin, YMin], [XMax, YMin], [XMax, YMax], [XMin, YMax]]
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

        removeFGDBs(workspace)
        createFGDBs(onMapDFs, workspace)

        del coords, feature_info, features, feature, poly_filename, outDir, mxd, df_info, XMax, XMin, YMax, YMin, ddp, pageName
    except Exception as e:
        log.info("An error occured: {}".format(e))


def generateTiledAnno(mxdPath):
    mxd = arcpy.mapping.MapDocument(mxdPath)
    ddp = mxd.dataDrivenPages
    pageName = str(ddp.pageRow.getValue(ddp.pageNameField.name))
    df_lst = arcpy.mapping.ListDataFrames(mxd)

    # List of data frames on the current page.
    onMapDFs = []
    for df in df_lst:
        if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0] and df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):
            onMapDFs.append(df)

    parentDir = os.path.abspath(os.path.join(os.path.dirname(mxd.filePath), os.pardir))
    workspace = arcpy.env.workspace = os.path.join(parentDir, pageName, "anno_fgdb")

    indexFC = arcpy.ListFeatureClasses("DF_Polygons*")[0]
    tileIndexPoly = os.path.join(workspace, indexFC)
    GroupAnno = "GroupAnno"
    anno_suffix = "Anno"

    for df in onMapDFs:
        # arcpy.activeView = df.name
        try:
            fgdb = os.path.join(workspace, "{}_{}_{}.gdb".format(pageName, str(df.name), int(round(df.scale))))
            if os.path.exists(fgdb):
                arcpy.TiledLabelsToAnnotation_cartography(
                    mxd.filePath,
                    str(df.name),
                    str(tileIndexPoly),
                    fgdb,
                    GroupAnno + str(df.name) + "_",
                    anno_suffix,
                    round(df.scale),
                    feature_linked="STANDARD",
                    generate_unplaced_annotation="NOT_GENERATE_UNPLACED_ANNOTATION")
                log.info("Tiled Annotation Created at {}".format(fgdb))
            else:
                log.info("{} DOES NOT EXIST".format(fgdb))

        except Exception as e:
            log.info(e)


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
    return str(pageName)

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
    logName = os.path.join(logPath, (getpass.getuser() + now.strftime("_%Y-%m-%d_%H-%M.log")))

    log = logging.getLogger("script_log")
    log.setLevel(logging.INFO)

    h1 = logging.FileHandler(logName)
    h2 = logging.StreamHandler()

    f = logging.Formatter("[%(levelname)s] [%(asctime)s] [%(lineno)d] - %(message)s", '%m/%d/%Y %I:%M:%S %p')

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
        confirm = query_yes_no("Are you sure you want to create new annotation? Existing FGDB(s) will be overwritten.")

        if confirm.lower() in ("y", "ye", "yes"):
            createExtentBoxes(mxd)
            generateTiledAnno(mxd)

    except Exception as e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')
