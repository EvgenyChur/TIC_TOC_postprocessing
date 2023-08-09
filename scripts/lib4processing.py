# -*- coding: utf-8 -*-
"""
Description: Personal module for preprocessing functions

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    04.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    07.06.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring
    1.3    09.08.2023 Evgenii Churiulin, MPI-BGC
           Add new function for data processing
"""

# =============================     Import modules     =======================
# -- Standard:
import os
import sys
import numpy as np
import pandas as pd
from re import match
from typing import Optional
import warnings
warnings.filterwarnings("ignore")
# 1.2: Personal modules
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4sys_support

# =============================   Personal functions   =======================

# --  metainfo_control ->  Fast quality control test. Headers in files should be the same!
def metainfo_control(
        # Input variables:
        ds_names:list[str],                 # Excel file names
        ds_paths:list[str],                 # Excel file input paths
        set4excel:dict,                     # Excel file settings
        # Output variables:
    ):                                      # Function print text or stop program

    #-- Check headers from 2 different datasets
    for i in range(len(ds_names)):
        if i + 1 <= len(ds_names) - 1:
            #-- Columns from the first dataset:
            col_df1 = (
                pd.read_excel(
                    ds_paths[i],
                    #-- Settings for reading .xls files
                    sheet_name = set4excel.get('sheet_name'),
                    skiprows   = set4excel.get('skiprows'),
                    header     = set4excel.get('header'),
                ).columns.to_list()
            )
            #-- Columns from the second dataset:
            col_df2 = (
                pd.read_excel(
                    ds_paths[i + 1],
                    #-- Settings for reading .xls files
                    sheet_name = set4excel.get('sheet_name'),
                    skiprows   = set4excel.get('skiprows'),
                    header     = set4excel.get('header'),
                ).columns.to_list()
            )
            #-- Check columns
            if col_df1 == col_df2:
                print(f'Header in {ds_names[i]} and {ds_names[i+1]} is the same')
            else:
                print(f'Header in {ds_names[i+1]} is different')
                sys.exit()
# ------------------------------------------------------------------------------

