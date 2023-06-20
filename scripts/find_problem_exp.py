# -*- coding: utf-8 -*-
"""
Description: Create table with missing experiments

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49 170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    06.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    07.06.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     ==============
import numpy as np
import pandas as pd
# =============================   Personal functions   ==============
# -- find_problem_exp --> Find "potential" missing numbers for the research experiment
def find_problem_exp(
        # Input variables:
        pin:str,                      # Input path with post-processing data. Result of tic-toc script
        exp:str,                      # Research experiment
        pout:str,                     # Output path
        split_by:str,                 # Parameter for spliting
        # Output variables:
    ):                                # Create a new file in .xlsx format in output folder
    # -- Local parameters for function:
    int4col  = 'int32'       # type of values 
    ser_name = 'miss_value'  # name of column
    step     = 1             # step in range of  min -- max values
    # -- Read experiment data after post-processing:
    df = pd.read_excel(pin)
    # -- Create column with experiment name:
    df['exp' ] = (
        df['probenname'].str.split(split_by, expand = True)
                        .loc[:,[0]]
                        .rename(columns = {0 : 'exp'})
    ) 
    # -- Create column with experiment number:
    df['num'] = (
        df['probenname'].str.split(split_by, expand = True)
                        .loc[:,[1]]
                        .rename(columns = {1 : 'verd'})
    )
    df['num'] = df['num'].astype(int4col)
    # -- Define the full list of possible numbers:
    min_num = np.min(df['num'])
    max_num = np.max(df['num'])
    refer_values = np.arange(min_num, max_num, step)
    # -- Compare experiment number with reference number:
    pot_prob = []
    for i in refer_values:
        if i not in df['num'].tolist():
            pot_prob.append(f'{exp} {i}')
    problem_numbers = pd.Series(pot_prob).rename(ser_name)
    # -- Save output files
    problem_numbers.to_excel(pout, sheet_name = f'{exp}_data')
    return df

# ================   User settings (have to be adapted)  ==============
# -- Select data (experiment name):
exp = 'mh'
#exp = 'ma'
#exp = 'mh-r'

# -- Select symbol for spliting data (don't change parameters set4exp and split_by)
set4exp = {
    'mh'  : 'h',
    'ma'  : 'a',
    'mh-r': 'r',
}
split_by = set4exp.get(exp)

# -- Output format for file:
form_table = '.xlsx'

# -- User paths (Common, intup and output):
main = 'C:/evchur/scripts/project_tic_toc/DATA/OUTPUT' # Path was changed
pin  = main + f'/data4_{exp}{form_table}'
pout = main + f'/no_data4{exp}{form_table}'

# =============================    Main program   =====================
if __name__ == '__main__':
    df = find_problem_exp(pin, exp, pout, split_by)
# =============================    End of program   ===================
