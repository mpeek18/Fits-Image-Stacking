# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 14:30:00 2018

@author: Matthew Peek
@last Modified: 18 October 2018
Generic rotation and stacking program
"""
import numpy as np
from astropy.io import ascii
import astropy.io.fits as fits
from matplotlib import pyplot as plt
from skimage.transform import rotate, resize


"""
Normalize Image function takes a single .fits image extracts the data and
stores in a variable, sums all individual pixel values, then divides each 
individual pixel value by the sum of all pixel values.

:param .fits image.
:return normalized .fits image.
"""
def normalizeImage(fileName):
    data = fits.getdata(fileName)
    sumData = np.sum(data)
    print ("Summed Image Data:", sumData,'\n')
    print ("Data:", data,'\n')
        
    normed = (data / sumData)
    print ("Normalization complete!")
        
    return normed
#End normalizeImage function

    
"""
Get Rotation Angle function takes an image ID number and list of object ID's
and matches the current object ID with the ID of an object in a list.
If match is found, gets the object's angle and returns the angle.

:param current object ID.
:param list of all object ID's.
:return angle object to be rotated.
"""
def getRotationAngle(ID, objIdList):
     for i in range(0, len(objIdList)):
        if (ID == objIdList[i]):
            rotationAngle = objIdList[i]
     print ("ID " + ID + " " + "angle " + rotationAngle)
     return rotationAngle
#End getRotationAngle Function


"""
Rotate Image function takes the current normalized image, image ID number, 
and angle to be rotated. Rotates the image clockwise and returns the
rotated image.

:param normalized image.
:param image ID number.
:param image rotation angle.
:returns rotated image.
"""     
shape = []
def rotateImages(normedImage, ID, rotationAngle):
    rotImage = rotate(normedImage, float(rotationAngle), True)
    print ("Image " + ID + " Rotated!")
    print ("Image shape:", rotImage.shape)
    return rotImage   
#End rotateImages function
    
"""
Stack Images function takes a list of images that have been normalized and
rotated, extracts each individual image from list and stores as numpy variable.

Numpy variable is then stacks each individual image by a mean average, median
average, and complete sum.

Stacked images are written out as .fits format into the current working
directory and given user defined names.

:param list of images.
"""
def stackImages(imageList):
    imageData = [file for file in imageList]
    
    print ("Total Absorber image data:", imageData,'\n')
    meanImage = np.mean(imageData, axis=0)
    medianImage = np.median(imageData, axis=0)
    imageStack = np.sum(imageData, axis=0)
    
    print ("Image Mean:", meanImage,'\n')
    print ("Image Median:", medianImage,'\n')
    print ("Image Sum:", imageStack,'\n')
    
    plt.clf()
    plt.imshow(meanImage)
    plt.colorbar()
    
    plt.clf()
    plt.imshow(medianImage)
    plt.colorbar()
    
    plt.clf()
    plt.imshow(imageStack)
    plt.colorbar()
    
    #Writes to current working directory and given user defined name.
    fits.writeto('Enter_user_defined_name_here.fits', meanImage, overwrite=True)
    fits.writeto('Enter_user_defined_name_here.fits', medianImage, overwrite=True)
    fits.writeto('Enter_user_defined_name_here.fits', imageStack, overwrite=True)
    
    print ("Stacking Images Complete!")
#End stackImages function
    
# =============================================================================
# Input file containing image ID numbers and angles to be rotated.
# =============================================================================
"""
This section of the program reads in the user defined file that containes 
image ID numbers and image angles and appends the data to lists for use in 
rotating and stacking functions.

FILE MUST BE .TXT FORMAT. 

Additional lists can be declared and used depending on the need of the user
and format of user's input file. 
"""
fields = []
imageIDs = []
angles = []
try:
    #Open function takes argument of file name to be opened.
    angleFile = open('File_name_here.txt', 'r')
    for line in angleFile:
        #line.split functions seperates line text into columns.
        fields.append(line.split()[0])
        imageIDs.append(line.split()[2])
        angles.append(line.split()[4])
    angleFile.close()

except IOError:
    print ("File could not be found in current directory!")
    
objIdList = []
imageAngles = []
for i in range(0, len(fields)):
    if (fields[i] == '8'):
        objIdList.append(imageIDs[i])
        imageAngles.append(angles[i])
        
print ("Image ID's", objIdList,'\n')
print ("Image Angles", imageAngles,'\n')
# =============================================================================
# Conclustion of image angle input file section.
# =============================================================================

# =============================================================================
# Begin section to read in user defined file containing image ID numbers
# of images user wishes to normalize, rotate, and stack.
# =============================================================================
"""
This section of the program reads in user supplied file containing image
ID's to be normalized, aligned, and stacked. Additional columns may be
read depending on user preference and input file contents.

INPUT FILE MUST BE ASCII TABLE .DAT FORMAT!

Individual image file names are assigned to variables and functions 
are then called to process each image. Once image has been normalized,
rotated, and resized, image is added to list to be stacked outside
of this section.
"""
absorberFile = ascii.read('File_name_here.dat', delimiter='|')
ID = absorberFile['col2']
count = 0
imageFileList = []
for i in range(1, len(ID)):
    try:
        fileName = 'Enter_Image_Name_Here' + ID[i] + '.fits'
                                
        #Call normalizeImage function.
        normed = normalizeImage(fileName)
                
        """
        Try and match ID's from Absorbtion data file with ID's from
        All Galaxy Angles file. If match found, call getGalAngles function
        and pass current matching ID as argument.
        """
        objectAngle = float(0.0)
        if (ID[i] in objIdList):
            objectAngle = getRotationAngle(ID[i], objIdList)
                
        """
        Call alignImages function and resize to stack.
        Note, images are not all the same size after rotating them, must resize
        in order to stack images.
        """
        rotImage = rotateImages(normed, ID[i], objectAngle)
        resized = resize(rotImage, (48,48))
                
        #Append normalized image to fileList to pass as argument to stack function.
        imageFileList.append(resized)
        file = fits.open(fileName)
        image = file[0].data
        file.close()
                
        count += 1
    except IOError:
        print ("Image ID " + ID[i] + " not found!")
# =============================================================================
# End user defined input file section and program's 'main'.
# =============================================================================
"""
Call stackImages function and hand it the list containing all normalized,
rotated, and resized images. Print out total number of images processed
by this program.
"""
stackImages(imageFileList)
print ("Number of images processed: ", count)