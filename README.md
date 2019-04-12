# final_year_project
This project is about "Automated Analysis of the Research Output of Computer Science Departments in the UK" which includes data collection from Google Scholar, data manipulation and visualisation.

# General Discription
This project allows you to collect citation data with specific year range from Google Scholar by a given staff list using API "scholarly". Then calculate h-index by collected citation data. There are some staff list and a decent result which is a re-rank of the UK's top30 universities at REF 2014 by their computer science academic staff’s citation data from 2015 to 2019.

# Read the Result
The result of this project which is a csv file is recommended to be read by jupyter notebook since it provides a better view than Pycharm console.
In order to read the result, add 

    import pandas as pd
    df1 = pd.read_csv('FinalResult_pattern1.csv')
    df1 = df1.drop('Unnamed: 0',1)
    df1

to jupyter notebook(if you are using other ide just add print() function to print df1).

If you are insterested in some citation data for a university please use following code on jupyter notebook.

    import pandas as pd
    df3 = pd.read_csv('uniData\\University of Liverpool.csv')
    df3 = df3.drop('Unnamed: 0',1)
    df3

In this way, you can access the staffs' citation data in University of Liverpool.

Explaination: "hhindex" in the FinalResult represent the staff h-index of the whole department. e.g.: hhindex is 13 for UCL means there are at least 13 staff whose h-index is greater than 13 at UCL.

# File Discription
  # GoogleQuery.py:
   Collect staff list from university website using google query for the website.
   Caution! It will override the existing list and it can not collect staff list from most university since it only contains one pattern of regular expression.
    
   # GoogleScholarQuery.py:
   Perform google scholar query to get citation data then calculate the h-index.
    
   # DataProcess.py:
   Manipulate collected data then store the final result into a csv file.
    
# Installation
If you are intend to use this repo please make sure you've install the library that is used in this project.

    pip install scholarly

    pip install BeautyfulSoup

scholarly is used in GoogleScholarQuery.py
BeautyfulSoup is used in GoogleQuery.py
