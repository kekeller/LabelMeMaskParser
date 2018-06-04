import os, glob
from matplotlib.widgets import Button
import csv 
import numpy as np
import shutil
import pandas


def buildKeepRejectList():
	imgList = []
	choosen = []
	
	with open('mask.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			imgList.append(row[0])
			choosen.append(row[1])

	ExcelFileName= 'labelme.results.xls'

	nameList = []
	assignmentID = []
	hitidList = []
	hitpeidList = []
	with open(ExcelFileName) as csvfile:
		spamreader = csv.reader(csvfile, delimiter='	')
		for row in spamreader:
			hitidList.append(row[0])
			hitpeidList.append(row[1])
			nameList.append(row[13][156:])
			assignmentID.append(row[18])

	rejectID = []
	keepHITID = []
	imagesToRepeat = []
	goodImages = []
	A = 0
	B = 0
	C = 0
	for img,ch in zip(imgList,choosen):
		if (ch == 'NONE'):
			name_A = 'A_' + img
			name_B = 'B_' + img
			name_C = 'C_' + img

			for i in range(len(nameList)):
				if (name_A == nameList[i]):
					#print(str(name_A) + " " + str(nameList[i]))
					rejectID.append(assignmentID[i])
					imagesToRepeat.append(nameList[i])
					A +=1
				if (name_B == nameList[i]):
					rejectID.append(assignmentID[i])
					imagesToRepeat.append(nameList[i])
					B += 1
				if (name_C == nameList[i]):
					rejectID.append(assignmentID[i])
					imagesToRepeat.append(nameList[i])
					C+=1	


		if (ch == 'A' or ch == 'B' or ch == 'C' or ch == 'ALL'):
			name_A = 'A_' + img
			name_B = 'B_' + img
			name_C = 'C_' + img
			for i in range(len(nameList)):
				if (name_A == nameList[i]):
					keepHITID.append(hitidList[i])
					goodImages.append(nameList[i][2:])
			for i in range(len(nameList)):
				if (name_B == nameList[i]):
					keepHITID.append(hitidList[i])
					goodImages.append(nameList[i][2:])
			for i in range(len(nameList)):
				if (name_C == nameList[i]):
					keepHITID.append(hitidList[i])
					goodImages.append(nameList[i][2:])

	#print(len(rejectID) + len(keepHITID))

	rejectFile = 'labelme.reject'
	sucessFile = 'labelme.success'
	repeateFile = 'repeatImages.txt'
	goodFile = 'goodImages.txt'

	goodImages = set(goodImages)
	imagesToRepeat = set(imagesToRepeat)

	f = open(rejectFile,"w")
	f.write("assignmentIdToReject\n")
	for reject in rejectID:
		f.write(str(reject) + '\t\n')

	f = open(sucessFile,"w")
	f.write("hitid	hittypeid\n")
	for hitid in keepHITID:
		f.write(str(hitid) + '\t' + str(hitpeidList[1]) + '\n')

	f = open(repeateFile,"w")
	for name in imagesToRepeat:
		f.write(str(name) + ',\n')

	f = open(goodFile,"w")
	for name in goodImages:
		f.write(str(name) + ',\n')


def copyRepeatedImages(imageDir,newImgDir):
	"""
	Copy tiff images from original folder and save matching ones for data set
	"""
	imgList = []
	with open('repeatImages.txt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			imgList.append(row[0][2:])

	if not (os.path.exists(newImgDir)):
			os.mkdir(newImgDir)

	#print(len(imgList))
	A = 0
	for img in imgList:
		print(img)
		A +=1
		name = imageDir + img
		name_A = newImgDir + "A_" + img
		shutil.copy(name,name_A)
		name_B = newImgDir + "B_" + img
		shutil.copy(name,name_B)
		name_C = newImgDir + "C_" + img
		shutil.copy(name,name_C)

	#print(A)

	goodList = []
	for tif in glob.glob( os.path.join('./blackMask') + '/*.png'  ):
		n = tif.replace('./blackMask/','')
		goodList.append(n.replace('.png','.jpg'))

	tifPath = os.path.join('./TIF') + '/*.tif'

	originalList = []
	for tif in glob.glob( tifPath ):
		n = tif.replace('./TIF/','')
		originalList.append(n.replace('.tif','.jpg'))

	for name in originalList:
		if (name not in goodList) and (name not in imgList):
			print(name)

imageDir = '/home/kevin/Pictures/2018_soy_segmentation/Early_Growth/256x256/processed/jpg/'
newImgDir = './jpgCopy/'


buildKeepRejectList()
copyRepeatedImages(imageDir,newImgDir)