# -*- coding: utf-8 -*-
"""
Description: Preprocessing data for Akanksha.

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    %(date) Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    07.06.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# -- Standard:
import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# -- Personal:
import lib4sys_support as l4s
import lib4processing as l4p
# ================   User settings (have to be adapted)  ================
# -- Logical parameters (True / False) --> Important
lmake_folder  = True   # Do you want to automatically create output folder?
lclean_folder = False   # Do you want to clean the previous results in output folder?
lauto_read    = True   # Do you want to read all data from your datafolder?
ldata_quality = False   # Do you want to compare headers in your excel files?
linfo         = False  # Do you want to get more information about your data

# -- Select data (experiment name) --> Important
exp = 'mh'
#exp = 'ma'
#exp = 'mh-r'

# -- Mask for filtering data
exp_mask = f'^{exp}[0-9]' 

# -- Paths (input and output) --> Important
#main ='C:/Users/evchur/RESULTS/ALINA'
main ='D:/data4python/'
# -- Can be the same
#pin  = main + '/INPUT'
pin = main
pout = main + '/OUTPUT'

# -- Select name for output file'
pout_xlsx = pout + f'/data4_{exp}'
# -- Output format for:
form_table = '.xlsx'

# -- Settings for excel files
set4excel = {
    'sheet_name' : 0 ,  # your excel sheet
    'skiprows'   : 10,  # how many rows you want to skip
    'header'     : 1 ,  # line for headers
}

# =============================    Main program   =======================
if __name__ == '__main__':
    # -- Part 1. Get filenames and create list with absolute data paths:
    # Automatic reading:
    if lauto_read is True:
        lst4names = []
        for path in os.listdir(main):
            if os.path.isfile(os.path.join(main, path)):
                lst4names.append(path)
        lst4names = sorted(lst4names)
    # Manual option:
    else:
        lst4names = ['highTOC_Gerighausen_EL5568.xls',
                     'highTOC_Gerighausen_EL5553.xls']
    # Get absolute data paths:
    lst4paths  = []
    for file in lst4names:
        lst4paths.append(f'{pin}/{file}')

    # -- Part 2. Run quality control test (important for the first run):
    if ldata_quality is True:
        l4p.metainfo_control(lst4names, lst4paths, set4excel)

    # -- Part 3. Get data:
    # Get data from our experiments (only data preprocessing):
    lst4df = []
    for i in range(len(lst4paths)):
        print(lst4names[i])
        lst4df.append(
            l4p.get_data4akanksha(lst4paths[i], lst4names[i], set4excel, linfo = linfo)
        )
    # -- Create new dataframe and sort values by probenname:
    df_data = (
        pd.concat(lst4df, axis = 0)
          .sort_values(['probenname'], ascending = True)
          .reset_index(drop = True)
    )
    # -- Split data by experiments:
    df_exp = (
        df_data.loc[df_data.probenname.str.contains(exp_mask), :]
               .sort_values('probenname', ascending = True)
               .reset_index(drop = True)
    )
    df_exp['depth'] = df_exp['depth'].astype(int)

    # -- Path 4: Make output folder and cleaning previous results:
    l4s.makefolder(pout)      if lmake_folder  is True else print('lmake_folder = False')
    l4s.dep_clean(pout + '/') if lclean_folder is True else print('lclean_folder = False')
    # -- Save output files for experiment:
    df_exp.to_excel(pout_xlsx + form_table,  sheet_name = f'{exp}_data')
# =============================    End of program   ======================
