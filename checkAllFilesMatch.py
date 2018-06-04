import os, glob

maskDir = '/home/kevin/Documents/Data_Set/Labeled_Data/MASK/'
imgDir = '/home/kevin/Documents/Data_Set/Labeled_Data/IMAGES/'


maskPath = os.path.join(maskDir) + '*.png'
imgPath = os.path.join(imgDir) + '*.tif'

maskList = []
imgList = []

for maskFullPath in glob.glob( maskPath ):
	maskList.append(maskFullPath[49:-4]) # crude way to get only the name, only has to be used once...

for imgFullPath in glob.glob( imgPath ):
	imgList.append(imgFullPath[51:-4])

print( "Masks match to images: " + str(set(maskList) == set(imgList))  )