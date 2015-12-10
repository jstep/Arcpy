def autoPath(folderName="z_layer_files"):
    """Returns a workspace path one level above the MXD's current directory, 
    and sets the current workspace to that directory. Creates a folder with 
    name equal to parameter, if it does not already exist. 
    Parameters: Folder name. Default parameter is 'Layerfiles'.
    """
    import arcpy
    import os
    # Create a 'folderName' folder in parent folder.
    mxd = arcpy.mapping.MapDocument('CURRENT')
    currentDir = os.path.dirname(os.path.realpath(mxd.filePath))
    parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    layersPath = os.path.join(parentDir, folderName)
    if not os.path.exists(layersPath):
        os.makedirs(layersPath)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = layersPath
    workspace = arcpy.env.workspace

    return workspace