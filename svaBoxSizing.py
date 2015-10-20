import arcpy

# Author: James Stephaniuk
# October 19, 2015
#
# Populates and aligns a graphic box with data from an shapefile attribute table.

mxd = arcpy.mapping.MapDocument("CURRENT")
mapLyr = arcpy.mapping.ListLayers(mxd,"SVAs_Internal_LabelsAnno*")[0]

# SVA container (graphic box) name.
svaBox = "svaBox"

# Graphic box ayout settings.
fontSize = 10.0
padding = 0.2
spacer = 0.1

# SVA text element names.
svaTxtElem0  = "SVA_textElem0"
svaTxtElem1  = "SVA_textElem1"
svaTxtElem2  = "SVA_textElem2"
svaTxtElem3  = "SVA_textElem3"
# SVA feature class field names.
svaTxtField0 = "textstring"
svaTxtField1 = "status"
svaTxtField2 = "fontname"
svaTxtField3 = "shape_length"

svaElem  = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem0)[0]
addrElem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem1)[0]
txtElem2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem2)[0]
txtElem3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem3)[0]

elemLst = [svaElem,addrElem, txtElem2, txtElem3]

# Captions cannot be empty therefore a single char (space). Set all font sizes to same.
for elem in elemLst:
	elem.text = " "
	elem.fontSize = fontSize

# Create columns.
rows = arcpy.SearchCursor(mapLyr.dataSource)
for row in rows:
	svaElem.text  += "{}\n".format(row.getValue(svaTxtField0))
	addrElem.text += "{}\n".format(row.getValue(svaTxtField1))
	txtElem2.text += "{}\n".format(row.getValue(svaTxtField2))
	txtElem3.text += "{}\n".format(row.getValue(svaTxtField3))

# Slice off leading space char.
for elem in elemLst:
	elem.text = elem.text[1:]

svaBox = arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", svaBox)[0]

# Position text elements.
addrElem.elementPositionY = txtElem2.elementPositionY = txtElem3.elementPositionY = svaElem.elementPositionY = svaBox.elementPositionY + padding
svaElem.elementPositionX  = svaBox.elementPositionX   + padding
addrElem.elementPositionX = svaElem.elementPositionX  + svaElem.elementWidth + spacer
txtElem2.elementPositionX = addrElem.elementPositionX + addrElem.elementWidth + spacer
txtElem3.elementPositionX = txtElem2.elementPositionX + txtElem2.elementWidth + spacer

# Set the svaBox height and width derived from text elements heights and widths.
tallestElem = max(svaElem.elementHeight, addrElem.elementHeight, txtElem2.elementHeight, txtElem3.elementHeight)
svaBox.elementHeight = tallestElem + (padding * 2)
svaBox.elementWidth = txtElem3.elementPositionX - svaElem.elementPositionX + txtElem3.elementWidth + (padding * 2)

# Set the svaBox position derived from svaTxtElem0 XY position.
svaBox.elementPositionX = svaElem.elementPositionX - padding
svaBox.elementPositionY = svaElem.elementPositionY - padding

