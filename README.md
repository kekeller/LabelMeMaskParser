# LabelMeMaskParser
Read xml from LabelMe image segmentation tool and convert to mask.

LabelMe used with MTurk returns a list of xml files that correspond to each polygon that was segmented. 

This set of scripts was used to extract one xml category from the xml file, output it as a mask overlayed on the original image. 

Then we take these masks and select the best option for our image using a matplot script that presents each mask/image combo. We can then select mask A/B/C or ALL (which then sets the voting), or NONE which removes the image from the dataset. 

If there are a lot of NONE images, the last script builds a list of work IDs to reject on Amazon Mechanical Turk, as well as a list of images to repeat. 

## Moles Detective Project Changes
In out project, we created our own annotations from moles images.  
we used LabelMe, to label approximately 5000 raw data images. 
for this target, those features was added:
- there is now an option to parse a complete directory root with sub-directories.
- it's possible to ignore unwanted labels although they exist in the xml.
- rgb masks can be generated with any color (for each label color can be modified)
- code is more readable, and scalable.