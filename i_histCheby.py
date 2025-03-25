import os
import pandas as pd
from matplotlib import pyplot as plt

from consts import _HistogramNewResults, _chebyshevNewResults, latex_tables_folder_springer, \
    DF_MEANS_PHI_pkl_CHEBY_HIST_UNDER, DF_VARS_PHI_pkl_CHEBY_HIST_UNDER, DF_MEANS_SERA_pkl_CHEBY_HIST_UNDER, \
    DF_VARS_SERA_pkl_CHEBY_HIST_UNDER, DF_MEANS_PHI_pkl_CHEBY_HIST_OVER, DF_VARS_PHI_pkl_CHEBY_HIST_OVER, \
    DF_MEANS_SERA_pkl_CHEBY_HIST_OVER, DF_VARS_SERA_pkl_CHEBY_HIST_OVER, plusMinusLatex, triLeftLatex, triRightLatex, \
    OVER, UNDER
from numpy.ma.core import zeros
from analyse.consts import DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl, DF_VARS_NORMAL_pkl, \
    DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl, MEANS_AND_VARS, LEARNERS, Results_OS_US, Win_loss_BARS
from pool_functions import load_means_vars, print_df, read_csv, wilcoxon_signed_rank_test, cleanFileName, saveCDgraph, \
    findRank, create_win_loss_bars, mapColumnNames, formatValues, create_win_loss_bars_subplot

RMSEPHIUNDER="RmsePhi_Under"
RMSEPHIOVER="RmsePhi_Over"
RMSEUNDER="Rmse_Under"
RMSOVER="Rmse_Over"
SERAUNDER="Sera_Under"
SERAOVER="Sera_Over"
HISTCHEBYRESULTSFOLDER = "ChebyHistResults"
CDDIAGRAMSFOLDER = "CD_diagrams"
RANKTABLES = "RankTables"
RMSEPHI="RMSE_{\phi}"
SERA="SERA"
CHEBYUS="ChebyUS"
CHEBYOS="ChebyOS"
HISTUS="HistUS"
HISTOS="HistOS"
LST_METHODS_METRICS = [RMSEPHIUNDER, RMSEPHIOVER, RMSEUNDER, RMSOVER, SERAUNDER, SERAOVER]

def extractTriLatex(value):
    #different from the one in pool_functions.py
    if value == "00":
        return ""
    elif value == "01":
        return triRightLatex
    elif value == "10":
        return triLeftLatex
    elif value == "11":
        raise ValueError("Invalid value")

def interleave(df1, df2):
    if df1.shape[1] != df2.shape[1]:
        raise ValueError("Both dataframes must have the same number of columns")
    combined_df = pd.DataFrame()
    for index, (col1, col2) in enumerate(zip(df1.columns, df2.columns)):
        combined_df[f"{LEARNERS[index]}_{col1}"] = df1.iloc[:, index]
        combined_df[f"{LEARNERS[index]}_{col2}"] = df2.iloc[:, index]
    return combined_df

def getInterleave(df1, df2, type):
    df1=df1.filter(like=type)
    df2=df2.filter(like=type)
    return interleave(df1, df2)

def getPath(methodPath,directory):
    return f"{methodPath}{directory[1:]}"

def getColumn(df,metric_type):
    if metric_type == "RmsePhi_Under":
        return df.iloc[:, 1]
    elif metric_type == "RmsePhi_Over":
        return df.iloc[:, 2]
    elif metric_type == "Rmse_Under":
        return df.iloc[:, 4]
    elif metric_type == "Rmse_Over":
        return df.iloc[:, 5]
    elif metric_type == "Sera_Under":
        return df.iloc[:, 7]
    elif metric_type == "Sera_Over":
        return df.iloc[:, 8]
    else:
        raise ValueError("Invalid metric type")

def significant(res1,res2):
    stat, p_value = wilcoxon_signed_rank_test(res1, res2)
    if stat is not None:
        is_res2_significant = 1 if p_value < 0.05 else 0
        return is_res2_significant
    return None

