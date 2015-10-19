import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
mapLyr = arcpy.mapping.ListLayers(mxd,"BS88_PointVAs*")[0]

# SVA container (graphic box) name.
svaBox = "svaBox"

# Layout dimensions.
fontSize = 10.0
padding = 0.25
spacer = 0.1

# SVA text element names.
svaTxtElem0  = "SVA_textElem0"
svaTxtElem1  = "SVA_textElem1"
svaTxtElem2  = "SVA_textElem2"
svaTxtElem3  = "SVA_textElem3"
# SVA feature class field names.
svaTxtField0 = "edabbr"
svaTxtField1 = "vaabbr"
svaTxtField2 = "vcount"
svaTxtField3 = "vaname"

svaElem  = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem0)[0]
addrElem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem1)[0]
txtElem2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem2)[0]
txtElem3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem3)[0]

# Captions cannot be empty therefore a single char (space). Set all font sizes to same.
for elem in [svaElem, addrElem, txtElem2, txtElem3]:
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
svaElem.text = svaElem.text[1:]
addrElem.text = addrElem.text[1:]
txtElem2.text = txtElem2.text[1:]
txtElem3.text = txtElem3.text[1:]

svaBox = arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", svaBox)[0]

# Position text elements.
addrElem.elementPositionY = txtElem2.elementPositionY = txtElem3.elementPositionY = svaElem.elementPositionY = svaBox.elementPositionY
svaElem.elementPositionX  = svaBox.elementPositionX   + padding
addrElem.elementPositionX = svaElem.elementPositionX  + svaElem.elementWidth + spacer
txtElem2.elementPositionX = addrElem.elementPositionX + addrElem.elementWidth + spacer
txtElem3.elementPositionX = txtElem2.elementPositionX + txtElem2.elementWidth + spacer

# Set the svaBox height and width derived from svaTxtElem height and widths.
tallestElem = max(svaElem.elementHeight, addrElem.elementHeight, txtElem2.elementHeight, txtElem3.elementHeight)
svaBox.elementHeight = tallestElem + (padding * 2)
svaBox.elementWidth = svaElem3.elementPositionX - svaElem.elementPositionX + svaElem3.elementWidth + (padding * 2)

# Set the svaBox position derived from svaTxtElem0 XY position.
svaBox.elementPositionX = svaElem.elementPositionX - padding
svaBox.elementPositionY = svaElem.elementPositionY - padding

