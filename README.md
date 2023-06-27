# PhonepeDatascrapping
This project created with the phone pe data 
The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.

Libraries/Modules needed for the project!
1.Plotly - (To plot and visualize the data) 2.Pandas - (To Create a DataFrame with the scraped data) 3.mysql.connector - (To store and retrieve the data) 4.Streamlit - (To Create Graphical user Interface) 5.json - (To load the json files) 6.git.repo.base - (To clone the GitHub repository)

Workflow
Step 1:
Importing the Libraries:
Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

!pip install ["Name of the library"]
If the libraries are already installed then we have to import those into our script by mentioning the below codes.

import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine
from streamlit.components.v1 import html
from git.repo.base import Repo
Step 2:
Data extraction:
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

Step 3:
Data transformation:
In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages. And finally load the data in Mysql db

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

Step 4:
Database insertion:
To insert the datadrame into SQL first I've created a script to create new database and tables using "sqlalchemy" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

Creating the connection between python and mysql

and viualise the data in the stream lit api for the user friendly visualisation.

## How to run this application:
Down load the scripts from this repo and save all the script in the same location.
Open command prompt and cd to the directory where scripts are down loaded.
run the below command:
  "python start_phpe.py"
# starrt_phpe.py
This script will start the application by runs the other script in the backend.

# phpeEDA.py
This script will down load the PhonePe data from git repo "https://github.com/PhonePe/pulse.git" and extract the json format data in to dataframe format. 
6 data frame will be created as part of this script. Aggregated transaction, aggregated user, map transaction, map user, top transaction, top user. 
one data is converted to data frame same script will upload the data in to sql database. 
Hope you have the database server installed in your machine. please update the code with your data base password and database name under the line 
#########BElow part is to upload the data into sql data base.###########  in the bottom of code.
*NOTE* -  Please update the database connection URL , database name, its username and password in this script to work according to your envronment.

# streamlitdashboard.py
This Script will create a stream lit dash board . 
Script Reads the data from the data base and create the visulation with dropdown options. 
*NOTE* -  Please update the database connection URL , database name, its username and password in this script to work according to your envronment.

# requirements.txt
This files hold all the required library for this project.