def get_sig_df(METHOD_METRIC):
    type = METHOD_METRIC.split("_")[1]
    sig_mapping = {0: [0, 0],1: [1, 1],None: [0, 0]}
    fileLists = os.listdir(getPath(_chebyshevNewResults,Results_OS_US))
    list_of_the_datasets = []
    sig_df = pd.DataFrame(columns=[""]*8)
    for file in fileLists:
        df_cheby = read_csv(f"{getPath(_chebyshevNewResults,Results_OS_US)}/{file}")
        df_hist =  read_csv(f"{getPath(_HistogramNewResults,Results_OS_US)}/{file}")
        list_of_the_datasets.append(file)
        list_of_learners_cheby = [df_cheby.iloc[0:10].reset_index(drop=True), df_cheby.iloc[10:20].reset_index(drop=True),
                            df_cheby.iloc[20:30].reset_index(drop=True), df_cheby.iloc[30:40].reset_index(drop=True)]
        list_of_learners_hist = [df_hist.iloc[0:10].reset_index(drop=True), df_hist.iloc[10:20].reset_index(drop=True),
                            df_hist.iloc[20:30].reset_index(drop=True), df_hist.iloc[30:40].reset_index(drop=True)]
        list_of_learners_phi_cheby = [getColumn(itemLst, METHOD_METRIC) for itemLst in list_of_learners_cheby]
        list_of_learners_phi_hist = [getColumn(itemLst, METHOD_METRIC) for itemLst in list_of_learners_hist]
        df_phi_cheby = pd.concat(list_of_learners_phi_cheby, axis=1)
        df_phi_hist = pd.concat(list_of_learners_phi_hist, axis=1)
        df_phi = getInterleave(df_phi_cheby,df_phi_hist,type)
        tmp_lst = [significant(df_phi.iloc[:, i],df_phi.iloc[:, i+1]) for i in range(0,df_phi.shape[1]) if i%2==0]
        sig_df.columns = df_phi.columns
        sig_df.loc[cleanFileName(file)] = [item for x in tmp_lst for item in sig_mapping[x]]
    return sig_df

def createRequiredDirectories(directories):
    if isinstance(directories, str):
        directories = [directories]
    if not os.path.exists(HISTCHEBYRESULTSFOLDER):
        os.makedirs(HISTCHEBYRESULTSFOLDER)
        print(f"Directory '{HISTCHEBYRESULTSFOLDER}' created.")
    directories = [f"./{HISTCHEBYRESULTSFOLDER}/{directory}" for directory in directories]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")

def getRankTmp():
    with open('rankTableChebyHist.tmp', 'r') as file:
        return file.read()

def saveRankTable(metric, type, approche1, approche2, ranks):
    rankTableChebyHist = getRankTmp()
    lable_metric=metric.replace(RMSEPHI,"phi")
    tmp = rankTableChebyHist\
        .replace("__METRIC__", metric)\
        .replace("__TYPE__", type)\
        .replace("__LABEL__", f"tab:Sum_{approche1}_{approche2}_{lable_metric}_{type}")\
        .replace("__APPROCHE1__", approche1)\
        .replace("__APPROCHE2__", approche2)\
        .replace("__CHEBY__HIST__RANKS__", ranks)
    targetPath=f"./{HISTCHEBYRESULTSFOLDER}/{RANKTABLES}"
    metric = metric.replace("RMSE_{\phi}","phi")
    with open(f"{targetPath}/rankTable_{approche1}_{approche2}_{metric}_{type}.tex",
              'w') as file:
        file.write(tmp)

def createIndexNamesWinLostDF(df_interleave):
    lst_col = df_interleave.columns
    lst=[]
    for index,_ in enumerate(lst_col):
        if index%2==0:
            lst.extend([f"{lst_col[index]}<{lst_col[index+1]}",f"{lst_col[index]}>{lst_col[index+1]}"])
    return lst

def createColumnsWinLostDF():
    return ["Win/Lost","Win/Lost (Significant)","Win/Lost (%)","Win/Lost (Significant) (%)"]