# -- get_data --> Preprocessing of excel data
def get_data(
        # Input variables:
        pin:str,                            # Excel file input paths
        df_name:str,                        # Excel file names
        set4excel:dict,                     # Excel file settings
        linfo: Optional[bool] = True,       # Do you want to get more information about data?
        # Output variables:
    ) -> pd.DataFrame:                      # Preprocessed data collected in one dataframe
    # -- Local variables:
    # Data types for columns:
    int4col = 'int32'
    flt4col = 'float'
    dat4col = '%Y-%m-%d'

    #-- Read data (excel file should have the same structure):
    df = pd.read_excel(
        pin,
        sheet_name = set4excel.get('sheet_name'),
        skiprows = set4excel.get('skiprows'),
        header = set4excel.get('header'),
    )
    # -- Get first information about data:
    if linfo == True:
        lib4sys_support.get_info(df, df_name)
    #-- Rename colums (all columns name should be in one register):
    for col in df.columns.to_list():
        df = df.rename(columns={col : col.lower()})
    #-- Change type of data for columns (if it is needed):
    # a. In columns (probenjahr and nummer - type int64 --> change to int32):
    df['probenjahr'] = df['probenjahr'].astype(int4col)
    df['nummer'] = df['nummer'].astype(int4col)
    # b. In columns (ergebnis - type object --> change to float):
    #   Check why we have this problem
    def check_data(row):
        return isinstance(row['ergebnis'], float)

    df['lcheck'] = df.apply(check_data, axis = 1)
    df = (df.loc[df.loc[:,'lcheck'] == True]
            .drop('lcheck', axis = 1)
    )
    df['ergebnis'] = df['ergebnis'].astype(flt4col)
    # c. Change register for all columns with object type:
    for col in df.loc[:, df.dtypes == object]:
        df[col] = df[col].str.lower()
    # d. Change time format in messdatum and probennahmedatum columns:
    df['messdatum'] = pd.to_datetime(df['messdatum'], format = dat4col)
    df['probennahmedatum'] = pd.to_datetime(df['probennahmedatum'], format = dat4col)
    # e. Delete space from probennamen:
    def space(row):
        return row['probenname'].replace(" ", "")
    df['probenname'] = df.apply(space, axis = 1)

    #-- We should ignore experiments with "Verdünnung prefix' in kommentar
    """
    def space(row):
        return row['kommentar'].replace(" ", "")
    df['kommentar'] = df.apply(space, axis = 1)

    #-- Split text to columns
    df['exp' ] = (
        df['kommentar'].str.split(r";", expand = True)
                       .loc[:,[0]]
                       .rename(columns = {0 : 'exp'})
    )

    try:
        df['verd'] = (
            df['kommentar'].str.split(r";", expand=True)
                           .loc[:,[1]]
                           .rename(columns = {1 : 'verd'})
                           .fillna(value='ndata')
        )
    except KeyError:
        print('In dataset (field - kommentar) there is no data with simbol ;')
        def nan_data(row):
            return 'ndata'
        df['verd'] = df.apply(nan_data, axis = 1)

    #-- Select only original data
    df = (df.loc[df.loc[:,'verd'] == 'ndata']
            .drop(['verd', 'exp'], axis = 1)
    )
    """
    # -- Delete columns which we don't want to use:
    df = df.drop(['nummer', 'instrument', 'messdatum'], axis = 1)
    # -- Add additional column with excel file name:
    exp_name = (
        pd.Series(np.nan, index = df.index)
          .replace(np.nan, df_name)
          .rename('excel_doc')
    )
    df = pd.concat([df, exp_name], axis = 1)
    # -- Additional quality control (We have columns with NaN values, but at
    #    this step it is fine and we delete such columns later, otherwise we can,
    #    get different number of columns).
    if linfo == True:
        lib4sys_support.get_info(df, df_name)
    return df
# ------------------------------------------------------------------------------

# -- select_data --> Select data based on parameter and get avarage values
def select_data(
        # Input variables:
        df:pd.DataFrame,                    # Research data collected in one dataframe
        param:str,                          # Research parameter (TIC or TOC)
        # Output variables:
    ) -> pd.DataFrame:                      # Research data after processing
    # -- Select data based on parameter:
    var = param
    df = df.query('parameter == @var').reset_index(drop = True)
    # -- Settings for groupby method:
    dct = {
        'probenjahr': 'mean',
        'ergebnis'  : 'mean',
        'einheit'   :  lambda col: col.mode() if col.nunique() == 1 else np.nan,
        'vermuffelt':  lambda col: col.mode() if col.nunique() == 1 else np.nan,
        'kommentar' :  lambda col: col.mode() if col.nunique() == 1 else np.nan,
        'probennahmedatum': 'mean',
        'excel_doc' :  lambda col: col.mode() if col.nunique() == 1 else np.nan,
    }
    # -- Groupby data:
    df_agg = (
        df.groupby(['probenname','parameter'])
          .agg(**{k: (k, v) for k, v in dct.items()})
    )
    return df_agg
# ------------------------------------------------------------------------------

