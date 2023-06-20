# -*- coding: utf-8 -*-
"""
Description: Main program for pre-processing of TIC and TOC data for different
             experiments

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    06.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    07.06.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ================
# -- Standard:
import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# Personal:
import lib4sys_support as l4s
import lib4processing as l4p
import lib4visualization as l4v
# ================   User settings (have to be adapted)  ==============
# -- Logical parameters (True / False) --> Important
lmake_folder  = True   # Do you want to automatically create output folder?
lclean_folder = False   # Do you want to clean the previous results in output folder?
lauto_read    = True   # Do you want to read all data from your datafolder?
ldata_quality = True   # Do you want to compare headers in your excel files?
linfo         = False  # Do you want to get more information about your data

# -- Select data (experiment name) --> Important:
exp = 'mh'
#exp = 'ma'
#exp = 'mh-r'

# -- Paths (input and output) --> Important:
main ='/Net/Groups/BGI/people/evchur/scripts/project_tic_toc/DATA/'

# -- Can be the same:
pin  = main
pout = main + 'OUTPUT'
fout = main + f'FIGURES_{exp}'

# -- Select name for output file':
pout_xlsx = pout + f'/data4_{exp}'
pout_stat = pout + f'/stat4_{exp}'
pout_fig  = fout + f'/fig4{exp}'

# -- Settings for excel files:
set4excel = {
    'sheet_name' : 0 ,  # your excel sheet
    'skiprows'   : 10,  # how many rows you want to skip
    'header'     : 1 ,  # line for headers
}

# -- Data visualization:
set4plots = {
    'legends': ['tic', 'toc' ],
    'colors' : ['red', 'blue'],
    'styles' : ['-'  , '-'   ],
    'markers': ['o'  , 'p'   ],
}

# -- Settings for linear plots:
set4line_plot = {
    #      periods color  fsize  lpad  ymin ymax ystep xstep
    'mh'  : [ 25, 'black', 12.0, 20.0, 0.0,141.0, 20.0, 25.0 ],
    'ma'  : [ 10, 'black', 12.0, 20.0, 0.0, 81.0, 10.0, 10.0 ],
    'mh-r': [  5, 'black', 12.0, 20.0, 0.0, 81.0, 10.0,  5.0 ],
}

# -- Settings for scatter plots:
set4scat_plot = {
    #          color  fsize  lpad  xmin  xmax  ymin  ymax
    'mh'   : ['black', 12.0, 20.0, 0.0, 145.0, 0.0, 145.0],
    'ma'   : ['black', 12.0, 20.0, 0.0,  85.0, 0.0,  85.0],
    'mh-r' : ['black', 12.0, 20.0, 0.0,  85.0, 0.0,  85.0],
}

# -- Settings for boxplots:
set4box_plot = {
    #         param    xmin  xmax   ymin  ymax
    'mh'   : {'tic' : [ 0.0, 145.0, 0.0, 145.0],
              'toc' : [ 0.0, 145.0, 0.0,  40.0]},
    'ma'   : {'tic' : [ 0.0,  85.0, 0.0,  85.0],
              'toc' : [ 0.0,  85.0, 0.0,  40.0]},
    'mh-r' : {'tic' : [ 0.0,  85.0, 0.0,  85.0],
              'toc' : [ 0.0,  40.0, 0.0,  40.0]},
}

# -- Filter values for tic and toc --> Important:
tic_filter1 = 1
tic_filter2 = 150
toc_filter1 = 0
toc_filter2 = 25
  
#================   User settings (can be the same)  =======================
#-- Mask for filtering data
exp_mask = f'^{exp}[0-9]' 

#-- Number of intervals
periods = set4line_plot.get(exp)[0]

#-- Output format for:
form_table = '.xlsx'

#-- Plot prefix:
plt_name1 = 1
plt_name2 = 2
# =============================    Main program   =====================
if __name__ == '__main__':

    #-- Part 1. Get filenames and create list with absolute data paths:
    #-- Get all dataset names from the folder:
    if lauto_read == True:
        # Automatic reading
        lst4names = []
        # Iterate directory
        for path in os.listdir(main):
            # check if current path is a file
            if os.path.isfile(os.path.join(main, path)):
                lst4names.append(path)
        lst4names = sorted(lst4names)
    else:
        #-- Manual option.
        lst4names = ['highTOC_Gerighausen_EL5553.xls',
                     'highTOC_Gerighausen_EL5561.xls',
                     'highTOC_Gerighausen_EL5568.xls']

    #-- Get absolute data paths
    lst4paths  = []
    for file in lst4names:
        lst4paths.append(os.path.join(main, file))

    #-- Part 2. Run quality control test (important for the first run)
    if ldata_quality is True:
        l4p.metainfo_control(lst4names, lst4paths, set4excel)

    #-- Part 3. Get data
    #-- Get data from our experiments (only data preprocessing)
    lst4df = []
    for i in range(len(lst4paths)):
        print(lst4names[i])
        lst4df.append(
            l4p.get_data(lst4paths[i], lst4names[i], set4excel, linfo = linfo)
        )

    #-- Get data for experiments
    df_exp = l4p.get_exp_data(lst4df, exp_mask)

    #-- Path 4. Postprocessing
    # -- Make output folders and cleaning previous results:
    l4s.makefolder(pout)      if lmake_folder  is True else print('lmake_folder = False')
    l4s.dep_clean(pout + '/') if lclean_folder is True else print('lclean_folder = False')
    l4s.makefolder(fout)      if lmake_folder  is True else print('lmake_folder = False')
    l4s.dep_clean(fout + '/') if lclean_folder is True else print('lclean_folder = False')
    # -- Save output files for experiment:
    df_exp.to_excel(pout_xlsx + form_table,  sheet_name = f'{exp}_data')

    # -- Part 4.1 Visualization of data (without filter)
    # -- Create special list with 2 series:
    lst4line_plot = [df_exp['ergebnis_tic'], df_exp['ergebnis_toc']]
    # -- Get linear plots
    l4v.line_plots(len(lst4line_plot), lst4line_plot, set4plots, set4line_plot,
                   exp, periods, pout_fig)
    # -- Get scatter plot:
    l4v.scatter_plots(df_exp, set4scat_plot, exp, plt_name1, pout_fig)
    # -- Get boxplot (tic, toc):
    l4v.boxplots(
        df_exp['ergebnis_tic'], 'ergebnis_tic, mg/l',
        pout_fig, 'tic', ylim = (set4box_plot.get(exp).get('tic')[0],
                                 set4box_plot.get(exp).get('tic')[1])
    )
    l4v.boxplots(
        df_exp['ergebnis_toc'], 'ergebnis_toc, mg/l',
        pout_fig, 'toc', ylim = (set4box_plot.get(exp).get('toc')[0],
                                 set4box_plot.get(exp).get('toc')[1])
    )
    # -- Get statistic:
    stat_tic = df_exp['ergebnis_tic'].describe()
    stat_tic.to_excel(pout_stat + f'_tic{form_table}',  sheet_name = f'{exp}_data')

    stat_toc = df_exp['ergebnis_tic'].describe()
    stat_toc.to_excel(pout_stat + f'_toc{form_table}',  sheet_name = f'{exp}_data')

    # -- Part 4.2 Visualization of data (with filters)
    # -- Exclude data (extreme values):
    df_exp2 = df_exp.query(
        'ergebnis_tic > @tic_filter1 and ergebnis_tic <= @tic_filter2 and '
        'ergebnis_toc > @toc_filter1 and ergebnis_toc <= @toc_filter2     ')
    # -- Plot second plots (scratter and boxplots):
    l4v.scatter_plots(df_exp2, set4scat_plot, exp, plt_name2, pout_fig)
    l4v.boxplots(
        df_exp2['ergebnis_tic'], 'ergebnis_tic, mg/l',
        pout_fig, 'tic2', ylim = (set4box_plot.get(exp).get('tic')[2],
                                  set4box_plot.get(exp).get('tic')[3])
    )
    l4v.boxplots(
        df_exp2['ergebnis_toc'], 'ergebnis_toc, mg/l',
        pout_fig, 'toc2', ylim = (set4box_plot.get(exp).get('toc')[2],
                                  set4box_plot.get(exp).get('toc')[3])
    )
    # -- Create dataframe and save it with problem points:
    non_values = np.nan
    df_ext1 = df_exp.query('ergebnis_tic <  @tic_filter1')
    df_ext2 = df_exp.query('ergebnis_tic >= @tic_filter2')
    df_ext3 = df_exp.query('ergebnis_toc <  @toc_filter1')
    df_ext4 = df_exp.query('ergebnis_toc >  @toc_filter2')
    df_prb = pd.concat([df_ext1, df_ext2, df_ext3, df_ext4], axis = 0)
    # -- Save output files:
    df_prb.to_excel(pout_xlsx + f'_prb{form_table}',  sheet_name = f'{exp}_data')
# =============================    End of program   ==================