def calculateWinLostsAndPercentage(df_means_cheby_hist):
    lstWin_Lost=[]
    lstWin_Lost_PERCENTAGE=[]
    t3= df_means_cheby_hist.shape[0]
    for index in range(0,df_means_cheby_hist.shape[1],2):
        t1 = df_means_cheby_hist.apply(lambda x: x[index] < x[index+1], axis=1).value_counts().get(True)
        t2 = df_means_cheby_hist.apply(lambda x: x[index] > x[index+1], axis=1).value_counts().get(True)
        lstWin_Lost.extend([t1,t2])
        lstWin_Lost_PERCENTAGE.extend([f"{(t1/t3)*100:.2f}%",f"{(t2/t3)*100:.2f}%"])
    return lstWin_Lost,lstWin_Lost_PERCENTAGE

def create_winLost_0_1_df(df_means):
    winLost_0_1_df = pd.DataFrame(columns=df_means.columns)
    for i in range(0, df_means.shape[1], 2):
        col0 = df_means.iloc[:, i]
        col1 = df_means.iloc[:, i+1]
        winLost_0_1_df.iloc[:,i] = (col0 < col1).astype(int)
        winLost_0_1_df.iloc[:,i+1] = (col1 < col0).astype(int)
    return winLost_0_1_df

def main_createRankTableandCDgraphs():
    createRequiredDirectories([CDDIAGRAMSFOLDER,RANKTABLES,latex_tables_folder_springer[2:]])
    springer_file_directory = f"./{HISTCHEBYRESULTSFOLDER}/{latex_tables_folder_springer[2:]}"

    # load chebyshev dataframes
    df_means_phi_cheby, \
        df_vars_phi_cheby, \
        df_means_normal_cheby, \
        df_vars_normal_cheby, \
        df_means_sera_cheby, \
        df_vars_sera_cheby = load_means_vars(f"{_chebyshevNewResults}{MEANS_AND_VARS[1:]}",
                                             DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                                             DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)

    # load histogram dataframes
    df_means_phi_hist, \
        df_vars_phi_hist, \
        df_means_normal_hist, \
        df_vars_normal_hist, \
        df_means_sera_hist, \
        df_vars_sera_hist = load_means_vars(f"{_HistogramNewResults}{MEANS_AND_VARS[1:]}",
                                             DF_MEANS_PHI_pkl,DF_VARS_PHI_pkl,DF_MEANS_NORMAL_pkl,
                                            DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)

    targetPath=f"./{HISTCHEBYRESULTSFOLDER}/{CDDIAGRAMSFOLDER}"



    type=UNDER
    df_means_phi_cheby_hist = getInterleave(df_means_phi_cheby, df_means_phi_hist,type )
    df_means_sera_cheby_hist = getInterleave(df_means_sera_cheby, df_means_sera_hist, type)
    df_vars_phi_cheby_hist = getInterleave(df_vars_phi_cheby, df_vars_phi_hist,type )
    df_vars_sera_cheby_hist = getInterleave(df_vars_sera_cheby, df_vars_sera_hist,type )
    saveCDgraph(mapColumnNames(df_means_phi_cheby_hist), f"{targetPath}/chebyHist_{RMSEPHIUNDER}",6,1.8)
    saveCDgraph(mapColumnNames(df_means_sera_cheby_hist), f"{targetPath}/chebyHist_{SERAUNDER}",6,1.8)
    phi_cheby_hist_US_rank_str = " & ".join(map(str, findRank(df_means_phi_cheby_hist)))
    sera_cheby_hist_US_rank_str = " & ".join(map(str, findRank(df_means_sera_cheby_hist)))




    # save to pickle files
    df_means_phi_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_MEANS_PHI_pkl_CHEBY_HIST_UNDER))
    df_vars_phi_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_VARS_PHI_pkl_CHEBY_HIST_UNDER))
    df_means_sera_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_MEANS_SERA_pkl_CHEBY_HIST_UNDER))
    df_vars_sera_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_VARS_SERA_pkl_CHEBY_HIST_UNDER))



    type=OVER
    df_means_phi_cheby_hist = getInterleave(df_means_phi_cheby, df_means_phi_hist,type )
    df_means_sera_cheby_hist = getInterleave(df_means_sera_cheby, df_means_sera_hist,type )
    df_vars_phi_cheby_hist = getInterleave(df_vars_phi_cheby, df_vars_phi_hist,type )
    df_vars_sera_cheby_hist = getInterleave(df_vars_sera_cheby, df_vars_sera_hist,type )
    saveCDgraph(mapColumnNames(df_means_phi_cheby_hist), f"{targetPath}/chebyHist_{RMSEPHIOVER}",6,1.8)
    saveCDgraph(mapColumnNames(df_means_sera_cheby_hist), f"{targetPath}/chebyHist_{SERAOVER}",6,1.8)
    phi_cheby_hist_OS_rank_str = " & ".join(map(str, findRank(df_means_phi_cheby_hist)))
    sera_cheby_hist_OS_rank_str = " & ".join(map(str, findRank(df_means_sera_cheby_hist)))

    # save to pickle files
    df_means_phi_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_MEANS_PHI_pkl_CHEBY_HIST_OVER))
    df_vars_phi_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_VARS_PHI_pkl_CHEBY_HIST_OVER))
    df_means_sera_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_MEANS_SERA_pkl_CHEBY_HIST_OVER))
    df_vars_sera_cheby_hist.to_pickle("{}/{}".format(springer_file_directory, DF_VARS_SERA_pkl_CHEBY_HIST_OVER))

    # save rank tables
    saveRankTable(RMSEPHI, UNDER, CHEBYUS, HISTUS, phi_cheby_hist_US_rank_str)
    saveRankTable(RMSEPHI, OVER, CHEBYOS, HISTOS, phi_cheby_hist_OS_rank_str)
    saveRankTable(SERA, UNDER, CHEBYUS, HISTUS, sera_cheby_hist_US_rank_str)
    saveRankTable(SERA, OVER, CHEBYOS, HISTOS, sera_cheby_hist_OS_rank_str)
    print("Rank tableds were created successfully. Dont forget to change the number of sig wins and lost manually "
          "which are "
          "all 0")
    return 0





