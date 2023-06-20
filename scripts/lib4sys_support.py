# -*- coding: utf-8 -*-
"""
Task : Library for work with file system

Autors of project: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    11.11.2022 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    03.03.2023 Evgenii Churiulin, MPI-BGC
           Add new function 3.
    1.2    07.06.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     =================
import os
import pandas as pd
# =============================   Personal functions   =================
# -- dep_clean --> Cleaning previous results
def dep_clean(
        # Input variables:
        path:str                # Path to the folder with results.
        # Output variables:
    ):
    for file in os.listdir(path):
        os.remove(path + file)

# -- makefolder --> Check and create folder:
def makefolder(
        # Input variables:
        path:str,               # Output path folder.
        # Output variables:
    ) -> str:                   # Output path
    # -- Create folder for output data
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path + '/'

# get_info --> Get common information about datasets
def get_info(
        # Input variables:
        df:pd.DataFrame,        # Research dataframe
        df_name:str,            # Name of the research dataset
        # Output variables:
    ):                          # Print information about dataset in command window
    # -- Get commot info:
    print(f'Common information about - {df_name}')
    df.info()
    print(df.columns, '\n')
    print(f'Numbers of NaN values in the dataset - {df_name}', '\n')
    print(df.isnull().sum())
    print(f'Numbers of duplicates (explicit)in the dataset - {df_name}', '\n')
    print(df.duplicated().sum())
