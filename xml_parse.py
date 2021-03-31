
import xml.etree.ElementTree as et
import glob
import os
import cv2
import matplotlib.image
import numpy as np
import scipy as sp
from PIL import Image, ImageDraw

colors_dict = {'background': (0, 0, 0),
               'background_skin': (0, 255, 0),
               'pigmentation': (0, 0, 0),
               'mole': (0, 255, 0),
               'scary_spot': (0, 0, 0)
               }
nx, ny = 750, 430


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


def parseLabeledObjects(root, mask_output_path, final_mask_output_path):
    polygon = []
    name_list = []

    image_size = root.findall('imagesize')
    nx = int(image_size[0].find('ncols').text.encode('utf-8').strip())
    ny = int(image_size[0].find('nrows').text.encode('utf-8').strip())
    for lmobj in root.findall('object'):
        name = None
        deleted = lmobj.find('deleted').text.encode('utf-8').strip()
        if deleted == '1':
            continue

        nameobj = lmobj.find('name')
        if nameobj.text is None:
            continue
        name = nameobj.text

        properties = {}
        for attrib in lmobj.findall('attributes'):
            if not attrib.text: break
            properties[attrib.text.encode('utf-8').strip()] = ''
        try:
            polygon.append(parsePolygon(lmobj.find('polygon')))
            name_list.append(name)
        except:
            print(name + ' polygon not found')

    img = Image.new("RGB", [nx, ny], colors_dict['background'])
    list_of_labels = []
    for poly, name in zip(polygon, name_list):
        list_of_labels.append(name)
        if name == 'mol':
            color = colors_dict['mole']
        else:
            color = colors_dict[name]
        if len(poly) < 3:
            continue
        ImageDraw.Draw(img).polygon(poly, outline=color, fill=color)
    print(list_of_labels)
    img.save(mask_output_path)
    maskRGB = cv2.imread(mask_output_path, -1)
    final_mask_np = maskRGB[:, :, 1]
    final_mask_np = Image.fromarray(final_mask_np)
    final_mask_np.save(final_mask_output_path)


def parseFolder():
    sep = '/*'
    fsAnnot = []
    include_dirs = []
    for depth in range(1, max_folder_depth):
        xmls_path = xmlFolder[:-1:] + sep*depth
        include_dirs += glob.glob(xmls_path)
        for file in include_dirs:
            if os.path.isdir(file):
                masks_dir = file.replace(xmlFolder, maskDir)
                finalmasks_dir = file.replace(xmlFolder, finalMaskDir)
                combined_mask = file.replace(xmlFolder, maskImageComb)
                if not os.path.exists(masks_dir) and not os.path.exists(finalmasks_dir) and not os.path.exists(combined_mask):
                    os.mkdir(masks_dir)
                    os.mkdir(finalmasks_dir)
                    os.mkdir(combined_mask)
        include_dirs = []
        fsAnnot += glob.glob(xmls_path + '.xml')
    for fsAnnotFullpath in fsAnnot:
        print(fsAnnotFullpath)
        # parse the XML file on the file system
        tree = et.parse(fsAnnotFullpath)
        root = tree.getroot()
        mask_output_path = fsAnnotFullpath.replace(xmlFolder, maskDir).replace('.xml', '.png')
        final_masks_output_path = fsAnnotFullpath.replace(xmlFolder, finalMaskDir).replace('.xml', '.png')
        parseLabeledObjects(root, mask_output_path, final_masks_output_path)
        input_image_path = fsAnnotFullpath.replace(xmlFolder, imageDir).replace('.xml', '.*')
        input_image = glob.glob(input_image_path)
        myCombineMaskImage(input_image[0], mask_output_path)


def myCombineMaskImage(input_image_path, mask):
    img = cv2.imread(input_image_path, -1)
    if img.shape[2] > 3:
        img = img[:, :, 0:3]
    mask = cv2.imread(mask, -1)
    combined = cv2.addWeighted(mask, 0.45, img, 1, 0, img)
    cv2.imwrite(input_image_path.replace(imageDir, maskImageComb), combined)


def check_existence_of_each_image():
    sep = '/*'
    xmls = []
    imgs = []
    success = True
    missing = []
    for depth in range(max_folder_depth):
        xmls_path = xmlFolder[:-1:] + sep*depth + '.xml'
        xmls += glob.glob(xmls_path)
        imgs_path = imageDir[:-1:] + sep*depth
        imgs += glob.glob(imgs_path + '.png')
        imgs += glob.glob(imgs_path + '.jpg')
        imgs += glob.glob(imgs_path + '.jpeg')
    if len(xmls) != len(imgs):
        success = False
        xml_names_without_point = []
        for xml_name in xmls:
            xml_names_without_point.append(xml_name.split('/')[-1].split('.')[0])
        for img_name in imgs:
            if img_name.split('/')[-1].split('.')[0] not in xml_names_without_point:
                missing.append(img_name)
    return success, missing


def initialize_folders():
    if not (os.path.exists(maskDir)):
        os.mkdir(maskDir)
    if not (os.path.exists(maskImageComb)):
        os.mkdir(maskImageComb)
    if not (os.path.exists(finalMaskDir)):
        os.mkdir(maskImageComb)
    if not (os.path.exists(xmlFolder)):
        os.mkdir(xmlFolder)
    if not (os.path.exists(imageDir)):
        os.mkdir(imageDir)


max_folder_depth = 4
maskDir = './mask/'
xmlFolder = './xml/'
imageDir = './img/'
maskImageComb = './combined/'
finalMaskDir = './final_masks/'


success, missing = check_existence_of_each_image()
if success:
    parseFolder()
else:
    print(missing)
    print(len(missing))


