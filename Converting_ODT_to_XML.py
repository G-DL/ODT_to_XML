"""

This program converts all the ODT files present in the directory root:\ODTfolder
to the XML files that hold their corresponding text content.
The script runs reasonably fast, and on my old machine it computes 100 files consisting of 1 page each
in around half a second.

********************
Please note: If the original files contain at any point this string of two characters:
\n
this string WILL be removed. You have been warned.
Python does not handle well the conversion between escape characters and strings of characters,
and the solution I have implemented is the only one that I could make work after multiple failed attempts.
********************

The process of unzipping the xml from the odt files unfortunately returns some unwanted 
characters in addition to the content of the actual xml file, and it was not possible to find a way around it
besides the manual removal of the unwanted characters.
These characters are:
b'              at the beginning of content.xml
\n              after the first xml tag
'               at the end of the file
Any comment or suggestion on how to achieve a more clean extraction of the XMLs would be welcome and appreciated.

The files extracted are readable and clean, and are ready to be parsed.

"""

"""
#############################################################
Dependencies
#############################################################
"""

import os
# os handles pathing and parsing
import zipfile
# zipfile handles the ODT files. This format is in fact a zipped archive of several XML files
import re
# Regular expression is used to clean the XML files from bytes at the beginning and ending of the
# decompressed zip archive, which are leftover from the decompression process

"""
#############################################################
Pathing-related code
#############################################################
"""

directoryODT = '\\ODTfolder' # Input directory. Change this to change the path to the ODT inputs

# Checks if the predefined directory exists. If it doesn't, prompts the user to 
# place the odt files in the predefined directory, and creates such directory
if os.path.exists(directoryODT)==False:
    print("Error. The ODT files to be converted to XML should be placed in the root:{0} directory".format(directoryODT))
    os.mkdir(directoryODT)

# Informs the user of the location of the converted XML files, and creates the output directory if necessary
directoryXML = '\\XMLfolder' # Output directory. Change this to change the path to the XML outputs
print("The XML files will be written in the root:{0} directory.".format(directoryXML))
if os.path.exists(directoryXML)==False:
    print("The XML directory was not found. It was created at root:{0}".format(directoryXML))
    os.mkdir(directoryXML)

"""
#############################################################
Parsing the ODTs and extracting their content.xml
#############################################################
"""

if os.listdir(directoryODT)==[]:
    print('No file found in the directory root:{0}'.format(directoryODT))
else:
    for filename in os.listdir(directoryODT):                             # Cycles through all files in the directory
        basename, extension = os.path.splitext(filename)
        fulldir = directoryODT+'\\'+filename                              # Returns absolute path
        if extension == '.odt':                                           # Checks if the file is an ODT. 
                                                                          #Skips to the next file otherwise

            zipped_file = zipfile.ZipFile(fulldir)                        # Opens the zip archive
            index_of_ZIP = zipped_file.infolist()                         # infolist() returns a list with all the files 
                                                                          # contained in the zip archive

            for element_of_list in index_of_ZIP:                          # Cycles through the elements of the list
                if element_of_list.orig_filename == 'content.xml':        # Checks if the file currently pointed is
                                                                          # content.xml, skips to next file otherwise

                    output_path = directoryXML+'\\'+basename+'.xml'       # As content.xml has been found, creates an 
                    output = open(output_path,'w')                        # output file where content.xml will be written
                    
                    file_in_buffer = str(zipped_file.read(element_of_list.orig_filename))  
                                                                          # buffers content.xml as a string

                    file_in_buffer = re.sub('^b\'','',file_in_buffer)     # The buffered files present some leftover 
                    file_in_buffer = file_in_buffer.replace('\\n', '')    # chars from the decompression. These are: 
                    file_in_buffer = re.sub('\'$','',file_in_buffer)      # b'   at the beginning of the file
                                                                          # \n   after the first XML tag
                                                                          # '    at the end of the file
                                                                          # This section of the code removes them.
                            
                    output.write(file_in_buffer)              # Writes the content.xml file in the output folder
                    output.close()                            # The file is named with the same name as the original

            zipped_file.close()    # After having cycled through all the XML files contained in an ODT file, closes it.

    print('Conversion done.')