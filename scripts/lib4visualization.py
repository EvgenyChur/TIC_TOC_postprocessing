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
    1.3    09.08.2023 Evgenii Churiulin, MPI-BGC
           Add new class for visualization
"""
# =============================     Import modules     =====================
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings("ignore")
from scipy import stats
# 1.2 Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4processing as l4p
days = mdates.DayLocator(5)

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


class Complex_PLT:
    def __init__(self, title, leg_loc):
        # Set common parameters for all figures:
        self.title = title    # Common plot title
        self.clr   = 'black'  # Color of labels
        self.fsize = 14       # Size of labels
        self.pad   = 20       # Space betveen axis and label
        self.l_pos = leg_loc  # Legend location
        self.gtype = 'major'  # Which axis do you want to use for grid (major or)
        self.gclr  = 'grey'   # Grid color
        self.gstyle= 'dashed' # Grid line style
        self.galpha= 0.2      # Grid transparacy
        self.txaxis_format = '%d-%m'

    def plt_uniq_settings(self, ax, uset):
        """ User settings for plot"""
        # -- Set plot title:
        if 'ltitle' in uset and uset.get('ltitle'):
            ax.set_title(
                self.title,
                color = self.clr,
                fontsize = self.fsize,
                pad = self.pad,
            )
        # -- Set x axis label:
        if 'xlabel' in uset:
            ax.set_xlabel(
                uset.get('xlabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set y axis label:
        if 'ylabel' in uset:
            ax.set_ylabel(
                uset.get('ylabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set X axis ticks parameters for time axis:
        if 'xlim_time' in uset and len(uset.get('xlim_time')) > 0:
            ax.set_xlim(
                pd.to_datetime(uset.get('xlim_time')[0], format='%d.%m.%Y'),
                pd.to_datetime(uset.get('xlim_time')[1], format='%d.%m.%Y'),
            )
            xftm = mdates.DateFormatter(self.txaxis_format)
            ax.xaxis.set_major_formatter(xftm)
            ax.xaxis.set_minor_locator(days)
        # -- Set X axis ticks paramters for numbers:
        if 'xlim_num' in uset and len(uset.get('xlim_num')) > 0:
            ax.set_xticks(
                np.arange(
                    uset.get('xlim_num')[0],
                    uset.get('xlim_num')[1],
                    uset.get('xlim_num')[2],
                )
            )
        # -- Set Y axis ticks parameters:
        if 'ylim_num' in uset and len(uset.get('ylim_num')) > 0:
            ax.set_yticks(
                np.arange(
                    uset.get('ylim_num')[0],
                    uset.get('ylim_num')[1],
                    uset.get('ylim_num')[2],
                )
            )
        # -- Change original y axis values to labels:
        if 'ltick_labels' in uset and uset.get('ltick_labels'):
            ax.set_yticklabels(
                abs(
                    np.arange(
                        uset.get('ylim_num')[0],
                        uset.get('ylim_num')[1],
                        uset.get('ylim_num')[2],
                    )
                )
            )
        # -- Add legend:
        if 'llegend' in uset and uset.get('llegend'):
            ax.legend(loc = self.l_pos)
        # -- Add grid settings:
        if 'lgrid' in uset and uset.get('lgrid'):
            ax.grid(
                uset.get('lgrid'),
                which = self.gtype,
                color = self.gclr,
                linestyle = self.gstyle,
                alpha = self.galpha,
            )


    def t2m_plot(self, ax, df):
        """T2m linear plot"""
        ax.plot(df.index, df, label = 'T2m', color = 'red')
        return ax


    def precip_plot(self, ax, df):
        """Precipitation bar plot"""
        ax.bar(df.index, df['rain (mm)'], label = 'Prec', color = 'green')
        return ax


    def sm_plot(self, ax, df):
        """Soil moisture linear plot"""
        # -- Get actual columns:
        cols = df.columns.tolist()
        # -- Defeni actual colors for line
        n = len(cols) + 1
        colors = plt.cm.jet(np.linspace(0, 1, n))
        # -- Add lines to the plot:
        for i,col in enumerate(cols):
            ax.plot(df[col], df.index, label = col, color=colors[i])
        return ax


def complex_plot(df, df_sets, t2m_sets, prec_sets, sm_sets):
    # -- Local variables:
    fig_length = 14
    fig_higth = 10
    cols = 3
    rows = 4
    # -- Get data for visualization:
    df_temp, df_prec, df_soil = l4p.get_complex_plot_data(df, df_sets)

    # -- Create figure and set figure parameters:
    fig = plt.figure(figsize = (fig_length, fig_higth))
    # -- Set boundaries:
    # Левая граница subplots на рисунке
    rcParams['figure.subplot.left'] = 0.1
    # Правая граница subplots на рисунке
    rcParams['figure.subplot.right'] = 0.95
    # Нижняя граница subplots на рисунке
    rcParams['figure.subplot.bottom'] = 0.05
    # Верхняя граница subplots на рисунке
    rcParams['figure.subplot.top'] = 0.95
    # -- Set numbers of subplot:
    egrid = (rows,cols)
    ax1 = plt.subplot2grid(egrid, (0, 0), colspan = 3)
    ax2 = plt.subplot2grid(egrid, (1, 0), colspan = 3)
    ax3 = plt.subplot2grid(egrid, (2, 0), colspan = 3, rowspan = 2)
    # -- Create complex plot:
    plot = Complex_PLT('WS Saaleaue', 'upper right')
    # -- Add first plot:
    plot.t2m_plot(ax1, df_temp)
    plot.plt_uniq_settings(ax1, t2m_sets)
    # -- Add second plot:
    plot.precip_plot(ax2, df_prec)
    plot.plt_uniq_settings(ax2, prec_sets)
    # -- Add trird plot:
    plot.sm_plot(ax3, df_soil)
    plot.plt_uniq_settings(ax3, sm_sets)
    # -- Save plot:
    plt.savefig(df_sets.get('fout'), format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()