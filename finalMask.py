from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os, glob
from matplotlib.widgets import Button
import csv 
import numpy as np
import shutil

nx, ny = 256,256

maskDir = './mask/'
voteMaskDir = './mask_vote/'
blendImageDir = './blendImages/'
imageDir = './img/'
fullTIFImageDir = '/home/kevin/Pictures/2018_soy_segmentation/Early_Growth/256x256/processed/tif/'
selectedTIFDir = './TIF/'
finalBlackMaskDir = './blackMask/'

def voteMask(localDir,voteMaskDir, finalBlackMaskDir):
	""" 
	Reads the input file from the manual mask voting process, and outputs
	an orange and a black mask. 

	The orange mask will get combined with the jpg image to create an overlay of mask/image
	The black mask is an 8 bit two channel binary image for training. 
	"""

	imgList = []
	choosen = []
	
	with open('mask.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			imgList.append(row[0])
			choosen.append(row[1])

	if not (os.path.exists(finalBlackMaskDir)):
		os.mkdir(finalBlackMaskDir)

	if not (os.path.exists(voteMaskDir)):
			os.mkdir(voteMaskDir)

	for img,ch in zip(imgList,choosen):
		print(img, ch)
		if (ch == 'ALL'):
			name_A = localDir + 'A_' + img.replace('.jpg','.png')
			name_B = localDir + 'B_' + img.replace('.jpg','.png')
			name_C = localDir + 'C_' + img.replace('.jpg','.png')
			A = np.array(Image.open(name_A))
			B = np.array(Image.open(name_B))
			try:
				C = np.array(Image.open(name_C))
			except:
				C = np.array(Image.open(name_A))
			
			newImage = Image.new("RGB", [nx, ny], (255,255,255) )
			newImage = np.array(newImage)

			blackMask = Image.new("L", [nx, ny], 255 )
			blackMask = np.array(blackMask)

			for rowCount in range( len(newImage) ):
				for pixCount in range( len(newImage) ):
					if( (A[rowCount][pixCount][2] < 255 and B[rowCount][pixCount][2] < 255) or  
						(A[rowCount][pixCount][2] < 255 and C[rowCount][pixCount][2] < 255) or
						(B[rowCount][pixCount][2] < 255 and C[rowCount][pixCount][2] < 255) ):
						#print(newImage[rowCount][pixCount])
						newImage[rowCount][pixCount] = (255,100,0)
						blackMask[rowCount][pixCount] = 0
			
			file_name = voteMaskDir + img
			file_name = file_name.replace('.jpg','.png')
			newImage = Image.fromarray(newImage)
			
			blackMask = Image.fromarray(blackMask)

			newImage.save(file_name)

			file_name = file_name.replace(voteMaskDir,finalBlackMaskDir)
			blackMask.save(file_name)

		if (ch != 'ALL' and ch != 'NONE'):
			name = localDir + str(ch) + '_' + img.replace('.jpg','.png')
			print(name)
			if(os.path.isfile(name)):
				goodMask = Image.open(name)
				file_name = voteMaskDir + img
				file_name = file_name.replace('.jpg','.png')
				goodMask.save(file_name)

				goodMask = np.array(goodMask)

				blackMask = Image.new("L", [nx, ny], 255 )
				blackMask = np.array(blackMask)

				for rowCount in range( nx ):
					for pixCount in range( ny ):
						if( goodMask[rowCount][pixCount][2] < 255 ): 

							blackMask[rowCount][pixCount] = 0

				blackMask = Image.fromarray(blackMask)

				file_name = file_name.replace(voteMaskDir,finalBlackMaskDir)
				blackMask.save(file_name)


def combineMaskImage(voteMaskDir,imageDir,blendImageDir):
	"""
	Overlay mask and image to visually confirm results
	"""
	maskPath = os.path.join(voteMaskDir) + '*.png'
	imagePath = os.path.join(imageDir) + '*.jpg'

	for maskFullPath, imageFullpath in zip(glob.glob( maskPath ), glob.glob( imagePath ) ):
		maskImg = Image.open(maskFullPath)

		name = maskFullPath.replace(voteMaskDir, imageDir + 'A_')
		name = name.replace('.png','.jpg')
		origImg = Image.open(name)
		maskImg = maskImg.convert("RGBA")
		origImg = origImg.convert("RGBA")

		new_img = Image.blend(origImg,maskImg, 0.4)

		if not (os.path.exists(blendImageDir)):
			os.mkdir(blendImageDir)

		file_name = maskFullPath.replace(voteMaskDir,blendImageDir )
		print(file_name)
		new_img.save(file_name)


def copyTiffImages(fullTIFImageDir,selectedTIFDir,finalBlackMaskDir):
	"""
	Copy tiff images from original folder and save matching ones for data set
	"""
	maskPath = os.path.join(finalBlackMaskDir) + '*.png'

	if not (os.path.exists(selectedTIFDir)):
		os.mkdir(selectedTIFDir)

	for maskFullPath in glob.glob( maskPath ):
		img = maskFullPath.replace('.png','.tif')
		name = img.replace(finalBlackMaskDir,fullTIFImageDir)
		print(name)
		name_new = img.replace(finalBlackMaskDir,selectedTIFDir)
		shutil.copy(name,name_new)


voteMask(maskDir,voteMaskDir,finalBlackMaskDir)
combineMaskImage(finalBlackMaskDir,imageDir, blendImageDir)
copyTiffImages(fullTIFImageDir,selectedTIFDir,finalBlackMaskDir)