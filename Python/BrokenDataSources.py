import arcpy.mapping as mapping, os
path = r"C:"
f = open(r"C:\Users\jastepha\Desktop\BrokenDataList.txt",'w')
for root,dirs,files in os.walk(path):
 for filename in files:
     basename, extension = os.path.splitext(filename)
     if extension == ".mxd":
         fullPath = os.path.join(path,filename)
         mxd = mapping.MapDocument(fullPath)
         f.write("MXD: " + filename + "\n")
         brknList = mapping.ListBrokenDataSources(mxd)
         for brknItem in brknList:
             f.write("\t" + brknItem.name + "\n")
f.close()

