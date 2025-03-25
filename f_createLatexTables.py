from pool_functions import *
from consts import *
import os
from consts import _HistogramNewResults,MEANS_AND_VARS,tmpAverageRanks



def createLongTableSpringer(df_means, df_vars, df_win_lost, sig_df, approch,metric,Sampling_type,
                            directoryTosave):

    # sample rows of the table should look like this:
    ####################################################################################################################
    #puma32H     & 0.032 $\pm$ 0.000             & \textbf{0.028 $\pm$ 0.000}            & 0.050 $\pm$ 0.000         & $\triangleright$ 0.040 $\pm$ 0.000 & \bftab 0.031 $\pm$ 0.000 & $\triangleleft$ 0.046 $\pm$ 0.000 & 0.070 $\pm$ 0.000 & 0.070 $\pm$ 0.000 \\
    #cpusum      & \bftab 10.73 $\pm$ 0.443      & $\triangleleft$ 16.29 $\pm$ 5.629     & \bftab 8.693 $\pm$ 0.830  &
    # $\triangleleft$ 25.25 $\pm$ 75.01 & \bftab 11.02 $\pm$ 0.744 & $\triangleleft$ 55.90 $\pm$ 43.12 & 22.83 $\pm$ 1.568 & $\triangleright$ \bftab 14.49 $\pm$ 0.495 \\
    ####################################################################################################################

    rankRow = findRank(df_means)
    rankRowStr = " & ".join(map(str, rankRow))

    # To prevent the original dataframes from being modified, we create a copy of them
    df_win_lost = df_win_lost.copy()
    df_means = df_means.copy().applymap(formatValues)
    df_vars = df_vars.copy().applymap(formatValues)
    sig_df = sig_df.copy()

    # prepare the WIN/LOST dataframes for concatenation
    df_winLost_phi_Under_odd_columns = df_win_lost.copy().iloc[:, 1::2]

    # make the column names the same as the concatenated dataframe to make the concatenation possible
    df_win_lost.columns = df_means.columns
    df_winLost_phi_Under_odd_columns.columns = sig_df.columns

    # Since the column names are the same, we can concatenate the dataframes
    df_concatenated = df_means.astype(str) + plusMinusLatex + df_vars.astype(str)

    # Bold the values in the concatenated dataframe based on the WIN/LOST dataframe
    df_concatenated = df_concatenated.where(df_win_lost == 0 , '\\textbf{' + df_concatenated + '}')


    triangle_df = sig_df.astype(str) + df_winLost_phi_Under_odd_columns.astype(str)
    triangle_df = triangle_df.applymap(extractTriLatex)



    # add triangle_df values to the beginning of odd column values of df_concatenated
    for i in range(1, len(df_concatenated.columns), 2):
        df_concatenated.iloc[:, i] = triangle_df.iloc[:, int(i/2)] + df_concatenated.iloc[:, i]

    latexTableRows = df_concatenated.apply(lambda row: " & ".join([str(row.name)] + list(row)) + " \\\\ ", axis=1)

    latexTableRows = latexTableRows.tolist()




    with open('springerTable_compare_Baseline.tmp', 'r') as file:
        latexTableTmp = file.read()

    metric_clean=metric.replace("{\phi}","phi")
    method_name=f"{approch.title()}{'US' if Sampling_type == UNDER else 'OS'}"
    latexTable = latexTableTmp.replace("__TABLE_ROWS__", "\n".join(latexTableRows)).\
                                replace("__METRIC__", metric).\
                                replace("__METHOD__", method_name).\
                                replace("__LABEL__",f"{method_name}_{metric_clean}" ).\
                                replace("__RANK_ROW__",rankRowStr)

    # create the Latex_tables_folder directory
    if not os.path.exists(directoryTosave):
        os.makedirs(directoryTosave)
        print(f"Directory '{directoryTosave}' created.")

    file_path = f"{directoryTosave}/{approch}_{metric}_{Sampling_type}.tex".replace("{\\phi}","phi")
    with open(file_path, 'w') as file:
        file.write(latexTable)
    print("Latex table is saved successfully in {}!".format(file_path))

