"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Script Name: DynamicTextElement.py
# Author: James Stephaniuk

# Requirements:
# 	- Add table with SVA/PVA info to map document.
#	- Add unique element name to box that contains SVA/PVA text.
#	- Must manually create a text element. 
#	- Set text element alignment.
#	- Set text element font style (optional).
#	- Set text element colour (optional).
#
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
# ddp = mxd.dataDrivenPages
# pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # pageName value must occur in pvaTable.

pvaTable = arcpy.mapping.ListTableViews(mxd, "PVA_text_placement")[0]
# pvaCursor = arcpy.da.SearchCursor(pvaTable.dataSource, pageName) # Limit to ddp edabbr/map number.


# Assign unique names to text elements. Zero-based.
txtElemLst = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
for i, txtElem in enumerate(txtElemLst):
	if txtElem.name.lower() != "title":
		txtElem.name = "Text_Element_" + str(i)
txtElemLst = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Text_Element*") # List of text elements excluding title elem.



txtElem_0 = txtElemLst[0]
# Text elements cannot be an empty string.
txtElem_0.text = " " # Place holder.
pvaCursor = arcpy.da.SearchCursor(pvaTable.dataSource, "*") # Limit to ddp edabbr/map number. See above pvaCursor variable.
for row in pvaCursor:
	txtElem_0.text += "%s %s FOO %0s\n" % (pvaCursor[-1], pvaCursor[-4], pvaCursor[-8]) # Replace indices with column names.
if txtElem_0.text[0].isspace and len(txtElem_0.text) > 1:
	txtElem_0.text = txtElem.text[1:] # Remove leading place holder.
arcpy.RefreshActiveView()


# TODO:
	# Figure out spacing/format of text element # Idea: Get lengths of address (middle) field from cursor and align from to max value. Use a while loop.
	# elementWidth
	# elementHeight
	# elementPositionX
	# elementPositionY
	# fontSize


