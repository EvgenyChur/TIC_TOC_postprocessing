# -*- coding: utf-8 -*-
"""
Description: Get data from MPI-BGC web-page with meteo-information. Create based 
 on downloaded data complex plot (T2m, Prec, Soil Moisture) and 3D plot for SM.

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

# =============================     Import modules     ==================
# 1.1 Standard modules:
import os
from os import listdir
from os.path import isfile, join
import sys
import chardet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1.2 Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4sys_support as l4s
import lib4visualization as l4v
import lib4processing as l4proc
import lib4parsing as l4parse

# =============================   Personal functions   =================
def get_csv_data(
        # Input parameters:
        input_dir:str,                  # Input path         
        filter_keys:list[str],          # Stations 
        # Output parameters:
    ) -> list[pd.Series]:
    """Get input raw data in csv format"""    
    onlyfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    # -- Select data by meteostations:
    for station_id, station in enumerate(filter_keys):
        if station_id == 0:
            st1 = l4proc.str_filter(onlyfiles, station)
        elif station_id == 1:
            st2 = l4proc.str_filter(onlyfiles, station)
        else:
            st3 = l4proc.str_filter(onlyfiles, station)
    
    def add_path(input_dir, ts):
        for i in range(len(ts)):
            ts[i] = f'{input_dir}{ts[i]}'
        return ts
    
    pin_stations = [
        add_path(input_dir, st1),
        add_path(input_dir, st2),
        add_path(input_dir, st3),
    ]
    return pin_stations


def check_data_type(file):
    with open(file, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
    print(result)


def get_data(
        # Input parameters:
        act_path:str,                    # Input path with data
        index_ds:int,                    # index of dataset
        # Output parameters:
    ) -> pd.DataFrame:                   # Daily data

    # -- Files use unusual encoding protocol -> you can get it by this function:
    #check_data_type(act_path)
    # -- Read raw data from csv files:
    df = pd.read_csv(
        act_path, 
        encoding = 'ISO-8859-1',
        skiprows = 0,
        sep=',', 
        header = 0, 
        na_values = ['-9999.99', '-9999', '-9999.00', '********'],
        )
    # -- Check data types:
    #df.info()
    # -- Check column names:
    #print(df.columns)
    # -- Convert time index:
    index = pd.to_datetime(df['Date Time'], format='%d.%m.%Y %H:%M:%S')
    # -- Reset index and drop columns:
    df = (
        df.reset_index(drop = True)
          .set_index(index)
          .drop('Date Time', axis = 1)
    )
    df.index.name = 'time'
    # -- Resample:
    df2 = df
    if index_ds <= 1:
        df2['rain (mm)'] = df['rain (mm)'].resample('1D').sum()
    df2 = df.resample('1D').mean()
    return df2


def get_params_units(
        # Input parameters:
        df,                            # Input data
        # Output parameters:
    ) -> tuple[list[str],              # Actual names of the columns
               list[str],              # Actual parameters (get from columns)
               list[str],              # Actual units (get from  columns)
    ]:
    """Get correct columns, parameters and units"""
    def remove(string):
        return string.replace(" ", "")
    # -- Get actual columns
    cols = df.columns.tolist()
    cols_correct = []
    for i in range(len(cols)):
        cols_correct.append(remove(cols[i]))
            
    # -- split parameters and units by '(' simbol:   
    split_cols = [
        words for segments in cols_correct for words in segments.split('(')]   
    # -- Create new lists for parameters and units:
    units = []
    params = []
    for string in split_cols:
        if string[-1] == ')':
            units.append(string)
        else:
            params.append(string)
    # -- Delete incorrect simbols from units:
    units = [
        item.translate({ord(SYM): None for SYM in '()'} ).strip() for item in units]
    return cols, params, units
        
# ================   User settings (have to be adapted)  =============== 
# -- Locical parameters:
lraw_data = False  # Do you want to download raw meteodata from MPI-BGC web-page?
lmain = True      # Do you want to get daily data and make first time filter?  
lplot = True     # Do you want to plot simple linear plots for all columns? 
                   # (lmain should be set to True)
lsoil = True       # Do you want to get complex plot (t2m, prec, soil moisture)
                   # over small period of time?
lsoil3d = True     # Do you want to get 3D plot for soil moisture? 

# -- Input paths and urls:    
main = 'C:/Users/evchur/Python/scripts/github/tic_toc'      # main folder    
url_mpage = 'https://www.bgc-jena.mpg.de/wetter'            # main url address

# -- Output folder for results:
raw_data  = f'{main}/DATA'

# -- Data filters (key words):
filters  = ['mpi_roof', 'mpi_saale', 'MPI_Soil']
stations = ['WS_Beutenberg', 'WS_Saaleaue', 'Versuchsbeete']

# -- time settings for main mode:
if lmain:
    time_fltr1 = '01.01.2020'
    time_fltr2 = '01.01.2024'
    tformat    = '%d.%m.%Y'
    y1 = pd.to_datetime(time_fltr1, format=tformat)
    y2 = pd.to_datetime(time_fltr2, format=tformat)

# -- user settings for complex plot:
if lsoil:
    # -- Set input data:
    pin_complex_plot = f'{raw_data}/WS_Saaleaue_01.01.2020_01.01.2024.xlsx'   
    # -- Set time filter (first / last date):
    time_fltr3 = '25.07.2023'
    time_fltr4 = '10.08.2023'
    tformat34  = '%d.%m.%Y'
    # -- Set output path for figure:
    fout_complex = f'{raw_data}/complex_plot_Saaleaue_{time_fltr3}_{time_fltr4}.png'
    # -- Set user settings for reading data from xlsx table:   
    uset4sm_data = {
        'tstart' : pd.to_datetime(time_fltr3, format=tformat34),
        'tstop'  : pd.to_datetime(time_fltr4, format=tformat34),
        'levels' : [0.0, -10.0, -20.0, -30.0, -60.0],           # soil levels
        'sm_cols': ['SM008 (%)', 'SM016 (%)',                   # Soil Moisture columns
                    'SM032 (%)', 'SM064 (%)', 'SM128 (%)'],
        't2m_col': ['T (degC)'],                                # T2m column
        'prec_col' : ['rain (mm)'],                             # Precipitation column
        'fout' :  fout_complex,                                 # Output path
    }
    
    '''
    # Potential settings which user can control
    user_settings4plot = {
        'ltitle' : True or False,                 # Do you need plot title?
        'xlabel' : str(),                         # Label for X axis
        'ylabel' : str(),                         # Label for Y axis
        'xlim_time': list[str(date), str(date)],  # Time limits for X axis 
        'xlim_num' : list[num, num, num],         # Numerical limits for X axis
        'ylim_num' : list[num, num, num],         # Numerical limits for Y axis
        'ltick_labels' : True or False,           # Do you want to replace tick labels?
        'llegend' : True or False,                # Do you want to add legend?
        'lgrid' : True or False,                  # Do you want to add grid?
        }
    '''
    # -- User settings for T2m plot:
    t2m_plot_sets = {
        'ltitle' : True,
        'ylabel' : 'T2m, C',
        'xlim_time' : [time_fltr3, time_fltr4],
        'ylim_num'  : [10.0, 30.1, 5.0],
        'llegend' : True,
        'lgrid' : True,
    }
    # -- User settings for Precipitation plot:
    prec_plot_sets = {
        'ylabel' : 'Precipitation, mm',
        'xlim_time' : [time_fltr3, time_fltr4],
        'ylim_num' : [0.0, 20.1, 2.0],
        'llegend' : True,
        'lgrid' : True,
    }
    # -- User settings for Soil Moisture plot:
    sm_plot_sets = {
        'xlabel' : 'SM (Vol. %)',
        'ylabel' : 'Tiefe / Depth (cm)',
        'xlim_num' : [15.0,  50.1,   5.0],
        'ylim_num' : [ 0.0, -70.1, -10.0],
        'ltick_labels' : True,
        'llegend' : True,
        'lgrid' : True,
    }

# -- User settings for complex plot:
if lsoil3d:
    # -- Set input data:
    pin_3d_plot = f'{raw_data}/WS_Saaleaue_01.01.2020_01.01.2024.xlsx'
    # -- Set time filter:
    time_fltr5 = '01.01.2020'
    time_fltr6 = '01.01.2021'
    tformat56  = '%d.%m.%Y'
    smt1 = pd.to_datetime(f'{time_fltr5}', format=tformat56)
    smt2 = pd.to_datetime(f'{time_fltr6}', format=tformat56)
    # -- Set depth values:
    depth = [0.0, -10.0, -20.0, -30.0, -60.0]
    # -- Set columns with soil moisture, Temperature and Precipitation:
    sm_cols  = ['SM008 (%)', 'SM016 (%)', 'SM032 (%)', 'SM064 (%)', 'SM128 (%)']   



# ========================== Start program ==============================
if __name__ == '__main__':
    # -- Create output folder for RAW DATA (if folder not exist):
    pout = l4s.makefolder(f'{raw_data}/RAW_METEO_DATA')
    
    # -- Get table with actual time periods and URL (Preprocessing step):
    if lraw_data:
        data = l4parse.get_data_url(f'{url_mpage}/weather_data.html', filters)
        # -- Download raw data and unzip them:
        l4parse.download_raw_data(pout, data, url_mpage)
    
    # -- Get csv data:
    if lmain:
        pin = get_csv_data(pout, filters)
        
        # Make daily data from 10 minutes data:
        datasets = []
        for ds in range(len(pin)):
            ds_data = []
            for file in range(len(pin[ds])):
                ds_data.append(get_data(pin[ds][file], ds))
            # -- Merge data by time:
            df = (pd.concat(ds_data, axis = 0)
                    .sort_values(by='time', ascending = True))
            # -- Save output files for experiment (full experiment):
            df.to_excel(f'{raw_data}/{stations[ds]}.xlsx')    
           
            # -- Select data for plots and further work:
            df_filter = df[y1:y2]
            
            # -- Create a full time series with data in range:
            ts_full = pd.Series(
                pd.date_range(
                    df_filter.index[0],
                    df_filter.index[-1], 
                    freq = '1d',
                ), name = 'time'
            )
            # -- Reset index in filter data 
            df_filter = df_filter.reset_index()
            # -- Create a new dataframe with correct time steps:
            df_filter2 = (
                df_filter
                    .merge(ts_full, how='outer')
                    .sort_values(by='time', ascending = True)
                    .set_index('time')
            )
            # -- Save output files for experiment (filter experiment):
            df_filter2.to_excel(
                f'{raw_data}/{stations[ds]}_{time_fltr1}_{time_fltr2}.xlsx')
            
            # -- Create linear plots with filter data:
            if lplot:
                # -- Create 2 new lists with parameter name and unit
                cols, params, units = get_params_units(df_filter2)

                fout = l4s.makefolder(f'{raw_data}/{stations[ds]}')
                for i,col in enumerate(cols):
                    fig = plt.figure(figsize = (12,7))
                    ax  = fig.add_subplot(111)
                    ax.plot(df_filter2.index, df_filter2[f'{col}'])
                    plt.savefig(f'{fout}{params[i]}.png', format = 'png', dpi = 300) 
                    plt.close(fig)        
                    plt.gcf().clear()            
    
    # -- Create complex plot for short period of time (1 month - maximum):      
    if lsoil:
        # -- Get input data:
        df = pd.read_excel(pin_complex_plot)
        l4v.complex_plot(
            df,              # research dataset
            uset4sm_data,    # user settings for research data
            t2m_plot_sets,   # user settings for t2m plot
            prec_plot_sets,  # user settings for precipitation plot
            sm_plot_sets,    # user settings for soil moisture plot
        )
    
    if lsoil3d:
        # -- Get input data:
        df = pd.read_excel(pin_3d_plot)
        # -- Reset time intex and take columns only with soil moisture:
        df['time'] = pd.to_datetime(df['time']).dt.date
        # -- Get data:
        df_soil = df.set_index('time')[sm_cols][smt1:smt2]
        df_soil = df_soil.reset_index()
        # -- Get list of actual columns (exclude column with time)
        cols = df_soil.columns.tolist()[1:]
        
        # -- Create 3D plot:
        fig = plt.figure(figsize = (14, 10))
        ax = fig.add_subplot(projection='3d')
        
        colors = ['r',  'g',  'b',  'y', 'black']
        yticks = [0.0, 10.0, 20.0, 30.0, 60.0   ]
        for i,k in enumerate(yticks):
            print(i,k)
            # Generate the random data for the y=k 'layer'.
            xs = df_soil['time'].index
            ys = df_soil[cols[i]]
              
            # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
            ax.plot(xs, ys, zs=k, zdir='y', alpha=0.8, label = cols[i]) #, color=cs)
        ax.legend()
        
        taxis = pd.date_range(time_fltr5, time_fltr6, freq = '1d')
        taxis2 = change_format = taxis.strftime(tformat56)
        
        ax.set_xticklabels(taxis2)

        
        for label in ax.xaxis.get_ticklabels():
            label.set_color('black')
            label.set_rotation(45)
            label.set_fontsize(12)    
        
        #ax.set_xlabel('Moment of time')
        ax.set_xlabel('Time', color = 'b', fontsize = 12,labelpad = 50)
        ax.set_ylabel('Tiefe / Depth (cm)', color = 'b',fontsize = 12,labelpad = 20)
        ax.set_zlabel('SM (Vol. %)', color = 'b', fontsize = 12,labelpad = 20)
        

        # On the y-axis let's only label the discrete values that we have data for.
        ax.set_yticks(yticks)
        #plt.show()
        fout = f'{raw_data}/sm_3d.png'
        plt.savefig(fout, format = 'png', dpi = 300)
        plt.close(fig)
        plt.gcf().clear()        
      