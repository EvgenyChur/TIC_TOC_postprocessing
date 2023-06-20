# -*- coding: utf-8 -*-
"""
Description: Script allow you to rename data in input folder:

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
# =============================     Import modules     =================
# -- Standard:
import os
import pandas as pd
# =============================   Personal functions   ===================

# ================   User settings (have to be adapted)  =================
main = 'C:/Users/evchur/Desktop/Ergebnisse/MH-r/Test/'
# -- Input and Output paths:
pin = main
pout = main
# -- New common name for input data:
name = 'highTOC_Gerighausen_'
# -- Data format:
exc_format = '.xls'
# =============================    Main program   =========================
if __name__ == '__main__':
    # -- Get the list of input data in main folder (we are interesting only in '.xls' files )
    lst4names = []
    for path in os.listdir(main):
        if path.endswith(exc_format):
            lst4names.append(path)
    # -- Get absolute data paths:
    lst4paths  = []
    for file in lst4names:
        lst4paths.append(os.path.join(main, file))
    # -- Get the list out new files based on input data:
    lst4out = []
    for file in lst4paths:
        df = pd.read_excel(file)
        num =  df['Unnamed: 1'][0]
        new_name = f'{name}EL{num}{exc_format}'
        lst4out.append(os.path.join(main, new_name))
    # -- Rename and save files:
    for i in range(len(lst4out)):
        print(f'File \n {lst4paths[i]} was rename to \n {lst4out[i]}')
        print(' ')
        os.rename(lst4paths[i], lst4out[i])
# =============================    End of program   ======================
