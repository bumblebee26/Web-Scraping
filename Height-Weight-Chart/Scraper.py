# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 22:02:45 2019

@author: viren
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import re
import shutil

r = requests.get("https://height-weight-chart.com")
c = r.content #raw text
soup = BeautifulSoup(c,"html.parser")  #html format text

# We can use this and get exact images data,
# but we miss out the html link of each image.
x = soup.find_all("img",{"class":"thumb"})

# This consists of the html link and the height weight info
all = soup.find_all("a")
# Since we know the total images (383), 
# we can select it from the "all" content   386 = (4+383)-1
content = all[3:386]

# Getting the seperate parameters from content
image_link = content[0]['href']
info = content[0].find("img")
text = info.get('title')
src = info.get('src')

# Creating lists for dataframe
title = []
ht_wt = []
file = []
a = len(content)
for i in range(0, a):
    image_link = content[i]['href']
    title = str(title) + ", " + str(image_link)
    
    info = content[i].find("img")
    text = info.get('title')
    text1 = info.get('src')
    ht_wt = str(ht_wt) + ", " + str(text)
    file = str(file) + ", " + str(text1)
    
title = title.split(",")
file = file.split(",")
f = [x.replace('s/', '') for x in file]
file = f
ht_wt = ht_wt.split(",")

path = "https://height-weight-chart.com/"
link = []
link = [path.strip() + x.strip() for x in title]

# Downloading the images 
print("\n\n****Downloading begins****\n\n")

response = requests.get(path)
soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all("img",{"class":"thumb"})
urls = [img['src'] for img in img_tags]

for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg))$', url)
    with open(filename.group(1), 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative 
            # if it is provide the base url which also happens 
            # to be the site variable atm. 
            url = '{}{}'.format(path, url)
        response = requests.get(url)
        f.write(response.content)

print("\n\n****All images are downloaded****\n\n")

# Creating DataFrame
df = pd.DataFrame()
df["Image_link"] = link
df["Filename"] = file
df["Height & Weight"] = ht_wt
df = df.loc[1:]
df.to_csv("Output_data.csv")

print("\n\n****Output CSV file is created****\n\n")