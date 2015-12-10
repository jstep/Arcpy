# Arcpy AddIns & Command Line Tools
ESRI Arcpy scripts for ArcGIS.

A collection of add-in and command line tools for map production and automation.

<strong>Add_Ins</strong>
  <ul>
    <li>Contains tools to record, restore, and reset layouts of data driven page (DDP) enabled mxds.
    <li>Records layout position, size, and extents of north arrows, scale bars/text, and data frames.
    <li>Saves data to a `.dbf` with specific name, which can be changed.
  </ul>

<strong>Annotation & Annotation_Stand_Alone</strong>
  <ul>
    <li><strong>ExtentBoxes</strong> Tool to create bounding boxes (polygons) of ddp dataframe extents of on-map dfs. Used for index polygon for Tiled Annotation creation.
    <li><strong>GenerateTiledAnno</strong> Automation of `TiledLabelsToAnnotation_cartography` tool that uses above generated boxes as index polygons.
    <li>Stand-alone script is the same tool as above but is run from the command line with syntax `python NAME_OF_SCRIPT.py`. Doesn't need ArcMap GUI and is therefore much fasterthan the above tools. 
  </ul>
  
<strong>Layers</strong>
  <ul>
    <li>A method of programmatically saving and restoring layer symbology for a given ddp.
    <li>Saves layerfiles to a specific location named as `pageName_layerName_dataframeName.lyr`.
  </ul>
  
<strong>PDF_Export_Addin & PDF_Export_Stand_Alone</strong>
  <ul>
    <li>Buttons to automate pdf export with pre-defined parameters. Can be easily altered to allow different params.
    <li>Generates pdf name in the form `pageName_dpi_colorspace_orientation`.
    <li>Stand-alone script is the same tool as above but is run from the command line with syntax `python NAME_OF_SCRIPT.py DPI` where DPI is and integer representing the dots per inch of the exported pdf. Doesn't need ArcMap GUI and is therefore much faster than the above tools. 
  </ul>
  
<strong>QuerySelection</strong>
  <ul>
    <li>On button press genterates definition query for layer of selected features. Simply select features you want to display for one layer, and press the button.
    <li>Select layer in table of contents and press clear selection button to clear the query for that layer.
  </ul>
  
<strong>ReplicateSD (Command Line Tool)</strong>
  <ul>
    <li>An automated way to replicate ArcSDE connected database to a local FGDB to improve performance.
    <li>Uses a list (`layerNameLst`) to control which files are copied. Can easily be altered to include all files on SDE. 
    <li>Change databaseConnection variable to your .sde connection file.
    <li>Can be run by a task scheduler at regular intervals to keep data up-to-date.
  </ul>
