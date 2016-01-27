import arcpy
import itertools
import os
import pythonaddins

mxd = arcpy.mapping.MapDocument("CURRENT")
# List of drives to cycle between.
drives = [r"P:\15030_32_EBC_Digital_Mapping\Utilities\Scripts\Python\Replication\Replicated_P.gdb", \
            r"C:\Users\jastepha\Desktop\testrep\Replicated_P.gdb"]
# Function to cycle drive list.
cycleDrives = itertools.cycle(drives).next

class ToggleDataSource(object):
    """Implementation for Cycle_Drives_addin.toggleDataSource (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = cycleDrives()
        # Replace sources in MXD. Validate set to True: workspace will only be updated if the 'replace workspace path' value is valid.
        mxd.findAndReplaceWorkspacePaths("",path, True)

        print "Resourced to {}".format(path)

        # Testing. Prints out all layer data source paths.
        # for lyr in arcpy.mapping.ListLayers(mxd):
        #     if lyr.supports("DATASOURCE"):
        #         print lyr.dataSource