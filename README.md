

Documentation for Amazon Mechanical Turk Data Filtering
-------------------------------------------------------
-------------------------------------------------------
Alfred Datui, Fang Juping, Matthew Yeo

Introduction
--------------------------------------------------------

This folder contains the necessary tools needed to filter out the data that you want to approve or reject from Amazon Mechanical Turk.

Place this folder in your desktop.


Part 1 : Selecting and Preparing the data for the Image Checking User Interface
----------------------------------------------------------------------------------------

Step 1. Download CSV from the Amazon Mechanical Turk Website

Step 2. (Optional but recommended) Rename the file in this format. 

	Format:	amturk_(the nth round)_(type).csv

	Example: amturk_5_raw.csv, amturk_2_rejected.csv, amturk_1_approved.csv, amturk_6_all.csv

	note: since this is the raw file from the Amazon Mechanical Turk website, name it as amturk_(n)_raw.csv

Step 3. (Optional but recommended) Place the file in the following directory:  

	imageprep\categories\(category)\results

	note: (category) can be 'babycoat' or 'hat' or 'babyshirt' etc.

Step 4. Open Command Prompt and navigate to the folder imageprep

Step 5. Open the Python Script dataprep.py on an editor and make the following changes.

	COMPULSORY: fpath = r'C:\Users\(name)\Desktop\imageprep\categories\babycoat\pictures' (directory of the pictures)
	COMPULSORY: csvpath = r'C:\Users\(name)\Desktop\imageprep\categories\babycoat\results\amturk_5_raw.csv' (directory of the csv file)
	COMPULSORY: results.tocsv('r'C:\Users\(name)\Desktop\imageprep\categories\babycoat\results\amturk_5_raw.csv'') (directory of where you want the saved result to be)

	OPTIONAL: temp = temp[temp['AssignmentStatus'] == ''].reset_index() 

	Change the assignment status to the status that you are interested in. i.e. Submitted, Approved, Rejected

	Or comment out the sentence, if this is the first round and you want all the data.




Part 2 : Approving and Rejecting the Bounding Boxes Drawn by the Amazon Mechanical Turks
----------------------------------------------------------------------------------------

Step 6. Go to imageprep\userinterface and run the Result_check.html on your browser.

Step 7. After loading the HTML file on your browser, to load the .csv file in to the HTML, click "Choose File".

Step 8. Navigate to imageprep\categories\(category)\results and choose the relevant file (Preprocessed by the Python Script)

Step 9. Click 'Accept' if the bounding box matches the criteria and 'Decline' if it does not (Some shorcuts : ","=>Accept, "."=> decline, next=> right arrow, back=> Left arrow, please open the console log to make sure it is correct when you accept and decline ctrl+shift+i-> console).

Step 10. At the last image, The image will not load to another image and the total number which is shown will be maximum.

Step 11. Click 'Download CSV' to get the .csv file.

Step 12. Upload the .csv file onto Amazon Mechanical Turk to have the 'Rejected' results fed back onto the website for another round. 




Part 3: (Optional): Cropping the Images
---------------------------------------

Step 13: Go to imageprep/categories/(category) and create a folder called cropped_(n)_(type)
	In this case, it is cropped_5_submitted. The cropped images of the 5th round of checking that is submitted.

Step 14: Go to imageprep and open image_crop.py in a Python editor and make the following edits.

	fpath = '/Users/(name)/Desktop/imageprep/categories/babycoat/pictures'
	csvpath = '/Users/(name)/Desktop/imageprep/categories/babycoat/results/amturk_5_raw.csv' 
	savepath = '/Users/(name)/Desktop/imageprep/categories/babycoat/cropped_5_submitted/'

Step 15: Open command prompt and run the Python file. 