# -- get_exp_data --> Get average data for tic and toc experiments presented
#                     for your experiment.
def get_exp_data(
        # Input variables:
        list4df:list[pd.DataFrame],         # List of dataframes with preprocessed data.
        mask:str,                           # Filter for searching data from your selected experiment.
        # Output variables:
    ) -> pd.DataFrame:                      # Data for your selected experiment
    # -- Local variables:
    tic_param = 'tic'
    toc_param = 'toc'
    sort_col = 'probenname'
    merge_type = 'outer'
    # -- Get all data in one dataframe:
    df = (
        pd.concat(list4df, axis = 0)
          .reset_index(drop = True)
          .dropna(axis = 1, how = 'all')
    )
    # -- Selected data based on parameters (tic and toc):
    df_tic = (
        select_data(df, tic_param)
           .sort_values(sort_col, ascending = False)
           .reset_index(drop = False)
    )
    df_toc = (
        select_data(df, toc_param)
           .sort_values(sort_col, ascending = False)
           .reset_index(drop = False)
    )
    #-- Merge data
    df_merge = df_tic.merge(
        df_toc[['probenname', 'probennahmedatum', 'ergebnis',
                'probenjahr', 'kommentar', 'parameter'       ]],
        on  = ['probenname' , 'probennahmedatum', 'probenjahr'],
        how = merge_type
    )
    # -- if you want to use other data you can uncomment this line
    #print(df_merge.columns, '\n')
    df_merge = (
        # -- Reorder columns in dataframe
        df_merge.loc[:, [
            'probenname' , 'probenjahr', 'parameter_x', 'ergebnis_x' ,
            'parameter_y', 'ergebnis_y', 'kommentar_x', 'kommentar_y',
            'probennahmedatum'         , 'einheit'    , 'vermuffelt' ,
            'excel_doc']]
        # -- Sort values by probenname
                .sort_values(['probenname'], ascending = False)
        # -- Reset index (drop = True - delete old columns with indexes)
                .reset_index(drop=True)
    #-- Rename columns
    ).rename(columns = {
        'ergebnis_x' : 'ergebnis_tic',
        'ergebnis_y' : 'ergebnis_toc'
        }
    #-- Drop columns
    ).drop(['parameter_x', 'parameter_y'], axis = 1)
    #-- Split data by experiments
    df_exp = (
        df_merge.loc[df_merge.probenname.str.contains(mask), :]
                .sort_values(sort_col, ascending = True)
                .reset_index(drop = True)
    )
    return df_exp
# ------------------------------------------------------------------------------


