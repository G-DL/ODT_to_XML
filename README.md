# ODT_to_XML
This script converts multiple odt files provided as in an input folder to the xml files which hold their content. 
It was written to automate the extraction of content from odt files, and to facilitate the subsequent parsing of the content itself. 

This is how the script works:
1) Place all odt files to be converted in root:\ODTfolder
2) Run the script
3) The converted files are now located in root:\XMLfolder

Feel free to customise this script for your own necessities. 
Also, please note that if any of the original files contain a string '\n' this string WILL be removed from the converted files.
It is either this, or the converted file would return a parsing error with most standard xml parsers. Further details are given in the comments of the source code, but you have been warned.
