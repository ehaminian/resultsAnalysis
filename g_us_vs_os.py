from astroid import Print

from consts import *
from pool_functions import *
import os
from f_createLatexTables import extractTriLatex



tmpAverageRanks = """
\multicolumn{1}{|c|}{ __0__ }  &
\multicolumn{2}{|c|}{ __1__ }  &
\multicolumn{1}{|c|}{ __2__ }  &
\multicolumn{2}{|c|}{ __3__ }  &
\multicolumn{1}{|c|}{ __4__ }  &
\multicolumn{2}{|c|}{ __5__ }  &
\multicolumn{1}{|c|}{ __6__ }  &
\multicolumn{2}{|c|}{ __7__ }  \\\\
"""

from consts import path_MEANS_AND_VARS, path_win_loss_tables, path_SignificancyFiles, path_Win_loss_BARS,\
                    path_Latex_tables_folder, path_RANK_TABLE, path_CD_disagrams
# path_MEANS_AND_VARS = f"{_HistogramNewResults}{MEANS_AND_VARS[1:]}"
# path_win_loss_tables = f"{_HistogramNewResults}{Win_loss_tables[1:]}"
# path_SignificancyFiles = f"{_HistogramNewResults}{SignificancyFiles[1:]}"
# path_Win_loss_BARS = f"{_HistogramNewResults}{Win_loss_BARS[1:]}"
# path_Latex_tables_folder = f"{_HistogramNewResults}{Latex_tables_folder[1:]}"
# path_RANK_TABLE = f"{_HistogramNewResults}{RANKE_TABLE[1:]}"
# path_CD_disagrams = f"{_HistogramNewResults}{CD_disagrams[1:]}"

def makeDFsRound(dfLst):
    lst = []
    for df in dfLst:
        df = df.round(2)
        df = df.applymap(lambda x: f'{x:.0e}' if x >= 1000 else f'{x:.2f}')
        lst.append(df)
    return lst

def getCleandf(df1,df2,df3,df4,df5,df6):
    lst_df = makeDFsRound([df1,df2,df3,df4,df5,df6])
    return lst_df[0],lst_df[1],lst_df[2],lst_df[3],lst_df[4],lst_df[5]

def getCleandf_New(df1,df2):
    lst_df = makeDFsRound([df1,df2])
    return lst_df[0],lst_df[1]

def createLongTableSpringer(df_means, df_vars, df_win_lost, sig_df, approch,metric,directoryTosave):

    # sample rows of the table should look like this:
    ####################################################################################################################
    #puma32H     & 0.032 $\pm$ 0.000             & \textbf{0.028 $\pm$ 0.000}            & 0.050 $\pm$ 0.000         & $\triangleright$ 0.040 $\pm$ 0.000 & \bftab 0.031 $\pm$ 0.000 & $\triangleleft$ 0.046 $\pm$ 0.000 & 0.070 $\pm$ 0.000 & 0.070 $\pm$ 0.000 \\
    #cpusum      & \bftab 10.73 $\pm$ 0.443      & $\triangleleft$ 16.29 $\pm$ 5.629     & \bftab 8.693 $\pm$ 0.830  &
    # $\triangleleft$ 25.25 $\pm$ 75.01 & \bftab 11.02 $\pm$ 0.744 & $\triangleleft$ 55.90 $\pm$ 43.12 & 22.83 $\pm$ 1.568 & $\triangleright$ \bftab 14.49 $\pm$ 0.495 \\
    ####################################################################################################################

    # To prevent the original dataframes from being modified, we create a copy of them
    df_win_lost = df_win_lost.copy()
    df_means = df_means.copy()
    df_vars = df_vars.copy()
    sig_df = sig_df.copy()

    rankRow = findRank(df_means)
    rankRowStr = " & ".join(map(str, rankRow))
    df_means,df_vars = getCleandf_New(df_means,df_vars)



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

    if df_concatenated.isna().any().any():
        print("There is a NaN value in the concatenated dataframe!")
        print("df_concatenated:")
        print_df(df_concatenated)
        exit(10)


    try:
        latexTableRows = df_concatenated.apply(lambda row: " & ".join([str(row.name)] + list(row)) + " \\\\ ", axis=1)
    except Exception as e:
        print(e)
        print("df_concatenated")
        print_df(df_concatenated)
        exit(150)

    latexTableRows = latexTableRows.tolist()

    with open('springerTable_compare_hist_US_OS.tmp', 'r') as file:
        latexTableTmp = file.read()

    metric_clean=metric.replace("{\phi}","phi")
    latexTable = latexTableTmp.replace("__TABLE_ROWS__", "\n".join(latexTableRows)).\
                                replace("__METRIC__", metric).\
                                replace("__LABEL__",f"{metric_clean}" ).\
                                replace("__RANK_ROW__",rankRowStr)

    # create the Latex_tables_folder directory
    if not os.path.exists(directoryTosave):
        os.makedirs(directoryTosave)
        print(f"Directory '{directoryTosave}' created.")

    file_path = f"{directoryTosave}/{approch.title()}_US_OS_{metric_clean}.tex"
    with open(file_path, 'w') as file:
        file.write(latexTable)
    print("Latex table is saved successfully in {}!".format(file_path))


