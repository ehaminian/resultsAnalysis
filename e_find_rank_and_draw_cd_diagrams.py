from pool_functions import *
from consts import *
import os

def main():

    # load the dataframes from pickle files
    df_means_phi, \
        _, \
        df_means_normal, \
        _, \
        df_means_sera, \
        _ = load_means_vars(path_MEANS_AND_VARS, DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                            DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)



    # change column names
    df_means_phi.columns = COLUMN_NAMES
    df_means_normal.columns = COLUMN_NAMES
    df_means_sera.columns = COLUMN_NAMES


    # Create a new dataframe df_means_phi_Under/df_means_phi_Over by selecting only the COLUMN_NAMES_UNDER columns
    df_means_phi_Under = df_means_phi[COLUMN_NAMES_UNDER].copy()
    df_means_phi_Over = df_means_phi[COLUMN_NAMES_OVER].copy()
    df_means_normal_Under = df_means_normal[COLUMN_NAMES_UNDER].copy()
    df_means_normal_Over = df_means_normal[COLUMN_NAMES_OVER].copy()
    df_means_sera_Under = df_means_sera[COLUMN_NAMES_UNDER].copy()
    df_means_sera_Over = df_means_sera[COLUMN_NAMES_OVER].copy()


    lst_us_rank_phi = findRank(df_means_phi_Under)
    lst_us_rank_sera = findRank(df_means_sera_Under)
    lst_us_rank_normal = findRank(df_means_normal_Under)

    # put the above list into a rows of a dataframe
    df = pd.DataFrame([lst_us_rank_phi, lst_us_rank_sera, lst_us_rank_normal])
    df.index = ['RSME_phi', 'sera', 'RSME']
    df = df.T
    df.index = ["Baseline","HistUS","Baseline","HistUS","Baseline","HistUS","Baseline","HistUS"]
    df_table = df.apply(lambda x:   f"{' & (0) & '.join(x.dropna().astype(str))} & (0)  \\\\", axis=1)
    df_table.index= df.index
    #4.15 & (0) & 6.38 & (0) & 2.58 & (8)  \\
    #3.83 & (0) & 6.25 & (0) & 2.38
    print("Table Baseline/HistUS comparison")
    print_df(df_table)

    lst_os_rank_phi = findRank(df_means_phi_Over)
    lst_os_rank_normal = findRank(df_means_normal_Over)
    lst_os_rank_sera = findRank(df_means_sera_Over)
    # put the above list into a rows of a dataframe
    df = pd.DataFrame([lst_os_rank_phi, lst_os_rank_sera, lst_os_rank_normal])
    df.index = ['RSME_phi', 'sera', 'RSME']
    df = df.T
    df.index = ["Baseline","HistOS","Baseline","HistOS","Baseline","HistOS","Baseline","HistOS"]
    df_table = df.apply(lambda x:   f"{' & (0) & '.join(x.dropna().astype(str))} & (0)  \\\\", axis=1)
    df_table.index= df.index
    print(50*"-")
    print("Table Baseline/HistOS comparison")
    print_df(df_table)


    # phi_US_rank_str = " & ".join(map(str, findRank(df_means_phi_Under)))
    # phi_OS_rank_str = " & ".join(map(str, findRank(df_means_phi_Over)))
    # normal_US_rank_str = " & ".join(map(str, findRank(df_means_normal_Under)))
    # normal_OS_rank_str = " & ".join(map(str, findRank(df_means_normal_Over)))
    # sera_US_rank_str = " & ".join(map(str, findRank(df_means_sera_Under)))
    # sera_OS_rank_str = " & ".join(map(str, findRank(df_means_sera_Over)))


    # print(f"{approach_name}_phi_US:{phi_US_rank_str}")
    # print(f"{approach_name}_phi_OS:{phi_OS_rank_str}")
    # print(f"{approach_name}_normal_US:{normal_US_rank_str}")
    # print(f"{approach_name}_normal_OS:{normal_OS_rank_str}")
    # print(f"{approach_name}_sera_US:{sera_US_rank_str}")
    # print(f"{approach_name}_sera_OS:{sera_OS_rank_str}")



    # with open('rankTable.tmp', 'r') as file:
    #     rankTableTmp = file.read()
    # rankTable_PHI_US_OS = rankTableTmp.replace("__US__RANKS__", phi_US_rank_str)
    # rankTable_PHI_US_OS = rankTable_PHI_US_OS.replace("__OS__RANKS__", phi_OS_rank_str)
    # rankTable_PHI_US_OS = rankTable_PHI_US_OS.replace("__METRIC__", "RMSE_{\phi}")
    # rankTable_PHI_US_OS = rankTable_PHI_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_PHI")
    #
    # rankTable_Normal_US_OS = rankTableTmp.replace("__US__RANKS__", normal_US_rank_str)
    # rankTable_Normal_US_OS = rankTable_Normal_US_OS.replace("__OS__RANKS__", normal_OS_rank_str)
    # rankTable_Normal_US_OS = rankTable_Normal_US_OS.replace("__METRIC__", "RMSE")
    # rankTable_Normal_US_OS = rankTable_Normal_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_Normal")
    #
    # rankTable_Sera_US_OS = rankTableTmp.replace("__US__RANKS__", sera_US_rank_str)
    # rankTable_Sera_US_OS = rankTable_Sera_US_OS.replace("__OS__RANKS__", sera_OS_rank_str)
    # rankTable_Sera_US_OS = rankTable_Sera_US_OS.replace("__METRIC__", "SERA")
    # rankTable_Sera_US_OS = rankTable_Sera_US_OS.replace("__LABEL__", "tab:Sum_HistUS_OS_Sera")



    # create the CD_diagrams directory
    createRequiredDirectories(path_CD_disagrams)

    # save the rank tables - still "Sign. Wins" needs to be filled manually

    # with open(f"{path_CD_disagrams}/{approach_name}_phi_rankTable.tex", 'w') as file:
    #     file.write(rankTable_PHI_US_OS)
    # with open(f"{path_CD_disagrams}/{approach_name}_normal_rankTable.tex", 'w') as file:
    #     file.write(rankTable_Normal_US_OS)
    # with open(f"{path_CD_disagrams}/{approach_name}_sera_rankTable.tex", 'w') as file:
    #     file.write(rankTable_Sera_US_OS)

    # save the CD diagrams
    saveCDgraph(mapColumnNames(df_means_phi_Under), f"{path_CD_disagrams}/{approach_name}US_phi.png")
    saveCDgraph(mapColumnNames(df_means_phi_Over), f"{path_CD_disagrams}/{approach_name}OS_phi.png")
    saveCDgraph(mapColumnNames(df_means_normal_Under), f"{path_CD_disagrams}/{approach_name}US_normal.png")
    saveCDgraph(mapColumnNames(df_means_normal_Over), f"{path_CD_disagrams}/{approach_name}OS_normal.png")
    saveCDgraph(mapColumnNames(df_means_sera_Under), f"{path_CD_disagrams}/{approach_name}US_sera.png")
    saveCDgraph(mapColumnNames(df_means_sera_Over), f"{path_CD_disagrams}/{approach_name}OS_sera.png")

    print(f"CD diagrams are saved successfully in {path_CD_disagrams}!")


if __name__ == "__main__":
    main()
