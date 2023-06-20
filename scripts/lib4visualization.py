# -*- coding: utf-8 -*-
"""
Description: Module with functions for visualization
    1. line_plots    --> create linear plot
    2. scatter_plots --> create scatter plot with regression line
    3. boxplots      --> create boxplot

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
# =============================     Import modules     =====================
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from scipy import stats
# =============================   Personal functions   =====================

# line_plots --> Create a line plot with for tic and toc experiments devided by periods
def line_plots(
        # Input variables:
        lines_count:int,                  # Numbers of lines, which you want to plot
        data:list[pd.Series],             # Research data presented as list of timeseries
        plt_set:dict,                     # Plot settings (legend, colors, style)
        set4line_plot:dict,               # Plot settings (fontsize, pads, limits)
        mask:str,                         # Experiment id
        periods:str,                      # Number of iterations (plots)
        pout:str,                         #  Output path
        # Output variables:
    ):                                    # Create figures in output folder
    # -- Local variables (Plot settings):
    ptitle = 'Linear plot for comparison tic and toc data'
    xlabel = 'Points'
    ylable = 'tic/toc, mg/l'
    clr    = set4line_plot.get(mask)[1]
    fsize  = set4line_plot.get(mask)[2]
    lpab   = set4line_plot.get(mask)[3]  
    y_min  = set4line_plot.get(mask)[4]
    y_max  = set4line_plot.get(mask)[5]
    y_step = set4line_plot.get(mask)[6]
    x_step = set4line_plot.get(mask)[7]
    # -- Get ranges
    if len(data[0]) == len(data[1]):
        step = (len(data[0]) + 1) / periods
        ranges = np.arange(len(data[0]) - len(data[0]), len(data[0]) + 1, step)
    else:
        sys.exit('data len is different')
    # -- Create plots:
    for i in range(periods):
        if i+1 <= periods - 1:
            fig = plt.figure(figsize = (12,7))
            ax  = fig.add_subplot(111)
            y1 = int(ranges[i])
            y2 = int(ranges[i+1])
            for i in range(lines_count):
                ax.plot(
                    data[i][y1:y2].index,
                    data[i][y1:y2],
                    label = plt_set.get('legends')[i],
                    color = plt_set.get('colors')[i],
                    linestyle = plt_set.get('styles')[i],
                )
            # -- Add plot legend and titles:
            ax.legend()
            ax.set_title(ptitle,  color = clr, fontsize = fsize, pad      = lpab)
            ax.set_xlabel(xlabel, color = clr, fontsize = fsize, labelpad = lpab)
            ax.set_ylabel(ylable, color = clr, fontsize = fsize, labelpad = lpab)
            # -- Get x and y ticks parameters:
            ax.set_yticks(np.arange(y_min, y_max, y_step))
            ax.set_xticks(np.arange(y1, y2, x_step ))
            # -- Grid settings
            ax.grid(True, which='major', color='grey', linestyle='dashed', alpha=0.2)
            #-- Plot save
            plt.savefig(pout + f'_in_range_{y1}_{y2}.png', format='png', dpi = 300) 
            #-- Clean memory
            plt.close(fig)        
            plt.gcf().clear()

# -- scatter_plots --> Create scatter plot:
def scatter_plots(
        # Input variables:
        data:pd.DataFrame,                # Data for visulaization
        set4scat_plot:dict,               # Plot settings (fontsize, pads, limits)
        mask:str,                         # Experiment id
        num:int,                          # Additional prefix for plots
        pout:str,                         # Output path
        # Output variables:
    ):                                    # create figures in your output folder
    # -- Plot settings:
    ptitle = 'Correlation plot of ergebnis_tic and ergebnis_toc data'
    xlabel = 'ergebnis_tic, mg/l'
    ylabel = 'ergebnis_toc, mg/l'
    clr   = set4scat_plot.get(mask)[0]
    fsize = set4scat_plot.get(mask)[1]
    lpab  = set4scat_plot.get(mask)[2]
    x_min = set4scat_plot.get(mask)[3]
    x_max = set4scat_plot.get(mask)[4]    
    y_min = set4scat_plot.get(mask)[5]
    y_max = set4scat_plot.get(mask)[6]
    # -- Create plot area:
    fig = plt.figure(figsize = (12, 7))
    ax  = fig.add_subplot(111) 
    ax.scatter(
        data['ergebnis_tic'],
        data['ergebnis_toc'],
        s = 60,
        alpha = 0.6,
        edgecolors = "k",
    )
    # -- Get y ticks parameters:
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    # -- Labels:
    ax.set_title(ptitle , color = clr, fontsize = fsize, pad      = lpab)
    ax.set_xlabel(xlabel, color = clr, fontsize = fsize, labelpad = lpab)
    ax.set_ylabel(ylabel, color = clr, fontsize = fsize, labelpad = lpab)
    #-- Grid settings:
    ax.grid(True, which='major', color='grey', linestyle = 'dashed', alpha = 0.2)
    # -- Plot regression line:
    data = data.dropna()
    slope, intercept, r_value, p_value, std_err = (
        stats.linregress(data['ergebnis_tic'],
                         data['ergebnis_toc'])
    )
    line = slope * data['ergebnis_tic'] + intercept
    ax.plot(
        data['ergebnis_tic'],
        line, 
        color="red", 
        lw=2.5, 
        label='y={:.2f}x+{:.2f}'.format(slope,intercept)
    )
    # -- Add legend
    plt.legend(fontsize=9)
    # -- Save plot and clean memory:
    plt.savefig(pout + f'_correlation_{num}.png', format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()  

# -- boxplots --> Create boxplot based on our research data
def boxplots(
        # Input variables:
        df:pd.DataFrame,                 # Research data
        col:str,                         # Name of the column for boxplot
        pout:str,                        # Output path
        name:str,                        # Boxplot output prefix name
        **kwargs,                        # Additional parameters for plot
        # Output variables:
    ):                                   # Create figures in your output folder
    # -- Create plot:
    fig = plt.figure(figsize = (12, 7))
    ax  = fig.add_subplot(111) 
    df.plot(
        y = col,
        title = col,
        kind = 'box',
        ax = ax,
        grid = True,
        **kwargs,
    )
    # -- Save plot and clean memory:
    plt.savefig(pout + f'_boxplot_{name}.png', format='png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()
