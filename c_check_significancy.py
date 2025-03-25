import os
from consts import *
from pool_functions import *


def main():

    list_of_the_datasets = []

    # Save the results of each learner type in a dataframe
    sig_df = pd.DataFrame(columns=["phi_under", "phi_over", "normal_under", "normal_over", "sera_under", "sera_over",
                                   "phi_under", "phi_over", "normal_under", "normal_over", "sera_under", "sera_over",
                                   "phi_under", "phi_over", "normal_under", "normal_over", "sera_under", "sera_over",
                                   "phi_under", "phi_over", "normal_under", "normal_over", "sera_under", "sera_over"
                                   ])

    # walk through all csv files in the Results folder
    for file in os.listdir(path_to_Results_OS_US):

        df = read_csv("{}/{}".format(path_to_Results_OS_US, file))
        list_of_the_datasets.append(file)
        # divide the dataframe into four dataframes each having 10 rows, re-indexing each dataframe
        list_of_learners = [df.iloc[0:10].reset_index(drop=True), df.iloc[10:20].reset_index(drop=True),
                            df.iloc[20:30].reset_index(drop=True), df.iloc[30:40].reset_index(drop=True)]

        tmplst = []
        for index, item in enumerate(list_of_learners):
            is_phi_significant_Under, is_phi_significant_Over,\
                is_normal_significant_Under,is_normal_significant_Over,\
                is_sera_significant_Under, is_sera_significant_Over = calculate_significatncy(item)

            # Append list2 to list1 and flatten the result
            tmplst.extend([is_phi_significant_Under, is_phi_significant_Over, is_normal_significant_Under,
                           is_normal_significant_Over, is_sera_significant_Under, is_sera_significant_Over])

        sig_df.loc[cleanFileName(file)] = tmplst

    sig_phi_df_Under = sig_df.iloc[:, 0:24:6]
    sig_phi_df_Over = sig_df.iloc[:, 1:24:6]
    sig_normal_df_Under = sig_df.iloc[:, 2:24:6]
    sig_normal_df_Over = sig_df.iloc[:, 3:24:6]
    sig_sera_df_Under = sig_df.iloc[:, 4:24:6]
    sig_sera_df_Over = sig_df.iloc[:, 5:24:6]


    # Rename the columns
    sig_phi_df_Under.columns = sig_phi_df_Over.columns =\
        sig_normal_df_Under.columns = sig_normal_df_Over.columns =\
        sig_sera_df_Under.columns = sig_sera_df_Over.columns = LearnerTypeLst

    # print_df(sig_df)
    # print_df(sig_phi_df_Under)
    # print_df(sig_phi_df_Over)
    # print_df(sig_normal_df_Under)
    # print_df(sig_normal_df_Over)
    # print_df(sig_sera_df_Under)
    # print_df(sig_sera_df_Over)


    # Save to Pickle files to $MEANS_AND_VARS
    if not os.path.exists(path_SignificancyFiles):
        os.makedirs(path_SignificancyFiles)
        print(f"Directory '{path_SignificancyFiles}' created.")

    # Save to Pickle
    sig_phi_df_Under.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_UNDER))
    sig_phi_df_Over.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_PHI_DF_OVER))
    sig_normal_df_Under.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_UNDER))
    sig_normal_df_Over.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_NORMAL_DF_OVER))
    sig_sera_df_Under.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_UNDER))
    sig_sera_df_Over.to_pickle("{}/{}".format(path_SignificancyFiles, SIG_SERA_DF_OVER))

    print(f"Files saved to {path_SignificancyFiles} folder!")


if __name__ == "__main__":
    main()