# get_data4akanksha -> Preprocessing of excel data (task for Akanksha)
def get_data4akanksha(
        # Input variables:
        pin:str,                      # Input data path
        df_name:str,                  # Input dataframe name (name of excel file) 
        set4excel:dict,               # Set of settings for reading excel data
        linfo: Optional[bool] = True, # Do you want to get more information about your data?
        # Output variables:
        ) -> pd.DataFrame :           # Data after pre-processing
    # -- Data types for columns:
    flt4col = 'float'
    dat4col = '%Y-%m-%d'
    #-- Read data (excel file should have the same structure):
    df = pd.read_excel(
        pin,
        sheet_name = set4excel.get('sheet_name'),
        skiprows   = set4excel.get('skiprows'),
        header     = set4excel.get('header'),
    )
    # -- Get first information about data:
    if linfo == True:
        lib4sys_support.get_info(df, df_name)
    # -- Rename colums (all columns name should be in one register):
    for col in df.columns.to_list():
        df = df.rename(columns={col : col.lower()})
    # -- Change data types for columns (if it is needed):  
    # -- a. In columns probenjahr and nummer change type int64 to str.
    #       Create new column analysis_nummer based on them:
    df['probenjahr'] = df['probenjahr'].astype(str)
    df['nummer'] = df['nummer'].astype(str)
    df['analysis_nummer'] = df.probenjahr.str.cat(df.nummer, sep='_')
    # -- b. In columns: change ergebnis type from type object to float:
    #   Important: Check why we have text in this column!!!!
    def check_data(row):
        return isinstance(row['ergebnis'], float)
    df['lcheck'] = df.apply(check_data, axis = 1)
    df = (df.loc[df.loc[:,'lcheck'] == True]
            .drop('lcheck', axis = 1)
    )
    df['ergebnis'] = df['ergebnis'].astype(flt4col)
    # -- c. Change time format in messdatum and probennahmedatum columns:
    df['messdatum'] = pd.to_datetime(df['messdatum'], format = dat4col)
    df['probennahmedatum'] = pd.to_datetime(df['probennahmedatum'], format = dat4col)
    # -- d. Delete space from probennamen:
    def space(row):
        return row['probenname'].replace(" ", "")
    df['probenname'] = df.apply(space, axis = 1)
    # -- e. Change register for all columns with object type
    for col in df.loc[:, df.dtypes == object]:
        df[col] = df[col].str.lower()
    # -- Get information from "kommentar'
    # -- a. Delete spaces:
    def space(row):
        return row['kommentar'].replace(" ", "")
    df['kommentar'] = df.apply(space, axis = 1)
    # -- b. Get new column 'plot':
    df['plot'] = (
        df['kommentar'].str.split(r"/", expand = True).loc[:,[0]].rename(columns = {0 : 'plot'})
    )
    try:
        # -- Temporal step:
        df['temp'] = (
            df['kommentar'].str.split(r"/", expand = True).loc[:,[1]].rename(columns = {0 : 'temp'})
        )
    except:
        print('In dataset (field - kommentar) there is no data with simbol /')
        df['temp'] = df['kommentar']
    # -- Get new column 'depth':
    df['depth'] = (
        df['temp'].str.split(r";", expand = True).loc[:,[0]].rename(columns = {0 : 'depth'})
    )
    # -- Get new column 'kommentar':
    try:
        df['kommentar'] = (
            df['temp'].str.split(r";", expand=True)
                           .loc[:,[1]]
                           .rename(columns = {1 : 'kommentar'})
                           .fillna(value='ndata')
        )
    except KeyError:
        print('In dataset (field - kommentar) there is no data with simbol ;')
        def nan_data(row):
            return 'ndata'
        df['kommentar'] = df.apply(nan_data, axis = 1)
    # -- Select data which we want to use:
    df_final = (
        df.loc[:, [
            'probenname'     , 'probennahmedatum', 'plot'    , 'depth'    ,
            'analysis_nummer', 'parameter'       , 'ergebnis', 'messdatum', 
            'kommentar'      ,
            ]
        ]
    )
    # -- Add additional column with excel file name:
    exp_name = (
        pd.Series(np.nan, index = df.index)
          .replace(np.nan, df_name)
          .rename('excel_doc')
    )
    # -- Add new column to dataframe:
    df_final = pd.concat([df_final, exp_name], axis = 1)
    return df_final


def get_complex_plot_data(
        # Input variables:
        df:pd.DataFrame,                    # Input data from meteostation
        uset4data:dict,                     # User parameters for dataset
        # Output variables:
    ) -> tuple[pd.DataFrame,               # T2m data
               pd.DataFrame,               # Precipitation data
               pd.DataFrame,               # Soil moisture data
    ]:
    # -- Local variables:
    t1 = uset4data.get('tstart')
    t2 = uset4data.get('tstop')
    depth = uset4data.get('levels')
    t2m_col = uset4data.get('t2m_col')
    prec_col = uset4data.get('prec_col')
    sm_cols  = uset4data.get('sm_cols')

    # -- Reset time intex and take columns only with soil moisture:
    df['time'] = pd.to_datetime(df['time']).dt.date
    # -- Get data:
    df_temp = df.set_index('time')[t2m_col][t1:t2]
    df_prec = df.set_index('time')[prec_col][t1:t2]
    df_soil = df.set_index('time')[sm_cols][t1:t2].T
    df_soil['depth'] = depth
    df_soil = df_soil.reset_index(drop = True).set_index('depth')
    return df_temp, df_prec, df_soil


def str_filter(
        # Input variables:
        lst4filter:list[str],
        flt_word:str,
        # Output variables:
    ) -> list[pd.Series]:
    """Select stations by flt_word"""
    return list(filter(lambda v: match(flt_word, v), lst4filter))
# =============================    End of program   ==========================