def main_createWinLostBars(df_means_metric_cheby,df_means_metric_hist,samplingMethod,MethodMetric,method1,method2):
    df_means_metric_cheby_hist = getInterleave(df_means_metric_cheby, df_means_metric_hist, samplingMethod)
    df = pd.DataFrame(zeros((len(df_means_metric_cheby_hist.columns), 4)), index=createIndexNamesWinLostDF(df_means_metric_cheby_hist), columns=createColumnsWinLostDF())
    lstWin_Lost,lstWin_Lost_PERCENTAGE=calculateWinLostsAndPercentage(df_means_metric_cheby_hist)
    df.iloc[:,0]= lstWin_Lost
    df.iloc[:,2]= lstWin_Lost_PERCENTAGE
    sig_df_metric_cheby_hist=get_sig_df(MethodMetric)
    winLost_df_0_1 = create_winLost_0_1_df(df_means_metric_cheby_hist)
    sigWinLost = sig_df_metric_cheby_hist * winLost_df_0_1
    t1=sigWinLost.sum(axis=0)
    t1.index=df.index
    df.iloc[:,1]=t1
    df.iloc[:,3]=t1/sigWinLost.shape[0]*100
    fileName = f"winLostbars_ChebyHist_{MethodMetric}.png"
    path=f"./{HISTCHEBYRESULTSFOLDER}/{Win_loss_BARS[1:]}"
    caption=f"{method1}/{method2}"
    caption=""
    return df, fileName, path, caption


