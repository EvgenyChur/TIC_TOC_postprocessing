# How to use scripts:

1. Scripts  `tic_tot.py` and `alina_task2.py`. These scripts were developed for preprocessing on TIC and TOC data for searching ***bad measurements: no data, errors, no information about measurement stations and ets)*** and processing data for Akanksha research tasks. The script `alina_task2.py` uses information from field `kommentar` as source of input metainformation about stations and because of that works correctly only for `MH` stations. For `MA` and `MH-r` stations there isn't correct searching mask and script can work with errors. To solve this problem input data has to have simular to `MH` stations description (simular for all measurements) or the searching mask should be modernized (needs to be discussed with responsible data specialists).
Scripts have 5 main parts:
    - *Import modules* - all import modules and packages are presented here. You don't need to change it;;
    - *User settings (have to be adapted)* - user settings, you have to change them. More information you can find in script comments;
    - *User settings (can be the same)* - user settings, you can use standard options without changes. Nevertheless, if you want to change them, you can do it, but I don't recommend to that at the beginning. More information you can find in script comments;
    - *Main program* - main algorithm for data processing. You don't need to change it.

These script are sensitive to input data, because of that there are several steps for working with these script:
* ***Step 1 - Introduction with script***
At the beginning, it is really important to understand how this script works regardless from input data problems. Because of that there is a debugging option for that. You can activate this option if you select these logical parameters in *User settings (have to be adapted)*:
```
lmake_folder  = True   # Do you want to automatically create output folder?
lclean_folder = False  # Do you want to clean the previous results in output folder?
lauto_read    = False  # Do you want to read all data from your datafolder?
ldata_quality = True   # Do you want to compare headers in your excel files?
linfo         = True   # Do you want to get more information about your data
```

In addition, you have to add your reliable  data (input files corresponding to all input data requirements) into variable `lst4names` in section `Manual option` (code lines 133 - 136). I recommend to use no more then 5 input files, the best solution (3 files).

* ***Step 2 - Running script based on all excel files from input folder:***
As I mentioned early, this script is really sensitive to input data, but we have a lot of input data and it can really difficult to check all of them manually. Because of that this script has a simplified system for input data control (quality control) and you can activate it with the next logical parameters in *User settings (have to be adapted)*:
```
lmake_folder  = True   # Do you want to automatically create output folder?
lclean_folder = False  # Do you want to clean the previous results in output folder?
lauto_read    = True   # Do you want to read all data from your datafolder?
ldata_quality = True   # Do you want to compare headers in your excel files?
linfo         = False  # Do you want to get more information about your data
```

If your input files correspondent to all input data requirements you can get this message into command window:
> Header in file_1 and file_2 is the same

The comparison is performed sequentially (file by file). If you have problems with input data you will get another message and program will be automatically stopped:
> Header in file_2 is different'

More information how solve this problems you can find in section ***Input data requirements*** and ***Problems with software***.

* ***Step 3 - Main run:***
Now, you are sure that your input files successfully passed `quality control` step and you can finally can start data processing. You can change the logical parameters in ***User settings (have to be adapted)*** and save computation time:
```
lmake_folder  = True   # Do you want to automatically create output folder?
lclean_folder = False  # Do you want to clean the previous results in output folder?
lauto_read    = True   # Do you want to read all data from your datafolder?
ldata_quality = False  # Do you want to compare headers in your excel files?
linfo         = False  # Do you want to get more information about your data
```

At this step, you can also get sevaral problems (problems 3, 4 and 5 from section ***Problems with software***) which are related to input data. These problems can be easily solved by small changes into input files. If you didn't get other error message  you can check data in your output folders and then you can run the next script `find_problem_exp.py`.

| Experiment | Line plot |  Boxplot (before filter) | Boxplot (after filter) | Correlation map (before filter) | Correlation map (after filter) |
|:----------:|:---------:|:------------------------:|:----------------------:|:-------------------------------:|:------------------------------:|
| MH         | ![][fig1a]| ![][fig1b]               | ![][fig1c]             | ![][fig1d]                      | ![][fig1f]                     |
| MA         | ![][fig2a]| ![][fig2b]               | ![][fig2c]             | ![][fig2d]                      | ![][fig2f]                     |
| MH-R       | ![][fig3a]| ![][fig3b]               | ![][fig3c]             | ![][fig3d]                      | ![][fig3f]                     |


[fig1a]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh/fig4mh_in_range_273_364.png
[fig1b]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh/fig4mh_boxplot_toc.png
[fig1c]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh/fig4mh_boxplot_toc2.png
[fig1d]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh/fig4mh_correlation_1.png
[fig1f]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh/fig4mh_correlation_2.png