def createTable(df_means, df_vars, df_winLost, sig_df, file_name, path):

    df_means = df_means.copy()
    df_vars = df_vars.copy()
    df_winLost = df_winLost.copy()
    sig_df = sig_df.copy()

    df_winLost_phi_Under_odd_columns = df_winLost.copy().iloc[:, 1::2]
    df_winLost.columns = df_means.columns
    df_winLost.replace(1, boldLatex, inplace=True)
    df_winLost.replace(0, "", inplace=True)

    # Since the column names are the same, we can concatenate the dataframes
    df_concatenated = df_means.astype(str) + plusMinusLatex + df_vars.astype(str)
    df_concatenated = df_winLost.astype(str) + df_concatenated.astype(str)
    df_winLost_phi_Under_odd_columns.columns = sig_df.columns
    triangle_df = sig_df.astype(str) + df_winLost_phi_Under_odd_columns.astype(str)
    triangle_df = triangle_df.applymap(extractTriLatex)
    result = pd.concat([df_concatenated.iloc[:, 0], triangle_df.iloc[:, 0], df_concatenated.iloc[:, 1],
                        df_concatenated.iloc[:, 2], triangle_df.iloc[:, 1], df_concatenated.iloc[:, 3],
                        df_concatenated.iloc[:, 4], triangle_df.iloc[:, 2], df_concatenated.iloc[:, 5],
                        df_concatenated.iloc[:, 6], triangle_df.iloc[:, 3], df_concatenated.iloc[:, 7]], axis=1)
    latexTable = result.apply(lambda row: " & ".join([str(row.name)] + list(row)) + " \\\\ ", axis=1)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")

    file_path = f"{path}/{file_name}.tex"
    latexTable.to_csv(file_path, index=False, header=False)
    print("Latex table is saved successfully in {}!".format(file_path))

def loadPicklesFiles():

    # load the dataframes winLost US_OS from pickle files
    df_winLost_phi_Un_OS = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Under_vs_Over_pkl))
    df_winLost_normal_Un_OS = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Under_vs_Over_pkl))
    df_winLost_sera_Un_OS = pd.read_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Under_vs_Over_pkl))

    # load the Significancy pickle files
    sig_phi_df_Un_OS = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_UNDER_VS_OVER))
    sig_normal_df_Un_OS = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_UNDER_VS_OVER))
    sig_sera_df_Un_OS = pd.read_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_UNDER_VS_OVER))

    # load the means and vars pickle files
    df_means_phi, \
        df_vars_phi, \
        df_means_normal, \
        df_vars_normal, \
        df_means_sera, \
        df_vars_sera = load_means_vars(path_MEANS_AND_VARS, DF_MEANS_PHI_Un_OS_pkl, DF_VARS_PHI_Un_OS_pkl, DF_MEANS_NORMAL_Un_OS_pkl,
                                       DF_VARS_NORMAL_Un_OS_pkl, DF_MEANS_SERA_Un_OS_pkl, DF_VARS_SERA_Un_OS_pkl)
    return df_winLost_phi_Un_OS, df_winLost_normal_Un_OS, df_winLost_sera_Un_OS,\
        sig_phi_df_Un_OS, sig_normal_df_Un_OS, sig_sera_df_Un_OS, \
            df_means_phi, df_vars_phi, df_means_normal,df_vars_normal, df_means_sera, df_vars_sera

