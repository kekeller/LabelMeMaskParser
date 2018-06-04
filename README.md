# LabelMeMaskParser
Read xml from LabelMe image segmentation tool and convert to mask.

LabelMe used with MTurk returns a list of xml files that correspond to each polygon that was segmented. 

This set of scripts was used to extract one xml category from the xml file, output it as a mask overlayed on the original image. 

Then we take these masks and select the best option for our image 
