import os
from consts import *
from pool_functions import *


def main():
    # create an empty dataframe
    df_means_phi = pd.DataFrame()
    df_vars_phi = pd.DataFrame()
    df_means_normal = pd.DataFrame()
    df_vars_normal = pd.DataFrame()
    df_means_sera = pd.DataFrame()
    df_vars_sera = pd.DataFrame()

    # create an empty list to store the names of the datasets
    list_of_the_datasets = []

    # walk through all csv files in the Results folder
    for file in os.listdir(path_to_Results_OS_US):

        df = read_csv("{}/{}".format(path_to_Results_OS_US, file))
        list_of_the_datasets.append(file)

        # divide the dataframe into four dataframes each having 10 rows, re-indexing each dataframe
        list_of_learners = [df.iloc[0:10].reset_index(drop=True), df.iloc[10:20].reset_index(drop=True),
                            df.iloc[20:30].reset_index(drop=True), df.iloc[30:40].reset_index(drop=True)]

        # calculate mean and variance for each dataframe column and append to the dataframe itself
        for index, item in enumerate(list_of_learners):
            list_of_learners[index] = calculate_mean_and_variance(item)

        # insert related columns into separate dataframes
        list_of_learners_phi = [item.iloc[:, 0:3] for item in list_of_learners]
        list_of_learners_normal = [item.iloc[:, 3:6] for item in list_of_learners]
        list_of_learners_sera = [item.iloc[:, 6:9] for item in list_of_learners]

        # concatenate all dataframes into one dataframe horizontally
        df_phi = pd.concat(list_of_learners_phi, axis=1)
        df_normal = pd.concat(list_of_learners_normal, axis=1)
        df_sera = pd.concat(list_of_learners_sera, axis=1)

        # just keep the mean and variance rows
        df_phi = df_phi.iloc[[10, 11], :]
        df_normal = df_normal.iloc[[10, 11], :]
        df_sera = df_sera.iloc[[10, 11], :]

        # append the mean and variance of each dataframe to the empty dataframe
        df_means_phi = df_means_phi.append(df_phi.iloc[0, :].reset_index(drop=True)).reset_index(drop=True)
        df_vars_phi = df_vars_phi.append(df_phi.iloc[1, :].reset_index(drop=True)).reset_index(drop=True)
        df_means_normal = df_means_normal.append(df_normal.iloc[0, :].reset_index(drop=True)).reset_index(drop=True)
        df_vars_normal = df_vars_normal.append(df_normal.iloc[1, :].reset_index(drop=True)).reset_index(drop=True)
        df_means_sera = df_means_sera.append(df_sera.iloc[0, :].reset_index(drop=True)).reset_index(drop=True)
        df_vars_sera = df_vars_sera.append(df_sera.iloc[1, :].reset_index(drop=True)).reset_index(drop=True)

    # set the same column names for all dataframes and set the same index for all dataframes
    df_means_phi.columns = df_vars_phi.columns = df_phi.columns
    df_means_normal.columns = df_vars_normal.columns = df_normal.columns
    df_means_sera.columns = df_vars_sera.columns = df_sera.columns


    list_of_the_datasets = [cleanFileName(x) for x in list_of_the_datasets]
    df_means_phi.index = df_vars_phi.index = df_means_normal.index = df_vars_normal.index = df_means_sera.index = df_vars_sera.index = list_of_the_datasets

    # Save to Pickle files to $MEANS_AND_VARS
    createRequiredDirectories(path_MEANS_AND_VARS)

    # Normalize the dataframes
    df_means_phi = normalize_df(df_means_phi)
    df_vars_phi = normalize_df(df_vars_phi)
    df_means_normal = normalize_df(df_means_normal)
    df_vars_normal = normalize_df(df_vars_normal)
    df_means_sera = normalize_df(df_means_sera)
    df_vars_sera = normalize_df(df_vars_sera)

    df_means_phi.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_PHI_pkl))
    df_vars_phi.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_PHI_pkl))
    df_means_normal.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_NORMAL_pkl))
    df_vars_normal.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_NORMAL_pkl))
    df_means_sera.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_SERA_pkl))
    df_vars_sera.to_pickle("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_SERA_pkl))


    # save the dataframes to csv files
    df_means_phi.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_PHI_csv), index=False, header=True)
    df_vars_phi.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_PHI_csv), index=False, header=True)
    df_means_normal.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_NORMAL_csv), index=False, header=True)
    df_vars_normal.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_NORMAL_csv), index=False, header=True)
    df_means_sera.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_MEANS_SERA_csv), index=False, header=True)
    df_vars_sera.round(4).to_csv("{}/{}".format(path_MEANS_AND_VARS, DF_VARS_SERA_csv), index=False, header=True)


    print("Pickle and CSV files are saved successfully in {}!".format(path_MEANS_AND_VARS))


if __name__ == "__main__":
    main()