def main():
    # load the dataframes from pickle files
    df_means_phi, \
    df_vars_phi, \
        df_means_normal, \
        df_vars_normal, \
        df_means_sera, \
        df_vars_sera = load_means_vars(path_MEANS_AND_VARS, DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                            DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)

    # compute the significance of the means just to compare Under vs Over sampling
    #################################################################
    list_of_the_datasets = []

    # Save the results of each learner type in a dataframe
    sig_df = pd.DataFrame(columns=["phi_under_over", "normal_under_over","sera_under_over",
                                   "phi_under_over", "normal_under_over", "sera_under_over",
                                   "phi_under_over", "normal_under_over", "sera_under_over",
                                   "phi_under_over", "normal_under_over", "sera_under_over"])

    # walk through all csv files in the Results folder
    for file in os.listdir(path_to_Results_OS_US):

        df = read_csv("{}/{}".format(path_to_Results_OS_US, file))
        list_of_the_datasets.append(file)

        # divide the dataframe into four dataframes each having 10 rows, re-indexing each dataframe
        list_of_learners = [df.iloc[0:10].reset_index(drop=True), df.iloc[10:20].reset_index(drop=True),
                            df.iloc[20:30].reset_index(drop=True), df.iloc[30:40].reset_index(drop=True)]

        tmplst = []
        for index, item in enumerate(list_of_learners):
            is_phi_significant_Un_OS, is_normal_significant_Un_OS, is_sera_significant_Un_OS = calculate_significatncy_US_OS(item)

            # Append list2 to list1 and flatten the result
            tmplst.extend([is_phi_significant_Un_OS, is_normal_significant_Un_OS, is_sera_significant_Un_OS])

        sig_df.loc[cleanFileName(file)] = tmplst

    sig_phi_df_Un_OS = sig_df.iloc[:, 0:12:3]
    sig_normal_df_Un_OS = sig_df.iloc[:, 1:12:3]
    sig_sera_df_Un_OS = sig_df.iloc[:, 2:12:3]

    # Rename the columns
    sig_phi_df_Un_OS.columns = sig_normal_df_Un_OS.columns = sig_sera_df_Un_OS.columns  = LearnerTypeLst


    # create the SignificancyFiles directory
    if not os.path.exists(path_SignificancyFiles):
        os.makedirs(path_SignificancyFiles)
        print(f"Directory '{path_SignificancyFiles}' created.")

    # Save to Pickle
    sig_phi_df_Un_OS.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_UNDER_VS_OVER))
    sig_normal_df_Un_OS.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_UNDER_VS_OVER))
    sig_sera_df_Un_OS.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_UNDER_VS_OVER))


    print("Files saved to SignificancyFiles folder!")
    #################################################################

    # change column names
    df_means_phi.columns = COLUMN_NAMES
    df_vars_phi.columns = COLUMN_NAMES
    df_means_normal.columns = COLUMN_NAMES
    df_vars_normal.columns = COLUMN_NAMES
    df_means_sera.columns = COLUMN_NAMES
    df_vars_sera.columns = COLUMN_NAMES

    # Create a new dataframe to just keep the columns of US and OS
    df_means_phi_Un_OS = df_means_phi[COLUMN_NAMES_UN_vs_OS].copy()
    df_vars_phi_Un_OS = df_vars_phi[COLUMN_NAMES_UN_vs_OS].copy()
    df_means_normal_Un_OS = df_means_normal[COLUMN_NAMES_UN_vs_OS].copy()
    df_vars_normal_Un_OS = df_vars_normal[COLUMN_NAMES_UN_vs_OS].copy()
    df_means_sera_Un_OS = df_means_sera[COLUMN_NAMES_UN_vs_OS].copy()
    df_vars_sera_Un_OS = df_vars_sera[COLUMN_NAMES_UN_vs_OS].copy()

    # save the means and vars dataframes to Pickle files
    df_means_phi_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_PHI_Un_OS_pkl))
    df_vars_phi_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_PHI_Un_OS_pkl))
    df_means_normal_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_NORMAL_Un_OS_pkl))
    df_vars_normal_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_NORMAL_Un_OS_pkl))
    df_means_sera_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_SERA_Un_OS_pkl))
    df_vars_sera_Un_OS.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_SERA_Un_OS_pkl))


    # create the win/lost dataframes
    df_winLost_phi_Un_OS = pd.DataFrame(index=df_means_phi_Un_OS.index)
    df_winLost_normal_Un_OS = pd.DataFrame(index=df_means_normal_Un_OS.index)
    df_winLost_sera_Un_OS = pd.DataFrame(index=df_means_sera_Un_OS.index)


    for i in range(0, df_means_phi_Un_OS.shape[1], 2):
        column_name = "{}<{}".format(df_means_phi_Un_OS.columns[i], df_means_phi_Un_OS.columns[i + 1])
        df_winLost_phi_Un_OS[column_name] = df_means_phi_Un_OS.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0, axis=1)
        df_winLost_normal_Un_OS[column_name] = df_means_normal_Un_OS.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0, axis=1)
        df_winLost_sera_Un_OS[column_name] = df_means_sera_Un_OS.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0, axis=1)

        column_name = "{}>{}".format(df_means_phi_Un_OS.columns[i], df_means_phi_Un_OS.columns[i + 1])
        df_winLost_phi_Un_OS[column_name] = df_means_phi_Un_OS.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0, axis=1)
        df_winLost_normal_Un_OS[column_name] = df_means_normal_Un_OS.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0, axis=1)
        df_winLost_sera_Un_OS[column_name] = df_means_sera_Un_OS.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0, axis=1)


    # create the Win_loss_tables directory
    if not os.path.exists(path_win_loss_tables):
        os.makedirs(path_win_loss_tables)
        print(f"Directory '{path_win_loss_tables}' created.")

    # Save to Pickle files
    df_winLost_phi_Un_OS.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Under_vs_Over_pkl))
    df_winLost_normal_Un_OS.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Under_vs_Over_pkl))
    df_winLost_sera_Un_OS.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Under_vs_Over_pkl))

    replicated_sig_phi_df_Un_OS = pd.DataFrame(index=sig_phi_df_Un_OS.index)
    replicated_sig_normal_df_Un_OS = pd.DataFrame(index=sig_normal_df_Un_OS.index)
    replicated_sig_sera_df_Un_OS = pd.DataFrame(index=sig_sera_df_Un_OS.index)
    for col in sig_phi_df_Un_OS.columns:
        replicated_sig_phi_df_Un_OS = pd.concat([replicated_sig_phi_df_Un_OS, sig_phi_df_Un_OS[col].copy()], axis=1)
        replicated_sig_phi_df_Un_OS = pd.concat([replicated_sig_phi_df_Un_OS, sig_phi_df_Un_OS[col].copy()], axis=1)
        replicated_sig_normal_df_Un_OS = pd.concat([replicated_sig_normal_df_Un_OS, sig_normal_df_Un_OS[col].copy()],axis=1)
        replicated_sig_normal_df_Un_OS = pd.concat([replicated_sig_normal_df_Un_OS, sig_normal_df_Un_OS[col].copy()],axis=1)
        replicated_sig_sera_df_Un_OS = pd.concat([replicated_sig_sera_df_Un_OS, sig_sera_df_Un_OS[col].copy()], axis=1)
        replicated_sig_sera_df_Un_OS = pd.concat([replicated_sig_sera_df_Un_OS, sig_sera_df_Un_OS[col].copy()], axis=1)

    # change column names
    replicated_sig_phi_df_Un_OS.columns = df_winLost_phi_Un_OS.columns
    replicated_sig_normal_df_Un_OS.columns = df_winLost_normal_Un_OS.columns
    replicated_sig_sera_df_Un_OS.columns = df_winLost_sera_Un_OS.columns

    # Multiply the win/lost dataframes with the replicated significance dataframes
    df_winLost_phi_sig_Un_OS = df_winLost_phi_Un_OS * replicated_sig_phi_df_Un_OS
    df_winLost_normal_sig_Un_OS = df_winLost_normal_Un_OS * replicated_sig_normal_df_Un_OS
    df_winLost_sera_sig_Un_OS = df_winLost_sera_Un_OS * replicated_sig_sera_df_Un_OS

    # =====================================================
    # number_of_wins_phi_Un_OS = calculate_sum(df_winLost_phi_Un_OS).iloc[[df_winLost_phi_Un_OS.shape[0]], :]
    # number_of_wins_normal_Un_OS = calculate_sum(df_winLost_normal_Un_OS).iloc[[df_winLost_normal_Un_OS.shape[0]], :]
    # number_of_wins_phi_sig_Un_OS = calculate_sum(df_winLost_phi_sig_Un_OS).iloc[[df_winLost_phi_sig_Un_OS.shape[0]], :]
    # number_of_wins_normal_sig_Un_OS = calculate_sum(df_winLost_normal_sig_Un_OS).iloc[[df_winLost_normal_sig_Un_OS.shape[0]], :]
    # number_of_wins_sera_Un_OS = calculate_sum(df_winLost_sera_Un_OS).iloc[[df_winLost_sera_Un_OS.shape[0]], :]
    # number_of_wins_sera_sig_Un_OS = calculate_sum(df_winLost_sera_sig_Un_OS).iloc[[df_winLost_sera_sig_Un_OS.shape[0]], :]
    # =====================================================

    # =====================================================
    # print_df(number_of_wins_phi_Un_OS)
    # print_df(number_of_wins_normal_Un_OS)
    # print_df(number_of_wins_phi_sig_Un_OS)
    # print_df(number_of_wins_normal_sig_Un_OS)
    # print_df(number_of_wins_sera_Un_OS)
    # print_df(number_of_wins_sera_sig_Un_OS)
    # =====================================================

    # prepare the dataframes PHI_UNDER_OVER for the final output
    DF_PHI_Un_OS = pd.concat([df_winLost_phi_Un_OS.sum(axis=0), df_winLost_phi_sig_Un_OS.sum(axis=0)], axis=1)
    DF_PHI_Un_OS.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_PHI_Un_OS["Win/Lost (%)"] = DF_PHI_Un_OS["Win/Lost"] / df_winLost_phi_Un_OS.shape[0]
    DF_PHI_Un_OS["Win/Lost (Significant) (%)"] = DF_PHI_Un_OS["Win/Lost (Significant)"] / df_winLost_phi_sig_Un_OS.shape[0]
    DF_PHI_Un_OS["Win/Lost (%)"] = DF_PHI_Un_OS["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Un_OS["Win/Lost (Significant) (%)"] = DF_PHI_Un_OS["Win/Lost (Significant) (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Un_OS["Win/Lost (%)"] = DF_PHI_Un_OS["Win/Lost (%)"].astype(str)
    DF_PHI_Un_OS["Win/Lost (Significant) (%)"] = DF_PHI_Un_OS["Win/Lost (Significant) (%)"].astype(str)



    # prepare the dataframes NORMAL_UNDER_OVER for the final output
    DF_NORMAL_Un_OS = pd.concat([df_winLost_normal_Un_OS.sum(axis=0), df_winLost_normal_sig_Un_OS.sum(axis=0)], axis=1)
    DF_NORMAL_Un_OS.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_NORMAL_Un_OS["Win/Lost (%)"] = DF_NORMAL_Un_OS["Win/Lost"] / df_winLost_normal_Un_OS.shape[0]
    DF_NORMAL_Un_OS["Win/Lost (Significant) (%)"] = DF_NORMAL_Un_OS["Win/Lost (Significant)"] / df_winLost_normal_sig_Un_OS.shape[0]
    DF_NORMAL_Un_OS["Win/Lost (%)"] = DF_NORMAL_Un_OS["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_Un_OS["Win/Lost (Significant) (%)"] = DF_NORMAL_Un_OS["Win/Lost (Significant) (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_Un_OS["Win/Lost (%)"] = DF_NORMAL_Un_OS["Win/Lost (%)"].astype(str)
    DF_NORMAL_Un_OS["Win/Lost (Significant) (%)"] = DF_NORMAL_Un_OS["Win/Lost (Significant) (%)"].astype(str)

    # prepare the dataframes SERA_UNDER_OVER for the final output
    DF_SERA_Un_OS = pd.concat([df_winLost_sera_Un_OS.sum(axis=0), df_winLost_sera_sig_Un_OS.sum(axis=0)], axis=1)
    DF_SERA_Un_OS.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_SERA_Un_OS["Win/Lost (%)"] = DF_SERA_Un_OS["Win/Lost"] / df_winLost_sera_Un_OS.shape[0]
    DF_SERA_Un_OS["Win/Lost (Significant) (%)"] = DF_SERA_Un_OS["Win/Lost (Significant)"] / df_winLost_sera_sig_Un_OS.shape[0]
    DF_SERA_Un_OS["Win/Lost (%)"] = DF_SERA_Un_OS["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_Un_OS["Win/Lost (Significant) (%)"] = DF_SERA_Un_OS["Win/Lost (Significant) (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_Un_OS["Win/Lost (%)"] = DF_SERA_Un_OS["Win/Lost (%)"].astype(str)
    DF_SERA_Un_OS["Win/Lost (Significant) (%)"] = DF_SERA_Un_OS["Win/Lost (Significant) (%)"].astype(str)

    # create the Win_loss_BARS directory

    if not os.path.exists(path_Win_loss_BARS):
        os.makedirs(path_Win_loss_BARS)
        print(f"Directory '{path_Win_loss_BARS}' created.")

    # create bar plots for the win/loss UNDER_OVER
    barCaption = f"{approach_name}US / {approach_name}OS"
    barCaption = ""

    ################### Create plots Separately
    # create_win_loss_bars(DF_PHI_Un_OS, path_Win_loss_BARS, f"{approach_name}US_OS_phi.png", caption=barCaption)
    # create_win_loss_bars(DF_NORMAL_Un_OS, path_Win_loss_BARS, f"{approach_name}US_OS_normal.png", [-13, -5, -2, 2, 4],  caption=barCaption)
    # create_win_loss_bars(DF_SERA_Un_OS, path_Win_loss_BARS, f"{approach_name}US_OS_sera.png", [-4, -2, 2, 5, 10],
    #                      caption=barCaption)



    ################### Create plots in one figure
    fig = plt.figure(figsize=(5, 1.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1],wspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])]

    handles, labels = create_win_loss_bars_subplot(DF_PHI_Un_OS, axes[0], None, barCaption, "RMSE$\\phi$", True,
                                                   add_legend=True)
    create_win_loss_bars_subplot(DF_SERA_Un_OS, axes[1], [-4, -2, 2, 5, 10], barCaption, "SERA", False)
    create_win_loss_bars_subplot(DF_NORMAL_Un_OS, axes[2], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

    if handles and labels:
        handles, labels = handles[::-1], labels[::-1]
        handles[0], handles[1] = handles[1], handles[0]
        labels[0], labels[1] = labels[1], labels[0]

        fig.legend(
            handles, labels,
            loc='lower center',  # Place the legend at the bottom
            bbox_to_anchor=(0.5, -0.15),  # Move it slightly below the plots
            ncol=len(labels),
            fontsize=5,
            frameon=False
        )

    plt.tight_layout()
    plt.savefig(f"{path_Win_loss_BARS}/{approach_name}US_OS_METRIC.png", dpi=600, bbox_inches="tight")
    #######################################


    print(f"The win/loss bar plots have been created and saved in {Win_loss_BARS}.")
    print(f"Method names:{df_means_phi_Un_OS.columns}")


    lst_rank_phi = findRank(df_means_phi_Un_OS)
    lst_rank_sera = findRank(df_means_sera_Un_OS)
    lst_rank_normal = findRank(df_means_normal_Un_OS)

    df_rank = pd.DataFrame([lst_rank_phi,lst_rank_sera,lst_rank_normal],columns=df_means_phi_Un_OS.columns)
    df_rank.index = ['RSME_phi', 'sera', 'RSME']
    df_rank.columns = ["HistUS","HistOS","HistUS","HistOS","HistUS","HistOS","HistUS","HistOS"]
    df_rank = df_rank.T
    df_table = df_rank.apply(lambda x: f"{' & (0) & '.join(x.dropna().astype(str))} & (0)  \\\\", axis=1)
    print_df(df_table)
    exit(210)

    phi_US_OS_rank_str = " & ".join(map(str, findRank(df_means_phi_Un_OS)))
    normal_US_OS_rank_str = " & ".join(map(str, findRank(df_means_normal_Un_OS)))
    sera_US_OS_rank_str = " & ".join(map(str, findRank(df_means_sera_Un_OS)))

    print(f"Rank in df_means_phi_Un_OS:{phi_US_OS_rank_str}")
    print(f"Rank in df_means_normal_Un_OS:{normal_US_OS_rank_str}")
    print(f"Rank in df_means_sera_Un_OS:{sera_US_OS_rank_str}")

    with open('rankTable_US_OS.tmp', 'r') as file:
        rankTable_US_OS = file.read()
    rankTable_PHI_US_OS = rankTable_US_OS.replace("__METRIC__", "RMSE_{\phi}")
    rankTable_PHI_US_OS = rankTable_PHI_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_PHI")
    rankTable_PHI_US_OS = rankTable_PHI_US_OS.replace("__US__OS__RANKS__", phi_US_OS_rank_str)

    rankTable_Normal_US_OS = rankTable_US_OS.replace("__METRIC__", "RMSE")
    rankTable_Normal_US_OS = rankTable_Normal_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_Normal")
    rankTable_Normal_US_OS = rankTable_Normal_US_OS.replace("__US__OS__RANKS__", normal_US_OS_rank_str)

    rankTable_Sera_US_OS = rankTable_US_OS.replace("__METRIC__", "SERA")
    rankTable_Sera_US_OS = rankTable_Sera_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_Sera")
    rankTable_Sera_US_OS = rankTable_Sera_US_OS.replace("__US__OS__RANKS__", sera_US_OS_rank_str)

    # create the CD_diagrams directory
    if not os.path.exists(path_RANK_TABLE):
        os.makedirs(path_RANK_TABLE)
        print(f"Directory '{path_RANK_TABLE}' created.")

    with open(f"{path_RANK_TABLE}/{approach_name}_phi_rankTable.tex", 'w') as file:
        file.write(rankTable_PHI_US_OS)
    with open(f"{path_RANK_TABLE}/{approach_name}_normal_rankTable.tex", 'w') as file:
        file.write(rankTable_Normal_US_OS)
    with open(f"{path_RANK_TABLE}/{approach_name}_sera_rankTable.tex", 'w') as file:
        file.write(rankTable_Sera_US_OS)

    # create the CD_diagrams directory

    if not os.path.exists(path_CD_disagrams):
        os.makedirs(path_CD_disagrams)
        print(f"Directory '{path_CD_disagrams}' created.")

    saveCDgraph(mapColumnNames(df_means_phi_Un_OS), "{}/{}".format(path_CD_disagrams, f"{approach_name}US_OS_phi.png"))
    saveCDgraph(mapColumnNames(df_means_normal_Un_OS), "{}/{}".format(path_CD_disagrams,
                                                                     f"{approach_name}US_OS_normal.png"))
    saveCDgraph(mapColumnNames(df_means_sera_Un_OS), "{}/{}".format(path_CD_disagrams,
                                                                    f"{approach_name}US_OS_sera.png"))

def createLatexTable_US_OS():
    df_winLost_phi_Un_OS, df_winLost_normal_Un_OS, df_winLost_sera_Un_OS, \
    sig_phi_df_Un_OS, sig_normal_df_Un_OS, sig_sera_df_Un_OS, \
    df_means_phi_Un_OS, df_vars_phi_Un_OS, df_means_normal_Un_OS, \
    df_vars_normal_Un_OS, df_means_sera_Un_OS,df_vars_sera_Un_OS = loadPicklesFiles()

    rankLsts = [findRank(df_means_phi_Un_OS),
                findRank(df_means_normal_Un_OS),
                findRank(df_means_sera_Un_OS)]

    for rankLst,methodName in zip(rankLsts,["phi_Un_OS","normal_Un_OS","sera_Un_OS"]):
        print(rankLst)
        print(f"{20*'-'}{methodName}{20*'-'}")
        # print(tmpAverageRanks.replace("__0__",str(rankLst[0])).replace("__1__",str(rankLst[1])).replace("__2__",
        # str(rankLst[2])).replace("__3__",str(rankLst[3])).replace("__4__",str(rankLst[4])).replace("__5__",
        # str(rankLst[5])).replace("__6__",str(rankLst[6])).replace("__7__",str(rankLst[7])))
        print(50*"-")

    # change column names
    df_means_phi_Un_OS.columns =  df_vars_phi_Un_OS.columns = \
        df_means_normal_Un_OS.columns = df_vars_normal_Un_OS.columns = \
        df_means_sera_Un_OS.columns = df_vars_sera_Un_OS.columns = COLUMN_NAMES_UN_vs_OS


    # df_means_phi_Un_OS,df_means_normal_Un_OS,df_means_sera_Un_OS,df_vars_phi_Un_OS,df_vars_normal_Un_OS,\
    # df_vars_sera_Un_OS = getCleandf(df_means_phi_Un_OS,df_means_normal_Un_OS,df_means_sera_Un_OS,df_vars_phi_Un_OS,
    #                                  df_vars_normal_Un_OS,df_vars_sera_Un_OS)

    # createTable(df_means_phi_Un_OS, df_vars_phi_Un_OS, df_winLost_phi_Un_OS, sig_phi_df_Un_OS, PHI_UN_OS,
    #              path_Latex_tables_folder)
    # createTable(df_means_normal_Un_OS, df_vars_normal_Un_OS, df_winLost_normal_Un_OS, sig_normal_df_Un_OS, NORMAL_UN_OS,
    #              path_Latex_tables_folder)
    # createTable(df_means_sera_Un_OS, df_vars_sera_Un_OS, df_winLost_sera_Un_OS, sig_sera_df_Un_OS, SERA_UN_OS,
    #                 path_Latex_tables_folder)


    if df_means_phi_Un_OS.isna().any().any() or df_vars_phi_Un_OS.isna().any().any() or df_winLost_phi_Un_OS.isna().any().any() or sig_phi_df_Un_OS.isna().any().any():
        print("There is a NaN value in the PHI_UNDER_OVER dataframes!")
        exit(10)


    createLongTableSpringer(df_means_phi_Un_OS, df_vars_phi_Un_OS, df_winLost_phi_Un_OS, sig_phi_df_Un_OS,
                            approach_name, RMSEPHI, path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_normal_Un_OS, df_vars_normal_Un_OS, df_winLost_normal_Un_OS, sig_normal_df_Un_OS,
                            approach_name, RMSE, path_Latex_tables_folder_springer)
    createLongTableSpringer(df_means_sera_Un_OS, df_vars_sera_Un_OS, df_winLost_sera_Un_OS, sig_sera_df_Un_OS,
                            approach_name, SERA, path_Latex_tables_folder_springer)







if __name__ == "__main__":
    main()
    createLatexTable_US_OS()
