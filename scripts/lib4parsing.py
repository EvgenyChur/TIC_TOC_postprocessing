# -*- coding: utf-8 -*-
"""
Description: Module for parsing meteodata for MPI-BGC web-page

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    09.08.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     =======================
# 1.1: Standard modules
import os
import sys
import io
import requests
import zipfile
from bs4 import BeautifulSoup
from re import match
import numpy as np
import pandas as pd
from typing import Optional
import warnings
warnings.filterwarnings("ignore")

# 1.2 Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4processing as l4proc

# =============================   Personal functions   =======================

# Create table with actual URLs with ZIP achives available at MPI-BGC web-page:
def get_data_url(
        url:str,                           # URL web-page
        filter_keys:list[str],             # Common file names for meteostations
    ) -> list[pd.DataFrame]:               # Tables with meta-information from URL
    """Get actual url adresses for input data"""
    # -- Local variables:
    tag4col_names   = 'b'
    tag4url_names   = 'a'
    tag4url_element = 'href'

    # Start program:
    # Make URL request for the main web-page:
    req = requests.get(url)
    # Print status request: (200 - Ok)
    print('Server status request is', req.status_code)

    soup = BeautifulSoup(req.text, 'lxml')
    # -- Get table with our data:
    table=soup.find_all('table')[1]

    # -- List with columns names:
    heading_table = []
    for row in table.find_all(tag4col_names):
        heading_table.append(row.text)

    # -- Get list with names for time periods:
    names = []
    for row in table.find_all('tr'):
        if not row.find_all(tag4col_names):
            names.append([element.text for element in row.find_all('td')])

    def get_names(lst4data):
        lname = lst4data.splitlines(True)[1:]
        # remote new lines:
        for i in range(len(lname)):
            lname[i] = lname[i].strip()
        return lname

    period_names = [
        get_names(names[0][0]),
        get_names(names[0][1]),
        get_names(names[0][2]),
    ]

    # -- Get List with URL content for relevant stations and time periods:
    content = [
        element[tag4url_element] for element in table.find_all(tag4url_names, href=True)
    ]
    # -- Create output tables:
    data = []
    for i in range(len(filter_keys)):
        data.append(
            pd.Series(
                l4proc.str_filter(content, filter_keys[i]),
                index = period_names[i],
                name  = 'url',
            ).reset_index().rename(columns = {'index':f'time_period_{heading_table[i]}'})
        )
    return data


def download_raw_data(
        # Input parameters:
        output_path:str,                # Output path
        data:list[pd.DataFrame],        # Table with meta-information
        url:str,                        # URL web-page
        # Output parameters:
    ):                                  # save data as csv in output folder
    """Get raw meteorological data in csv format from MPI-BGC web-page"""
    for i in range(len(data)):
        for row in range(len(data[i])):
            url_prefix = data[i]['url'][row]
            file_url = f"{url}/{url_prefix}"
            r = requests.get(file_url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(output_path)

# =============================    End of program   ==========================