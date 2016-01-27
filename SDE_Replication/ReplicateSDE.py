import arcpy
import datetime
import logging
import logging.handlers
import os
import shutil
import sys
import time

########################### User defined functions ###########################

def getDatabaseItemCount(workspace):
    log = logging.getLogger("script_log")
    """returns the item count in provided database"""
    arcpy.env.workspace = workspace
    feature_classes = []
    log.info("Compiling a list of items in {0} and getting count.".format(workspace))
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype="Any",type="Any"):
        for filename in filenames:
            feature_classes.append(os.path.join(dirpath, filename))
    log.info("There are a total of {0} items in the database".format(len(feature_classes)))
    return feature_classes, len(feature_classes)

def replicateDatabase(dbConnection, targetGDB):
    log = logging.getLogger("script_log")
    startTime = time.time()

    if arcpy.Exists(dbConnection):
        featSDE,cntSDE = getDatabaseItemCount(dbConnection)
        log.info("Geodatabase being copied: %s -- Feature Count: %s" %(dbConnection, cntSDE))
        if arcpy.Exists(targetGDB):
            # Archive old geodatabase with timestamp.
            # shutil.copytree(targetGDB, os.path.join(os.path.dirname(__file__), str(now.strftime("%Y-%m-%d_%H-%M.gdb")))) # TODO: Release Locking
            featGDB,cntGDB = getDatabaseItemCount(targetGDB) 
            log.info("Old Target Geodatabase: %s -- Feature Count: %s" %(targetGDB, cntGDB))
            try:
                shutil.rmtree(targetGDB)
                log.info("Deleted Old %s" %(os.path.split(targetGDB)[-1]))
            except Exception as e:
                log.info(e)

        GDB_Path, GDB_Name = os.path.split(targetGDB)
        log.info("Now Creating New %s" %(GDB_Name))
        arcpy.CreateFileGDB_management(GDB_Path, GDB_Name)

        arcpy.env.workspace = dbConnection

        # try:
        #     datasetList = [arcpy.Describe(a).name for a in arcpy.ListDatasets()]
        # except Exception as e:
        #     datasetList = []
        #     log.info(e)
        try:
            featureClasses = layerNameLst
        except Exception as e:
            featureClasses = []
            log.info(e)
        # try:
        #     tables = [arcpy.Describe(a).name for a in arcpy.ListTables()]
        # except Exception as e:
        #     tables = []
        #     log.info(e)

        #Compiles a list of the previous three lists to iterate over
        allDbData = featureClasses # + datasetList + tables

        for sourcePath in allDbData:
            targetName = sourcePath.split('.')[-1]
            targetPath = os.path.join(targetGDB, targetName)
            if not arcpy.Exists(targetPath):
                try:
                    log.info("Attempting to Copy %s to %s" %(targetName, targetPath))
                    arcpy.Copy_management(sourcePath, targetPath)
                    log.info("Finished copying %s to %s" %(targetName, targetPath))
                except Exception as e:
                    log.info("Unable to copy %s to %s" %(targetName, targetPath))
                    log.info(e)
            else:
                log.info("%s already exists....skipping....." %(targetName))

        featGDB,cntGDB = getDatabaseItemCount(targetGDB)
        log.info("Completed replication of %s -- Feature Count: %s" %(dbConnection, cntGDB))

    else:
        log.info("{0} does not exist or is not supported! \
        Please check the database path and try again.".format(dbConnection))

def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    if minutes >= 60:
        hours, minutes_rem = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes_rem, seconds_rem)
    else:
        minutes, seconds_rem = divmod(x, 60)
        return "00:%02d:%02d" % (minutes, seconds_rem)

################################# Layer List #################################
# Layer name list. Controls which features will be replicated.
layerNameLst = [
                'indea:mdwilkie.indea_bs10_covlines_view_active',
                'indea:mdwilkie.indea_background_ebc_greenspace_active',
                'indea:mdwilkie.indea_background_ebc_usa_poly_active',
                'indea:mdwilkie.indea_background_ebc_communities_active',
                'indea:genmaint.idm_ebc_roads',
                'indea:mdwilkie.indea_road_segments_active',
                'indea:mdwilkie.indea_background_ebc_railways_active',
                'indea:genmaint.idm_ebc_municipalities_ebc_indian_reserves',
                'indea:mdwilkie.indea_background_ebc_canada_poly_active',
                'indea:mdwilkie.indea_background_ebc_water_features_streams_active',
                'indea:mdwilkie.indea_background_ebc_water_features_areal_active',
                'indea:genmaint.cart_ebc_buildings',
                'indea:mdwilkie.indea_background_ebc_ocean_active',
                'indea:mdwilkie.indea_background_ebc_islands_active',
                'indea:mdwilkie.indea_background_ebc_parks_active',
                'indea:genmaint.cart_ebc_water_features_streams_tab',
                'indea:genmaint.indea_background_ebc_external_transparency_active'
                ]

if __name__ == "__main__":
    startTime = time.time()
    now = datetime.datetime.now()

    ############################# User variables #############################
    # Change this variable to the target database location (SDE connection).
    databaseConnection = "PATH_TO_YOUR_SDE_CONNECTION"

    # Log files folder will be created at same directory level as script. 
    logPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "replicateSDE_Logfiles")
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # Replicated FGDB will be created at same directory level as script.
    targetGDB = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Replicated.gdb")

    ############################## Logging items #############################

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

        replicateDatabase(databaseConnection, targetGDB)

        ######################################################################
    except Exception as e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')