def createTable(df_means, df_vars, df_win_lost, sig_df, file_name,directoryTosave=None):

    # To prevent the original dataframes from being modified, we create a copy of them
    df_win_lost = df_win_lost.copy()
    df_means = df_means.copy()
    df_vars = df_vars.copy()
    sig_df = sig_df.copy()

    # prepare the WIN/LOST dataframes for concatenation
    df_winLost_phi_Under_odd_columns = df_win_lost.copy().iloc[:, 1::2]
    df_win_lost.replace(1, boldLatex, inplace=True)
    df_win_lost.replace(0, "", inplace=True)

    # make the column names the same as the concatenated dataframe to make the concatenation possible
    df_win_lost.columns = df_means.columns

    # Since the column names are the same, we can concatenate the dataframes
    df_concatenated = df_means.astype(str) + plusMinusLatex + df_vars.astype(str)

    # concatenate the WIN/LOST dataframe with the concatenated dataframe
    df_concatenated = df_win_lost.astype(str) + df_concatenated.astype(str)

    df_winLost_phi_Under_odd_columns.columns = sig_df.columns
    triangle_df = sig_df.astype(str) + df_winLost_phi_Under_odd_columns.astype(str)
    triangle_df = triangle_df.applymap(extractTriLatex)

    result = pd.concat([df_concatenated.iloc[:, 0], triangle_df.iloc[:, 0], df_concatenated.iloc[:, 1],
                        df_concatenated.iloc[:, 2], triangle_df.iloc[:, 1], df_concatenated.iloc[:, 3],
                        df_concatenated.iloc[:, 4], triangle_df.iloc[:, 2], df_concatenated.iloc[:, 5],
                        df_concatenated.iloc[:, 6], triangle_df.iloc[:, 3], df_concatenated.iloc[:, 7]], axis=1)

    latexTable = result.apply(lambda row: " & ".join([str(row.name)] + list(row)) + " \\\\ ", axis=1)

    # create the Latex_tables_folder directory
    if directoryTosave is not None:
        Latex_tables_folder = directoryTosave
    if not os.path.exists(Latex_tables_folder):
        os.makedirs(Latex_tables_folder)
        print(f"Directory '{Latex_tables_folder}' created.")

    file_path = f"{Latex_tables_folder}/{file_name}.tex"
    latexTable.to_csv(file_path, index=False, header=False)
    print("Latex table is saved successfully in {}!".format(file_path))


# extract triRightLatex and triLeftLatex based on winlost and significancy dfs
def extractTriLatex(value):
    if value == "00":
        return ""
    elif value == "01":
        return ""
    elif value == "10":
        return triLeftLatex
    elif value == "11":
        return triRightLatex


def formatValues(value):
    if value < 1:
        return '{:03.2f}'.format(value)
    elif value < 10:
        return '{:03.2f}'.format(value)
    elif value < 100:
        return '{:03.2f}'.format(value)
    elif value < 1000:
        return '{:03.1f}'.format(value)
    elif value <= 100000:
        return '{:04.0f}'.format(value)
    else:
        return '{:d}'.format(int(value / 1000))


