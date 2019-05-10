Scrapping project

In this I have scrapped http://court.mah.nic.in/courtweb/index_eng.php 
for get court cases related data such and storing them into csvs 
according to the type of the data.

I have done this project in Linux system particularly Ubuntu 18.04

FOR RUNNING:
tesseract is being used for captcha.

to install use:
$ sudo apt-get install tesseract-ocr

create a python virtual environment
$ conda create -n scrap python=3.7

Note: scrap is the virtual environment name.
then activate this environment

$ conda activate scrap
$ pip install -r requirements.txt
$ python main.py

tesseract is unable of detect the text in the image of captcha 
that's why I am printing the text which is the output from tesseract
and then taking the captcha text input from the user in the terminal.
After the running the above code please enter the captcha text.

The four output files will be saved in the output folder.


***** The flow of the program: *****

selenium is being used to handle the webpage and 
pandas is used to convert the html table into 4 csv

I have made two classes for this Webpage and Table.
Task was to make a few click on the website then a table will be generated in the website and
then seperate the tables and save them to csv.
Using selenium for making clicks using the button/select ids or classs or xpath and then get the table and save it.

Captcha image is also being saved.

Author:
Mohit Musaddi
96mohitm@gmail.com
Website: https://96mohitm.github.io/
Mob: +91 9007578896

Resume: https://96mohitm.github.io//mohit_resume.pdf