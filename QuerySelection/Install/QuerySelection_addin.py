import arcpy
import pythonaddins
import os
import sys


sys.path.append(os.path.dirname(__file__)) # Add this script to system path. Used to separate main script from other code packages.
import clearSelectedLayerQuery
import getSelectionSet
import querySelected

class ClearSelection(object):
    """Implementation for QuerySelection_addin.clearSelection (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        clearSelectedLayerQuery.clearSelectedLayerQuery()

class QuerySelection(object):
    """Implementation for QuerySelection_addin.querySelection (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        querySelected.querySelected()