import arcpy
import os
import pythonaddins
import sys

sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.
from autoPath import autoPath

class LayerHelper(object):
    """Implementation for Layers_addin.layerHelper_1 (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
    def pageIndexExtentChanged(self, new_id):
        RestoreLayers.onClick()

class ResetLayers(object):
    """Implementation for Layers_addin.resetLayers (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        parentDir = os.path.abspath(os.path.join(autoPath(), os.pardir))
        defaultLayersWorkspace = os.path.join(parentDir, "z_Default_Layers")
        arcpy.env.workspace = defaultLayersWorkspace
        mxd = arcpy.mapping.MapDocument("CURRENT")

        # Create Default Layers directory if none exists.
        if not os.path.exists(defaultLayersWorkspace):
            os.makedirs(defaultLayersWorkspace)
            pythonaddins.MessageBox("Default layers yet not created.\nRun createDefaultLyrs.py inside the interactive python window of this MXD.", "Layers Not Created", 0)

        # Load Default Layers.
        dfLst = arcpy.mapping.ListDataFrames(mxd)

        # Initialize empty lists for MessageBox.
        lyrsReset, lyrsNotReset = [], []

        # Iterate features and dataframes. Replace with default layer file. NOTE: Make sure feature class names are unique.
        for df in dfLst:
            for lyr in arcpy.mapping.ListLayers(mxd, "*", df):
                if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer:
                    lyrString = "default_%s.lyr" % (lyr.name)
                    if lyrString in arcpy.ListFiles("*.lyr"):
                        ref_layer = arcpy.mapping.ListLayers(mxd, lyr.name, df)[0]
                        insert_layer = arcpy.mapping.Layer("%s\\%s" % (defaultLayersWorkspace, lyrString))
                        arcpy.mapping.InsertLayer(df, ref_layer,insert_layer, "AFTER")
                        arcpy.mapping.RemoveLayer(df, ref_layer)
                        # Add swapped layers to list and show user with pythonaddins.MessageBox().
                        lyrsReset.append("{} - {}".format(lyrString, df.name))
                    else:
                        lyrsNotReset.append("{} - {}".format(lyrString, df.name))
        pythonaddins.MessageBox("Layers Reset:\n{} \n\nLayers NOT Reset:\n{}".format(lyrsReset, lyrsNotReset),"Layer Reset Summary", 0)

class RestoreLayers(object):
    """Implementation for Layers_addin.RestoreLayers (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        try:
            # Create an instance of the ResetLayers class.
            reset = ResetLayers()
            # Call ResetLayers onClick method.
            reset.onClick()

            workspace = autoPath()
            os.chdir(workspace)

            mxd = arcpy.mapping.MapDocument("CURRENT")
            ddp = mxd.dataDrivenPages
            pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
            dfLst = arcpy.mapping.ListDataFrames(mxd)
            layers = arcpy.mapping.ListLayers(mxd)

            # Add description to layers if blank.
            for layer in arcpy.mapping.ListLayers(mxd):
                if layer.description == "":
                    layer.description = "This is a default description for the '%s' layer. Feel free to change or update this description." % (layer.name)

            # Initialize empty list for MessageBox.
            lyrsRestored = []
            # Iterate features and dataframes. Replace if layerfile exists for feature.
            for df in dfLst:
                for lyr in arcpy.mapping.ListLayers(mxd,"*", df):
                    if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer:
                        lyrString = "%s_%s_%s.lyr" % (pageName, lyr.name, df.name)
                        if lyrString in arcpy.ListFiles("*.lyr"):
                            ref_layer = arcpy.mapping.ListLayers(mxd, lyr.name, df)[0]
                            insert_layer = arcpy.mapping.Layer("%s\\%s" % (workspace, lyrString))
                            arcpy.mapping.InsertLayer(df, ref_layer,insert_layer, "AFTER")
                            arcpy.mapping.RemoveLayer(df, ref_layer)
                            lyrsRestored.append(lyrString + df.name)

            pythonaddins.MessageBox("Layers Restored:\n%s" % lyrsRestored,"Restored Layers Summary", 0)
        except Exception as e:
            pythonaddins.MessageBox(e, "Error")

class SaveLayers(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        try:
            workspace = autoPath()
            mxd = arcpy.mapping.MapDocument("CURRENT")
            ddp = mxd.dataDrivenPages
            dfLst = arcpy.mapping.ListDataFrames(mxd)
            pageName = ddp.pageRow.getValue(ddp.pageNameField.name)

            # Set data frame name to credits field (can change to description field) for use in lyrString. 
            for df in dfLst:
                for lyr in arcpy.mapping.ListLayers(mxd, "*", df):
                    if isinstance(lyr, arcpy.mapping.Layer) and not lyr.isGroupLayer:
                        lyr.credits = df.name

            lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
            if not isinstance(lyr, arcpy.mapping.Layer) or lyr.isGroupLayer:
                pythonaddins.MessageBox('Please select one (1) layer (not a group or data frame or multiple layers) in the Table Of Contents', 'Layer Selection Error', 0)
            else:
                lyrString = "%s_%s_%s.lyr" % (pageName, lyr.name, lyr.credits)
                arcpy.SaveToLayerFile_management(lyr, workspace + "\\" + lyrString, "ABSOLUTE")
                pythonaddins.MessageBox("%s layer saved to:\n\n%s\n\nas:\n\n%s" % (lyr.name, workspace, lyrString), "Layer Saved", 0)
        except Exception as e:
            pythonaddins.MessageBox(e, "Error")