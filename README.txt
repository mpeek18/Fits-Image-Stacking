This program is a generic version of parent program that is specific to normalizing, rotating, and stacking Hubble Space Telescope images. 

This particular program has the basic functionality and is designed to be customizable given the unique needs of the user.

Input images MUST BE .fits format.

Image_Stack must first know what files to read in from the current working directory. In the case of this version of the program, this information is provided by an external ASCII table file. Image_Stack reads the ASCII table that is in .dat format and gets only the object ID column. Next Image_Stack starts a loop that goes through the object ID's and finds the specific fits image associated with the current object ID.

The first function called from within the loop is normalizeImage which takes the file name as a parameter. NormalizeImage function extracts the data from the image and sums it all together. Because an image is simply a 2-Dimensional array, Numpy handles the process of summing all the pixel values together. Next, each individual pixel is divided by the value of the summed data. This normalizes that data by relating the values of individual pixels to each other so that some values are not extreme to each other. Finally, the normalized image is returned for further processing.

This version of Image_Stack relys on an additional text document that provides information concering the object ID numbers and angle to rotate the image. This is most likely the most probable section of the program that will need to be customized. As of now Image_Stack reads in the text file and splits the text into columns for the current hubble field, image ID's, and angles. Next, this data is added to lists so it can be worked with.

Withing the current image for loop, the object ID list created from the external text file is searched for a match to the current loop image. If a match is found, getRotationAngle function is called and the object ID and object ID list are passed as parameters.

The getRotationAngle function simply goes through the object ID list and matches the current object ID with an object ID within the list. Next the angle the image needs to be rotated is assigned to a variable and returned. 

We are now back inside the for loop. Now that we have a rotation angle the rotateImages function is called. RotateImages takes the normalized image, the current object ID, and rotation angle as parameters.

RotateImage function uses the normalized image and rotation angle to rotate the image to the specified angle. NOTE: .fits images are rotated clockwise, whereas .png are rotated counter clockwise. This needs to be carefully considered by the user. For the purpose of this developer, galaxy angles needed to be negated to compensate for the rotation function rotating images clockwise instead of counter clockwise. Finally, the rotated image is returned.

Back inside the for loop, the rotated image is returned but needs to be resized to a standard x, y size. In order to be stacked, all the images have to be the same size. The resized images are appended to a list and the loop is finished.

The stackImages function is called and is passed the resized image list as a parameter. StackImages goes through all image numpy arrays and assignes it all to a single variable. Using numpy, the stack is accomplished by summing all the image data together by either a mean sum, median sum, or standard sum. All three forms of stacked images are written out as new .fits images.

Image_Stack is now complete, a counter keeps track of how many images were processed and stacked and prints out the result. The output of the stacked images are written into the current working directory.