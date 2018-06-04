# LabelMeMaskParser
Read xml from LabelMe image segmentation tool and convert to mask.

LabelMe used with MTurk returns a list of xml files that correspond to each polygon that was segmented. 

This set of scripts was used to extract one xml category from the xml file, output it as a mask overlayed on the original image. 

Then we take these masks and select the best option for our image using a matplot script that presents each mask/image combo. We can then select mask A/B/C or ALL (which then sets the voting), or NONE which removes the image from the dataset. 

If there are a lot of NONE images, the last script builds a list of work IDs to reject on Amazon Mechanical Turk, as well as a list of images to repeat. 
