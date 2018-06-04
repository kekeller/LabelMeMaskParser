
import xml.etree.ElementTree as et
import glob
import os
import numpy as np
import scipy as sp
from PIL import Image, ImageDraw

nx, ny = 256,256

def parsePolygon( etelem ):
    points = []
    for pt in etelem.findall('pt'):
        num = pt.find('x').text
        if '.' in num: 
            tx = int(float(num))
        else:
            tx = int(num)
        num = pt.find('y').text
        if '.' in num:  
            ty = int(float(num))
        else:
            ty = int(num)

        points.append(tx)
        points.append(ty)
    return points

def parseLabeledObjects(root, maskDir):

    file_name = root.findall('filename')[0].text
    polygon = []
    name_list = []

    for lmobj in root.findall('object'):
        deleted = lmobj.find('deleted').text.encode('utf-8').strip()
        if deleted=='1':
            continue

        nameobj = lmobj.find('name')
        if nameobj.text is None:
            continue
        name = nameobj.text
        name_list.append(name)

        properties = {}
        for attrib in lmobj.findall('attributes'):
            if not attrib.text: break
            properties[ attrib.text.encode('utf-8').strip() ] = ''
        polygon.append( parsePolygon( lmobj.find('polygon') ))
        
    #print(polygon)
    img = Image.new("RGB", [nx, ny], (255,255,255) )
    for poly,name in zip(polygon,name_list):
        print(name)
        color = (255,100,0)
        #color = (0,0,0)
        if (len(poly) < 3): continue

        ImageDraw.Draw(img).polygon(poly, outline=color, fill=color)
        #ImageDraw.Draw(img).polygon(poly, outline=color)
        mask = np.array(img)

    #file_name = file_name.replace('.jpg','_m.jpg')
    file_name = maskDir + file_name
    img.save(file_name.replace('.jpg','.png'), "PNG")

def parseFolder( localDir, maskDir):
    labels = []
    fsAnnotPath = os.path.join(localDir) + '/*.xml'
    print(fsAnnotPath)
                  
    for fsAnnotFullpath in glob.glob( fsAnnotPath ):
        print(fsAnnotFullpath)
        # parse the XML file on the file system
        tree = et.parse( fsAnnotFullpath )
        root = tree.getroot()
        print(root)
        if not (os.path.exists(maskDir)):
            os.mkdir(maskDir)

        parseLabeledObjects(root, maskDir)

def combineMaskImage(maskDir,imageDir,maskImageComb):
    maskPath = os.path.join(maskDir) + '/*.png'
    imagePath = os.path.join(imageDir) + '/*.jpg'
    print('combined mask')

    for maskFullPath, imageFullpath in zip(glob.glob( maskPath ), glob.glob( imagePath ) ):
        maskImg = Image.open(maskFullPath)
        name = maskFullPath.replace(maskDir, imageDir )
        name = name.replace('.png','.jpg')
        origImg = Image.open(name)

        maskImg = maskImg.convert("RGBA")
        origImg = origImg.convert("RGBA")

        new_img = Image.blend(origImg,maskImg, 0.4)
        
        if not (os.path.exists(maskImageComb)):
            os.mkdir(maskImageComb)

        file_name = maskFullPath.replace(maskDir,maskImageComb )
        file_name = file_name.replace('.png','.jpg')
        print(file_name)

        new_img.save(file_name)


maskDir = './mask/'
xmlFolder = './xml/'
imageDir = './img/'
maskImageComb = './combined/'

parseFolder(xmlFolder,maskDir)
combineMaskImage(maskDir,imageDir,maskImageComb)


