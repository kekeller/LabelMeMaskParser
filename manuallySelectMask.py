from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os, glob
from matplotlib.widgets import Button
import csv 
import numpy as np
import shutil
from skimage.morphology import erosion, dilation, opening,square


nx, ny = 256, 256

combinedDir = './combined/'

class ImageSelect(object):
	
	def __init__(self):
		self.selected = []

	def A(self, event):
		plt.close()
		self.selected.append('A')

	def B(self, event):
		plt.close()
		self.selected.append('B')
		
	def C(self, event):
		plt.close()
		self.selected.append('C')

	def ALL(self, event):
		plt.close()
		self.selected.append('ALL')


def chooseBestMaskManually(localDir):
	"""
	Present three masks to user and allow user to select A/B/C/ALL
	Save name and selection in output file
	"""
	selected = []
	imList = os.path.join(localDir) + '/*.jpg'
	base_image = []          
	for im in glob.glob( imList ):
		
		name = im.replace(localDir,'')
		if (name[0] == 'A'):
			base_image.append(name.replace('A_',''))

	callback = ImageSelect()
	for i in base_image:
		name_A = localDir + 'A_' + i
		name_B = localDir + 'B_' + i
		name_C = localDir + 'C_' + i
		A = mpimg.imread(name_A)
		B = mpimg.imread(name_B)
		C = mpimg.imread(name_C)
		
		fig = plt.figure(figsize=(20,10))
		
		plt.subplot(131)
		plt.imshow(A)
		plt.axis("off")

		plt.subplot(132)
		plt.imshow(B)
		plt.axis("off")

		plt.subplot(133)
		plt.imshow(C)
		plt.axis("off")
		
		a_loc = plt.axes([0.2, 0.05, 0.1, 0.075])
		a_sel = Button(a_loc, 'A')
		a_sel.on_clicked(callback.A)

		b_loc = plt.axes([0.4, 0.05, 0.1, 0.075])
		b_sel = Button(b_loc, 'B')
		b_sel.on_clicked(callback.B)

		c_loc = plt.axes([0.6, 0.05, 0.1, 0.075])
		c_sel = Button(c_loc, 'C')
		c_sel.on_clicked(callback.C)

		d_loc = plt.axes([0.8, 0.05, 0.1, 0.075])
		d_sel = Button(d_loc, 'ALL')
		d_sel.on_clicked(callback.ALL)

		plt.show()
		print(callback.selected)

	mask_file = open("mask.csv","w")
	print(callback.selected )
	masks = callback.selected
	for m, img in zip(masks,base_image):
		mask_file.write(str(img) + "," + str(m) + "\n")
	mask_file.close()


chooseBestMaskManually(combinedDir)