[fig2a]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_ma/fig4ma_in_range_0_57.png
[fig2b]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_ma/fig4ma_boxplot_toc.png
[fig2c]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_ma/fig4ma_boxplot_toc2.png
[fig2d]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_ma/fig4ma_correlation_1.png
[fig2f]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_ma/fig4ma_correlation_2.png

[fig3a]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh-r/fig4mh-r_in_range_24_48.png
[fig3b]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh-r/fig4mh-r_boxplot_toc.png
[fig3c]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh-r/fig4mh-r_boxplot_toc2.png
[fig3d]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh-r/fig4mh-r_correlation_1.png
[fig3f]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/DATA/FIGURES_mh-r/fig4mh-r_correlation_2.png

**Figure 1.** Examples of output results calculated based `tic_toc.py` script

3. `find_problem_exp.py` - you can get a special output tables with missing measurements. If you want to do that, you have to have results of the `tic_toc.py` script and check actual values in section **User settings**, after that save changes and run script;

If you want to do that, you have to have results of the `tic_toc.py` script and check actual values in section **User settings**, after that save changes and run script;

4. `rename` - you can rename your input files based on metainformation from excel files. If you want to do that, you have to open this script, check values in section ***User settings (have to be adapted)*** and run you script. It makes sense, if your data has different names which are not follow  required to ***Input data requirements*** and have correct meta information in file.


## How to run script:
1. Local computer --> open anaconda and run script;
2. MPI-BGC cluster --> use this command;
```
python3 ./script.py
# or
python3 ./Net/Groups/BGI/people/user/.../script.py
```
where: `script` is your running script

## Input data requirements:
1. All input data for `tic_toc.py` and `alina_task2` script have to have:
    - Filenames with the next structure ***highTOC_{station}_EL{index}.xls***. Where `station` is the name of the research station (*Gerighausen*) and `index` is uniq name for moment of measurements (*EL5654*);
    - Data which is located in `Sheet1`;
    - Similar German header (**not English**), which is located in line 12 of excel file;
    - Metainformation about measurements, which is located in lines 1 - 10, columns A - B - C;
    - No gaps, between data;
    - In field `Kommentar` you should have additional meteinformation. For ***MH*** experiments it has to be something like that `B1A01/20` or `B1A01/20; Verdünung 1:5 eingerechnet`. It is really important for script `alina_task2.py` due to, this script uses this column as a source of information about measurements point.
    - In field `Ergebnis` you should have values, not text (`Probe alle`). If you have text value in this column, this line will be automatically ignore;

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/data_requirements.jpg"></p>

**Figure 2.** Example of correct input data for TIC TOC data processing

***P.S.:*** You can control parameters of excel files (header, sheet) based on variable `set4excel` in `tic_toc.py` script, but all your data have to have the same structure. Otherwise, you have to write exception and it can make the code much more complex, but not effective.

***P.S.2:*** You should have in input data folder onle .xls file and folders. No other files

### Problems with software:
1. ***Missing optional dependency*** or ***No module:***:

|    A         |     B |
|:------------:|:------------:|
| ![][fig5a]   | ![][fig5b]   |

[fig5a]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_xlrd.jpg
[fig5b]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_no_module.jpg

**Figure 3.** Example of problem with: A - missing optional dependency, B - module

***How you can solve it:*** You have to use these command on MPI-BGC cluster
```
module load proxy
conda install -c anaconda xlrd
conda install -c anaconda openpyxl
```
or
```
conda install -c anaconda xlrd
conda install -c anaconda openpyxl
```
if you working on you local computer

2. ***Header problem:***

|    A         |     B        |
|:------------:|:------------:|
| ![][fig6a]   | ![][fig6b]   |

[fig6a]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_header.jpg
[fig6b]: https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_probenjahr.jpg

**Figure 4.** Problem with input data header: A - during quality control test, B - main mode

***How you can solve it:*** You have to open your excel file (`file.xls`) and manually change the file header to German. The best option, you have to paste the copied header from another file, then save changes in excel file and run script again. If you get this problem at the beginning, the error can be not in printed file, but in a previous one (first).

3. ***Space between lines:***

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_NA.jpg"></p>

**Figure 5.** Example of error when we have space between lines

***How you can solve it:*** You have to open the last opened file before error and delete a gap between lines, then save changes in excel file and run script again.

4. ***No data for replace:***

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_replace.jpg"></p>

**Figure 6.** Example of error when we have no data for replace

***How you can solve it:*** You have to open the last opened file before error and check values in `Kommentar` column. If you don't have data you have to add them or delete this file.

5. ***Putty problem:***

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_putty.jpg"></p>

**Figure 7.** Example of the problem with openning output figure

You can ignore this problem or install and run `Xming`. Actual for Windows users.

6. ***File not found:***

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/RESULTS/error_no_data.jpg"></p>

**Figure 8.** File not found

***How you can solve it:*** You have to change input path in your running script