def createLongTableSpringer(df_means_metric_cheby, df_means_metric_hist,df_vars_metric_cheby ,df_vars_metric_hist,
                            samplingMethod,MethodMetric,directoryTosave):

    # sample rows of the table should look like this:
    ####################################################################################################################
    #puma32H     & 0.032 $\pm$ 0.000             & \textbf{0.028 $\pm$ 0.000}            & 0.050 $\pm$ 0.000         & $\triangleright$ 0.040 $\pm$ 0.000 & \bftab 0.031 $\pm$ 0.000 & $\triangleleft$ 0.046 $\pm$ 0.000 & 0.070 $\pm$ 0.000 & 0.070 $\pm$ 0.000 \\
    #cpusum      & \bftab 10.73 $\pm$ 0.443      & $\triangleleft$ 16.29 $\pm$ 5.629     & \bftab 8.693 $\pm$ 0.830  &
    # $\triangleleft$ 25.25 $\pm$ 75.01 & \bftab 11.02 $\pm$ 0.744 & $\triangleleft$ 55.90 $\pm$ 43.12 & 22.83 $\pm$ 1.568 & $\triangleright$ \bftab 14.49 $\pm$ 0.495 \\
    ####################################################################################################################
    df_means_metric_cheby_hist = getInterleave(df_means_metric_cheby, df_means_metric_hist, samplingMethod)
    df_vars_metric_cheby_hist = getInterleave(df_vars_metric_cheby, df_vars_metric_hist, samplingMethod)
    sig_df_metric_cheby_hist=get_sig_df(MethodMetric)
    winLost_df_0_1 = create_winLost_0_1_df(df_means_metric_cheby_hist)
    sig_winLost = sig_df_metric_cheby_hist * winLost_df_0_1

    print_df(sig_winLost)

    rankRow=findRank(df_means_metric_cheby_hist)
    rankRowStr=" & ".join(map(str,rankRow))

    df_means_metric_cheby_hist=df_means_metric_cheby_hist.applymap(formatValues)
    df_vars_metric_cheby_hist=df_vars_metric_cheby_hist.applymap(formatValues)

    df_concatenated = df_means_metric_cheby_hist.astype(str) + plusMinusLatex + df_vars_metric_cheby_hist.astype(str)
    df_concatenated = df_concatenated.where(winLost_df_0_1 == 0 , '\\textbf{' + df_concatenated + '}')

    cheby_sig_win=sig_winLost.iloc[:, ::2].astype(str)
    hist_sig_win=sig_winLost.iloc[:, 1::2].astype(str)
    cheby_sig_win.columns = hist_sig_win.columns = ["AMRules","FIMTDD","Perceptron","TargetMean"]
    compacted_sig_winLost = cheby_sig_win + hist_sig_win

    triangle_df = compacted_sig_winLost.applymap(extractTriLatex)
    for i in range(1, len(df_concatenated.columns), 2):
        df_concatenated.iloc[:, i] = triangle_df.iloc[:, int(i/2)] + df_concatenated.iloc[:, i]


    latexTableRows = df_concatenated.apply(lambda row: " & ".join([str(row.name)] + list(row)) + " \\\\ ", axis=1)
    latexTableRows = latexTableRows.tolist()


    metric = RMSEPHI if (MethodMetric == RMSEPHIUNDER) or (MethodMetric == RMSEPHIOVER) else SERA
    metric_clean = metric.replace("{\phi}", "phi")
    if samplingMethod == UNDER:
        label=f"{CHEBYUS}_{HISTUS}_{metric_clean}"
        methods=f"{CHEBYUS} VS {HISTUS}"
    elif samplingMethod == OVER:
        label=f"{CHEBYOS}_{HISTOS}_{metric_clean}"
        methods = f"{CHEBYOS} VS {HISTOS}"
    else:
        raise ValueError("Invalid sampling method")

    # construct the headers row __TABLE_HEADER__
    US_HEARDERS_ROW=(f"Dataset & {CHEBYUS} & {HISTUS} & {CHEBYUS} & {HISTUS} & {CHEBYUS} & {HISTUS} & {CHEBYUS} & "
                     f"{HISTUS} \\\\")
    OS_HEARDERS_ROW=(f"Dataset & {CHEBYOS} & {HISTOS} & {CHEBYOS} & {HISTOS} & {CHEBYOS} & {HISTOS} & {CHEBYOS} & "
                     f"{HISTOS} \\\\")

    with open('springerTable_compare_cheby_hist.tmp', 'r') as file:
        latexTableTmp = file.read()



    latexTable = latexTableTmp.replace("__TABLE_ROWS__", "\n".join(latexTableRows)).\
                            replace("__METRIC__", metric).\
                            replace("__TABLE_HEADER__", US_HEARDERS_ROW if samplingMethod==UNDER else OS_HEARDERS_ROW). \
                            replace("__METHODS__", methods). \
                            replace("__LABEL__",label ).\
                            replace("__RANK_ROW__",rankRowStr)

    # create the Latex_tables_folder directory
    if not os.path.exists(directoryTosave):
        os.makedirs(directoryTosave)
        print(f"Directory '{directoryTosave}' created.")

    file_path = f"{directoryTosave}/{label}.tex"
    with open(file_path, 'w') as file:
        file.write(latexTable)
    print("Latex table is saved successfully in {}!".format(file_path))