def main():
    # load the dataframes from pickle files
    print(f"Reading means and vars from {path_MEANS_AND_VARS}")
    df_means_phi, \
        df_vars_phi, \
        df_means_normal, \
        df_vars_normal, \
        df_means_sera, \
        df_vars_sera = load_means_vars(path_MEANS_AND_VARS, DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                            DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)






    # Load the WIN/LOST pickled DataFrames
    print(f"Reading win/lost files from {path_win_loss_tables}")
    df_winLost_phi_Under = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Under_pkl))
    df_winLost_phi_Over = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Over_pkl))
    df_winLost_normal_Under = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Under_pkl))
    df_winLost_normal_Over = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Over_pkl))
    df_winLost_sera_Under = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Under_pkl))
    df_winLost_sera_Over = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Over_pkl))


    # Load the Significancy pickle files

    print(f"Reading significancy files from {path_SignificancyFiles}")
    sig_phi_df_Under = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_UNDER))
    sig_phi_df_Over = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_OVER))
    sig_normal_df_Under = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_UNDER))
    sig_normal_df_Over = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_OVER))
    sig_sera_df_Under = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_UNDER))
    sig_sera_df_Over = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_OVER))

    # change column names
    df_means_phi.columns = \
        df_means_normal.columns = \
        df_vars_normal.columns = \
        df_vars_phi.columns = \
        df_means_sera.columns = \
        df_vars_sera.columns = COLUMN_NAMES

    # Create a new dataframe Under/Over by selecting only the COLUMN_NAMES_UNDER columns
    df_means_phi_Under = df_means_phi[COLUMN_NAMES_UNDER].copy()
    df_vars_phi_Under = df_vars_phi[COLUMN_NAMES_UNDER].copy()
    df_means_phi_Over = df_means_phi[COLUMN_NAMES_OVER].copy()
    df_vars_phi_Over = df_vars_phi[COLUMN_NAMES_OVER].copy()

    df_means_normal_Under = df_means_normal[COLUMN_NAMES_UNDER].copy()
    df_vars_normal_Under = df_vars_normal[COLUMN_NAMES_UNDER].copy()
    df_means_normal_Over = df_means_normal[COLUMN_NAMES_OVER].copy()
    df_vars_normal_Over = df_vars_normal[COLUMN_NAMES_OVER].copy()

    df_means_sera_Under = df_means_sera[COLUMN_NAMES_UNDER].copy()
    df_vars_sera_Under = df_vars_sera[COLUMN_NAMES_UNDER].copy()
    df_means_sera_Over = df_means_sera[COLUMN_NAMES_OVER].copy()
    df_vars_sera_Over = df_vars_sera[COLUMN_NAMES_OVER].copy()


    # create the latex tables
    createTable(df_means_phi_Under, df_vars_phi_Under, df_winLost_phi_Under, sig_phi_df_Under,"phi_Under",path_Latex_tables_folder)
    createTable(df_means_phi_Over, df_vars_phi_Over, df_winLost_phi_Over, sig_phi_df_Over, "phi_Over",path_Latex_tables_folder)
    createTable(df_means_normal_Under, df_vars_normal_Under, df_winLost_normal_Under, sig_normal_df_Under,
                "normal_Under",path_Latex_tables_folder)
    createTable(df_means_normal_Over, df_vars_normal_Over, df_winLost_normal_Over, sig_normal_df_Over, "normal_Over",path_Latex_tables_folder)
    createTable(df_means_sera_Under, df_vars_sera_Under, df_winLost_sera_Under, sig_sera_df_Under,"sera_Under",path_Latex_tables_folder)
    createTable(df_means_sera_Over, df_vars_sera_Over, df_winLost_sera_Over, sig_sera_df_Over, "sera_Over",path_Latex_tables_folder)



    #springer tables for journal

    createLongTableSpringer(df_means_phi_Under, df_vars_phi_Under, df_winLost_phi_Under, sig_phi_df_Under,
                            approach_name,RMSEPHI,UNDER,path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_phi_Over, df_vars_phi_Over, df_winLost_phi_Over, sig_phi_df_Over,
                            approach_name,RMSEPHI,OVER,path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_normal_Under, df_vars_normal_Under, df_winLost_normal_Under, sig_normal_df_Under,
                            approach_name,RMSE,UNDER,path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_normal_Over, df_vars_normal_Over, df_winLost_normal_Over, sig_normal_df_Over,
                            approach_name,RMSE,OVER,path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_sera_Under, df_vars_sera_Under, df_winLost_sera_Under, sig_sera_df_Under,
                            approach_name,SERA,UNDER,path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_sera_Over, df_vars_sera_Over, df_winLost_sera_Over, sig_sera_df_Over,
                            approach_name,SERA,OVER,path_Latex_tables_folder_springer)




    rankLsts=[findRank(df_means_phi_Under),
              findRank(df_means_phi_Over),
              findRank(df_means_normal_Under),
              findRank(df_means_normal_Over),
              findRank(df_means_sera_Under),
              findRank(df_means_sera_Over)]

    for rankLst,methodName in zip(rankLsts,["phi_US","phi_OS","normal_US","normal_OS",
                                                                   "sera_US","sera_OS"]):
        print(rankLst)
        print(f"{20*'-'}{methodName}{20*'-'}")
        print(tmpAverageRanks.replace("__0__",str(rankLst[0])).replace("__1__",str(rankLst[1])).replace("__2__",
        str(rankLst[2])).replace("__3__",str(rankLst[3])).replace("__4__",str(rankLst[4])).replace("__5__",
        str(rankLst[5])).replace("__6__",str(rankLst[6])).replace("__7__",str(rankLst[7])))
        print(50*"-")
if __name__ == "__main__":
    main()
