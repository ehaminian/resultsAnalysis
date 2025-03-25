from os import replace


from consts import *
from pool_functions import *
import os

# load file from the C:\Users\Ehsan\Desktop\git\eea1\Results\results_18_HIST_FIMT_DD.csv into a dataframe
import pandas as pd

import re

import re


KOTLINE_RESULTS_DIR=r"C:\Users\Ehsan\Desktop\git\eea1\Results"
# HIST_FILE_NAME='results_18_HIST_FIMT_DD.csv'
# CHEBY_FILE_NAME='results_18_CHEBY_FIMT_DD.csv'
HIST_FILE_NAME='results_6_FIMT_DD_hist.csv'
CHEBY_FILE_NAME='results_6_FIMT_DD_cheby.csv'


SAVE_TABLE_NAME= 'rankTable_6_range' #SAVE_TABLE_NAME


HIST_INTERESTED_METRIC_MODELS_COLUMNS_NAME=[ 'histRmsePhiUnder', 'histRmsePhiOver', 'histRmseUnder', 'histRmseOver',
                                      'histSeraUnder', 'histSeraOver']
CHEBY_INTERESTED_METRIC_MODELS_COLUMNS_NAME=[ 'chebyRmsePhiUnder', 'chebyRmsePhiOver', 'chebyRmseUnder', 'chebyRmseOver',
                                      'chebySeraUnder', 'chebySeraOver']
RMSE_PHI_COLUMNS=['baseRmsePhi', 'histRmsePhiUnder', 'histRmsePhiOver', 'chebyRmsePhiUnder', 'chebyRmsePhiOver']
SERA_COLUMNS=['baseSera', 'histSeraUnder', 'histSeraOver', 'chebySeraUnder', 'chebySeraOver']
RMSE_COLUMNS=['baseRmse', 'histRmseUnder', 'histRmseOver', 'chebyRmseUnder', 'chebyRmseOver']
LATEX_COLUMNS = ['Baseline', 'HistUS', 'HistOS', 'ChebyUS', 'ChebyOS']
df_hist_raw = pd.read_csv(os.path.join(KOTLINE_RESULTS_DIR, HIST_FILE_NAME))
df_cheby_raw = pd.read_csv(os.path.join(KOTLINE_RESULTS_DIR, CHEBY_FILE_NAME))




df_hist = df_hist_raw[HIST_INTERESTED_METRIC_MODELS_COLUMNS_NAME]
df_cheby = df_cheby_raw[CHEBY_INTERESTED_METRIC_MODELS_COLUMNS_NAME]


# extract baseRmsePhi and baseSera columns from both dataframes
df_hist_base = df_hist_raw[['baseRmsePhi','baseRmse', 'baseSera']]
df_cheby_base = df_cheby_raw[['baseRmsePhi','baseRmse', 'baseSera']]
df_base = (df_hist_base + df_cheby_base ) / 2
df_base.columns = ['baseRmsePhi','baseRmse' ,'baseSera']

df_Total = pd.concat([df_base, df_hist, df_cheby], axis=1)

df_rmsePhi = df_Total[RMSE_PHI_COLUMNS]
df_sera = df_Total[SERA_COLUMNS]
df_normal = df_Total[RMSE_COLUMNS]

df_rmsePhi_mean = pd.Series(df_rmsePhi.mean(), name="mean").to_frame().T
df_rmsePhi_vars = pd.Series(df_rmsePhi.var(), name="var").to_frame().T
df_normal_mean = pd.Series(df_normal.mean(), name="mean").to_frame().T
df_normal_vars = pd.Series(df_normal.var(), name="var").to_frame().T
df_sera_mean = pd.Series(df_sera.mean(), name="mean").to_frame().T
df_sera_vars = pd.Series(df_sera.var(), name="var").to_frame().T


df_rmsePhi_mean.reset_index(drop=True, inplace=True)
df_rmsePhi_vars.reset_index(drop=True, inplace=True)
df_normal_mean.reset_index(drop=True, inplace=True)
df_normal_vars.reset_index(drop=True, inplace=True)
df_sera_mean.reset_index(drop=True, inplace=True)
df_sera_vars.reset_index(drop=True, inplace=True)




df_rmsePhi_mean_vars = df_rmsePhi_mean.round(2).astype(str) + plusMinusLatex + df_rmsePhi_vars.round(2).astype(str)
df_normal_mean_vars = df_normal_mean.round(2).astype(str) + plusMinusLatex + df_normal_vars.round(2).astype(str)
df_sera_mean_vars = df_sera_mean.round(2).astype(str) + plusMinusLatex + df_sera_vars.round(2).astype(str)


df_rmsePhi_mean_vars.columns = df_sera_mean_vars.columns = df_normal_mean_vars.columns = LATEX_COLUMNS




# append the df_hist_mean_vars and df_cheby_mean_vars
df_hist_cheby_mean_vars = df_rmsePhi_mean_vars.append(df_normal_mean_vars.append(df_sera_mean_vars))
df_hist_cheby_mean_vars.index = [RMSEPHI,RMSE, SERA]


# print row with index RMSE_{\phi} in df_hist_cheby_mean_vars
print(df_hist_cheby_mean_vars.loc[RMSEPHI].tolist())
print(df_hist_cheby_mean_vars.loc[RMSE].tolist())
print(df_hist_cheby_mean_vars.loc[SERA].tolist())



rmse_phi_mean_vars_latex = " & ".join(map(str, df_hist_cheby_mean_vars.loc[RMSEPHI].tolist()))
rmse_mean_vars_latext = " & ".join(map(str, df_hist_cheby_mean_vars.loc[RMSE].tolist()))
sera_mean_vars_latex = " & ".join(map(str, df_hist_cheby_mean_vars.loc[SERA].tolist()))

rmsePhi_rank_latex_table = " & ".join(map(str, findRank(df_rmsePhi)))
rmse_rank_latex_table = " & ".join(map(str, findRank(df_normal)))
sera_rank_latex_table = " & ".join(map(str, findRank(df_sera)))

print_df(df_hist_cheby_mean_vars)

with open('syntheticDataset.tmp', 'r') as file:
    latexTable = file.read()



latexTable = latexTable.replace('__RMSE_PHI_MEAN__', rmse_phi_mean_vars_latex).\
                        replace("__RMSE_PHI_RANK__",rmsePhi_rank_latex_table).\
                        replace("__RMSE_MEAN__",rmse_mean_vars_latext).\
                        replace("__RMSE_RANK__",rmse_rank_latex_table).\
                        replace("__SERA_MEAN__",sera_mean_vars_latex).\
                        replace("__SERA_RANK__",sera_rank_latex_table)

targetPath = f"{Synthetic_results}/{RANKE_TABLE}"
createRequiredDirectories(targetPath)
with open(f"{targetPath}/{SAVE_TABLE_NAME}.tex",
          'w') as file:
    file.write(latexTable)