############################################
#PART 2
############################################

createRequiredDirectories([Win_loss_BARS])
df_means_phi_cheby, \
    df_vars_phi_cheby, \
    df_means_normal_cheby, \
    df_vars_normal_cheby, \
    df_means_sera_cheby, \
    df_vars_sera_cheby = load_means_vars(f"{_chebyshevNewResults}{MEANS_AND_VARS[1:]}",
                                         DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                                         DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)

df_means_phi_hist, \
    df_vars_phi_hist, \
    df_means_normal_hist, \
    df_vars_normal_hist, \
    df_means_sera_hist, \
    df_vars_sera_hist = load_means_vars(f"{_HistogramNewResults}{MEANS_AND_VARS[1:]}",
                                         DF_MEANS_PHI_pkl,DF_VARS_PHI_pkl,DF_MEANS_NORMAL_pkl,
                                        DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)
if __name__ == "__main__":
    main_createRankTableandCDgraphs()



    # create win/loss bars for in one plot
    fig = plt.figure(figsize=(5, 1.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]


    # Under-sampling RMSE_{\phi}
    df, fileName, path, caption = main_createWinLostBars(df_means_phi_cheby,df_means_phi_hist,UNDER,RMSEPHIUNDER,CHEBYUS,HISTUS)
    handles, labels = create_win_loss_bars_subplot(df, axes[0], None, caption, "RMSE$\\phi$", True,add_legend=True)




    # Under-sampling SERA
    df, fileName, path, caption = main_createWinLostBars(df_means_sera_cheby,df_means_sera_hist,UNDER,SERAUNDER,CHEBYUS,HISTUS)
    create_win_loss_bars_subplot(df, axes[1], handles, caption, "SERA", False)



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

    plt.savefig(f"{path}/winLostbars_ChebyHist__{CHEBYUS}-{HISTUS}.png", dpi=600, bbox_inches="tight")
    #######################################



    # create win/loss bars for in one plot
    fig = plt.figure(figsize=(5, 1.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]


    # Over-sampling RMSE_{\phi}#
    df, fileName, path, caption = main_createWinLostBars(df_means_phi_cheby, df_means_phi_hist, OVER, RMSEPHIOVER,CHEBYOS, HISTOS)
    handles, labels = create_win_loss_bars_subplot(df, axes[0], None, caption, "RMSE$\\phi$", True,add_legend=True)

    # Over-sampling SERA
    df, fileName, path, caption = main_createWinLostBars(df_means_sera_cheby,df_means_sera_hist,OVER,SERAOVER,CHEBYOS,HISTOS)
    create_win_loss_bars_subplot(df, axes[1], handles, caption, "SERA", False)



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
    plt.savefig(f"{path}/winLostbars_ChebyHist__{CHEBYOS}-{HISTOS}.png", dpi=600, bbox_inches="tight")












    springer_file_directory = f"./{HISTCHEBYRESULTSFOLDER}/{latex_tables_folder_springer[2:]}"

    try:
        createLongTableSpringer(df_means_phi_cheby, df_means_phi_hist, df_vars_phi_cheby, df_vars_phi_hist,
                            UNDER,RMSEPHIUNDER, springer_file_directory)
    except Exception as e:
        print(e)
        print(50*"-")
        print_df(df_means_phi_cheby)
        print(50 * "-")
        print_df(df_means_phi_hist)
        exit(160)
    createLongTableSpringer(df_means_phi_cheby, df_means_phi_hist, df_vars_phi_cheby, df_vars_phi_hist,
                            OVER,RMSEPHIOVER, springer_file_directory)
    createLongTableSpringer(df_means_sera_cheby, df_means_sera_hist, df_vars_sera_cheby, df_vars_sera_hist,
                            UNDER,SERAUNDER, springer_file_directory)
    createLongTableSpringer(df_means_sera_cheby, df_means_sera_hist, df_vars_sera_cheby, df_vars_sera_hist,
                            OVER,SERAOVER, springer_file_directory)








