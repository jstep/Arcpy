import arcpy

# Author: James Stephaniuk
# October 19, 2015
#
# Populates and aligns a graphic box with data from an shapefile attribute table.

mxd = arcpy.mapping.MapDocument("CURRENT")
# Feature class name.
mapLyr = arcpy.mapping.ListLayers(mxd,"SVAs_Internal_LabelsAnno*")[0]

# SVA container (graphic box) name.
svaBox = "svaBox"

# Graphic box layout settings.
# fontSize = 10.0
padding = 0.2
spacer = 0.1

# SVA text element names.
SVATitleText  = "SVATitle"
svaTitleElem0 = "SVA_TitleElem0"
svaTitleElem1 = "SVA_TitleElem1"
svaTitleElem2 = "SVA_TitleElem2"
svaTitleElem3 = "SVA_TitleElem3"
svaTxtElem0   = "SVA_textElem0"
svaTxtElem1   = "SVA_textElem1"
svaTxtElem2   = "SVA_textElem2"
svaTxtElem3   = "SVA_textElem3"
# SVA feature class field names.
svaTxtField0 = "textstring"
svaTxtField1 = "textstring"
svaTxtField2 = "textstring"
svaTxtField3 = "shape_length"

SVATitle   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", SVATitleText)[0]
titleElem0 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem0)[0]
titleElem1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem1)[0]
titleElem2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem2)[0]
titleElem3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem3)[0]
svaElem    = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem0)[0]
addrElem   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem1)[0]
txtElem2   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem2)[0]
txtElem3   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem3)[0]

elemLst = [svaElem,addrElem, txtElem2, txtElem3]

# Captions cannot be empty therefore a single char (space). Set all font sizes to same.
for elem in elemLst:
	elem.text = " "
	#elem.fontSize = fontSize ### TODO

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

titleElem0.elementPositionX = svaElem.elementPositionX
titleElem1.elementPositionX = addrElem.elementPositionX
titleElem2.elementPositionX = txtElem2.elementPositionX
titleElem3.elementPositionX = txtElem3.elementPositionX

titleElem0.elementPositionY = svaElem.elementPositionY + svaElem.elementHeight + spacer
titleElem1.elementPositionY = addrElem.elementPositionY + addrElem.elementHeight + spacer
titleElem2.elementPositionY = txtElem2.elementPositionY + txtElem2.elementHeight + spacer
titleElem3.elementPositionY = txtElem3.elementPositionY + txtElem3.elementHeight + spacer

SVATitle.elementPositionX = titleElem0.elementPositionX
SVATitle.elementPositionY = titleElem0.elementPositionY + titleElem0.elementHeight + spacer

# Set the svaBox height and width derived from text elements heights and widths.
tallestElem = max(svaElem.elementHeight, addrElem.elementHeight, txtElem2.elementHeight, txtElem3.elementHeight)
boxHeight = SVATitle.elementPositionY  - svaElem.elementPositionY + SVATitle.elementHeight
svaBox.elementHeight = boxHeight + (padding * 2)
svaBox.elementWidth = txtElem3.elementPositionX - svaElem.elementPositionX + txtElem3.elementWidth + (padding * 2)
svaBox.elementWidth = max(txtElem3.elementPositionX - svaElem.elementPositionX + txtElem3.elementWidth, SVATitle.elementWidth) + (padding * 2)

# Set the svaBox position derived from svaTxtElem0 XY position.
svaBox.elementPositionX = svaElem.elementPositionX - padding
svaBox.elementPositionY = svaElem.elementPositionY - padding

# SVA Box title.
# svaBox.elementHeight += 0.5
