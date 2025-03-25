import os
from consts import *
from pool_functions import *


def main():

    # load the dataframes from pickle files
    df_means_phi, \
        _, \
        df_means_normal, \
        _, \
        df_means_sera, \
        _ = load_means_vars(path_MEANS_AND_VARS, DF_MEANS_PHI_pkl, DF_VARS_PHI_pkl, DF_MEANS_NORMAL_pkl,
                                       DF_VARS_NORMAL_pkl, DF_MEANS_SERA_pkl, DF_VARS_SERA_pkl)



    # load significany dfs from pickle file
    sig_phi_df_under, \
    sig_phi_df_over, \
    sig_normal_df_under, \
    sig_normal_df_over, \
    sig_sera_df_under, \
    sig_sera_df_over = load_significance_dfs(path_SignificancyFiles,
                                               SIG_PHI_DF_UNDER,
                                               SIG_PHI_DF_OVER,
                                               SIG_NORMAL_DF_UNDER,
                                               SIG_NORMAL_DF_OVER,
                                               SIG_SERA_DF_UNDER,
                                               SIG_SERA_DF_OVER)




    # change column names
    df_means_phi.columns = COLUMN_NAMES
    df_means_normal.columns = COLUMN_NAMES
    df_means_sera.columns = COLUMN_NAMES


    # Create a new dataframe Under/Over by selecting only the COLUMN_NAMES_UNDER columns
    df_means_phi_Under = df_means_phi[COLUMN_NAMES_UNDER].copy()
    df_means_phi_Over = df_means_phi[COLUMN_NAMES_OVER].copy()
    df_means_normal_Under = df_means_normal[COLUMN_NAMES_UNDER].copy()
    df_means_normal_Over = df_means_normal[COLUMN_NAMES_OVER].copy()
    df_means_sera_Under = df_means_sera[COLUMN_NAMES_UNDER].copy()
    df_means_sera_Over = df_means_sera[COLUMN_NAMES_OVER].copy()

    # Create a new dataframe df_means_normal_Under/df_means_normal_Over by selecting only the COLUMN_NAMES_UNDER columns
    df_winLost_phi_Under = pd.DataFrame(index=df_means_phi_Under.index)
    df_winLost_phi_Over = pd.DataFrame(index=df_means_phi_Over.index)
    df_winLost_normal_Under = pd.DataFrame(index=df_means_normal_Under.index)
    df_winLost_normal_Over = pd.DataFrame(index=df_means_normal_Over.index)
    df_winLost_sera_Under = pd.DataFrame(index=df_means_sera_Under.index)
    df_winLost_sera_Over = pd.DataFrame(index=df_means_sera_Over.index)


    for i in range(0, df_means_phi_Under.shape[1], 2):
        column_name = "{}<{}".format(df_means_phi_Under.columns[i], df_means_phi_Under.columns[i + 1])
        df_winLost_phi_Under[column_name] = df_means_phi_Under.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)
        df_winLost_normal_Under[column_name] = df_means_normal_Under.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)
        df_winLost_sera_Under[column_name] = df_means_sera_Under.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)

        column_name = "{}>{}".format(df_means_phi_Under.columns[i], df_means_phi_Under.columns[i + 1])
        df_winLost_phi_Under[column_name] = df_means_phi_Under.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)
        df_winLost_normal_Under[column_name] = df_means_normal_Under.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)
        df_winLost_sera_Under[column_name] = df_means_sera_Under.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)

    for i in range(0, df_means_phi_Over.shape[1], 2):
        column_name = "{}<{}".format(df_means_phi_Over.columns[i], df_means_phi_Over.columns[i + 1])
        df_winLost_phi_Over[column_name] = df_means_phi_Over.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)
        df_winLost_normal_Over[column_name] = df_means_normal_Over.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)
        df_winLost_sera_Over[column_name] = df_means_sera_Over.apply(lambda row: 1 if (row[i] < row[i + 1]) else 0,axis=1)

        column_name = "{}>{}".format(df_means_phi_Over.columns[i], df_means_phi_Over.columns[i + 1])
        df_winLost_phi_Over[column_name] = df_means_phi_Over.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)
        df_winLost_normal_Over[column_name] = df_means_normal_Over.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)
        df_winLost_sera_Over[column_name] = df_means_sera_Over.apply(lambda row: 1 if (row[i] > row[i + 1]) else 0,axis=1)

    # Save to Pickle files to $MEANS_AND_VARS
    createRequiredDirectories(path_win_loss_tables)



    # Save to Pickle files
    df_winLost_phi_Under.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Under_pkl))
    df_winLost_phi_Over.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_phi_Over_pkl))
    df_winLost_normal_Under.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Under_pkl))
    df_winLost_normal_Over.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_normal_Over_pkl))
    df_winLost_sera_Under.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Under_pkl))
    df_winLost_sera_Over.to_pickle("{}/{}".format(path_win_loss_tables, DF_WINLOST_sera_Over_pkl))

    # replicate each column of the significance dataframes and insert it next to the original column
    # Iterate through the columns and concatenate the replicated columns

    # for the under dataframes
    replicated_sig_phi_df_Under = pd.DataFrame(index=sig_phi_df_under.index)
    replicated_sig_normal_df_Under = pd.DataFrame(index=sig_normal_df_under.index)
    replicated_sig_sera_df_Under = pd.DataFrame(index=sig_sera_df_under.index)
    for col in sig_phi_df_under.columns:
        replicated_sig_phi_df_Under = pd.concat([replicated_sig_phi_df_Under, sig_phi_df_under[col].copy()], axis=1)
        replicated_sig_phi_df_Under = pd.concat([replicated_sig_phi_df_Under, sig_phi_df_under[col].copy()], axis=1)
        replicated_sig_normal_df_Under = pd.concat([replicated_sig_normal_df_Under, sig_normal_df_under[col].copy()],axis=1)
        replicated_sig_normal_df_Under = pd.concat([replicated_sig_normal_df_Under, sig_normal_df_under[col].copy()],axis=1)
        replicated_sig_sera_df_Under = pd.concat([replicated_sig_sera_df_Under, sig_sera_df_under[col].copy()],axis=1)
        replicated_sig_sera_df_Under = pd.concat([replicated_sig_sera_df_Under, sig_sera_df_under[col].copy()],axis=1)


    # for the over dataframes
    replicated_sig_phi_df_Over = pd.DataFrame(index=sig_phi_df_over.index)
    replicated_sig_normal_df_Over = pd.DataFrame(index=sig_normal_df_over.index)
    replicated_sig_sera_df_Over = pd.DataFrame(index=sig_sera_df_over.index)
    for col in sig_phi_df_over.columns:
        replicated_sig_phi_df_Over = pd.concat([replicated_sig_phi_df_Over, sig_phi_df_over[col].copy()], axis=1)
        replicated_sig_phi_df_Over = pd.concat([replicated_sig_phi_df_Over, sig_phi_df_over[col].copy()], axis=1)
        replicated_sig_normal_df_Over = pd.concat([replicated_sig_normal_df_Over, sig_normal_df_over[col].copy()],axis=1)
        replicated_sig_normal_df_Over = pd.concat([replicated_sig_normal_df_Over, sig_normal_df_over[col].copy()],axis=1)
        replicated_sig_sera_df_Over = pd.concat([replicated_sig_sera_df_Over, sig_sera_df_over[col].copy()],axis=1)
        replicated_sig_sera_df_Over = pd.concat([replicated_sig_sera_df_Over, sig_sera_df_over[col].copy()],axis=1)

    # change column names
    replicated_sig_phi_df_Under.columns = df_winLost_phi_Under.columns
    replicated_sig_normal_df_Under.columns = df_winLost_normal_Under.columns
    replicated_sig_phi_df_Over.columns = df_winLost_phi_Over.columns
    replicated_sig_normal_df_Over.columns = df_winLost_normal_Over.columns
    replicated_sig_sera_df_Under.columns = df_winLost_sera_Under.columns
    replicated_sig_sera_df_Over.columns = df_winLost_sera_Over.columns

    # Multiply the win/lost dataframes with the replicated significance dataframes
    df_winLost_phi_sig_Under = df_winLost_phi_Under * replicated_sig_phi_df_Under
    df_winLost_normal_sig_Under = df_winLost_normal_Under * replicated_sig_normal_df_Under
    df_winLost_phi_sig_Over = df_winLost_phi_Over * replicated_sig_phi_df_Over
    df_winLost_normal_sig_Over = df_winLost_normal_Over * replicated_sig_normal_df_Over
    df_winLost_sera_sig_Under = df_winLost_sera_Under * replicated_sig_sera_df_Under
    df_winLost_sera_sig_Over = df_winLost_sera_Over * replicated_sig_sera_df_Over

    # prepare the dataframes PHI_UNDER for the final output
    DF_PHI_Under = pd.concat([df_winLost_phi_Under.sum(axis=0), df_winLost_phi_sig_Under.sum(axis=0)], axis=1)
    DF_PHI_Under.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_PHI_Under["Win/Lost (%)"] = DF_PHI_Under["Win/Lost"] / df_winLost_phi_Under.shape[0]
    DF_PHI_Under["Win/Lost (Significant) (%)"] = DF_PHI_Under["Win/Lost (Significant)"] / \
                                                 df_winLost_phi_sig_Under.shape[0]
    DF_PHI_Under["Win/Lost (%)"] = DF_PHI_Under["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Under["Win/Lost (Significant) (%)"] = DF_PHI_Under["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Under["Win/Lost (%)"] = DF_PHI_Under["Win/Lost (%)"].astype(str)
    DF_PHI_Under["Win/Lost (Significant) (%)"] = DF_PHI_Under["Win/Lost (Significant) (%)"].astype(str)

    # prepare the dataframes PHI_OVER for the final output
    DF_PHI_Over = pd.concat([df_winLost_phi_Over.sum(axis=0), df_winLost_phi_sig_Over.sum(axis=0)], axis=1)
    DF_PHI_Over.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_PHI_Over["Win/Lost (%)"] = DF_PHI_Over["Win/Lost"] / df_winLost_phi_Over.shape[0]
    DF_PHI_Over["Win/Lost (Significant) (%)"] = DF_PHI_Over["Win/Lost (Significant)"] / df_winLost_phi_sig_Over.shape[0]
    DF_PHI_Over["Win/Lost (%)"] = DF_PHI_Over["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Over["Win/Lost (Significant) (%)"] = DF_PHI_Over["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_PHI_Over["Win/Lost (%)"] = DF_PHI_Over["Win/Lost (%)"].astype(str)
    DF_PHI_Over["Win/Lost (Significant) (%)"] = DF_PHI_Over["Win/Lost (Significant) (%)"].astype(str)

    # prepare the dataframes NORMAL_UNDER for the final output
    DF_NORMAL_UNDER = pd.concat([df_winLost_normal_Under.sum(axis=0), df_winLost_normal_sig_Under.sum(axis=0)], axis=1)
    DF_NORMAL_UNDER.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_NORMAL_UNDER["Win/Lost (%)"] = DF_NORMAL_UNDER["Win/Lost"] / df_winLost_normal_Under.shape[0]
    DF_NORMAL_UNDER["Win/Lost (Significant) (%)"] = DF_NORMAL_UNDER["Win/Lost (Significant)"] / \
                                                    df_winLost_normal_sig_Under.shape[0]
    DF_NORMAL_UNDER["Win/Lost (%)"] = DF_NORMAL_UNDER["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_UNDER["Win/Lost (Significant) (%)"] = DF_NORMAL_UNDER["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_UNDER["Win/Lost (%)"] = DF_NORMAL_UNDER["Win/Lost (%)"].astype(str)
    DF_NORMAL_UNDER["Win/Lost (Significant) (%)"] = DF_NORMAL_UNDER["Win/Lost (Significant) (%)"].astype(str)

    # prepare the dataframes NORMAL_OVER for the final output
    DF_NORMAL_OVER = pd.concat([df_winLost_normal_Over.sum(axis=0), df_winLost_normal_sig_Over.sum(axis=0)], axis=1)
    DF_NORMAL_OVER.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_NORMAL_OVER["Win/Lost (%)"] = DF_NORMAL_OVER["Win/Lost"] / df_winLost_normal_Over.shape[0]
    DF_NORMAL_OVER["Win/Lost (Significant) (%)"] = DF_NORMAL_OVER["Win/Lost (Significant)"] / \
                                                   df_winLost_normal_sig_Over.shape[0]
    DF_NORMAL_OVER["Win/Lost (%)"] = DF_NORMAL_OVER["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_OVER["Win/Lost (Significant) (%)"] = DF_NORMAL_OVER["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_NORMAL_OVER["Win/Lost (%)"] = DF_NORMAL_OVER["Win/Lost (%)"].astype(str)
    DF_NORMAL_OVER["Win/Lost (Significant) (%)"] = DF_NORMAL_OVER["Win/Lost (Significant) (%)"].astype(str)


    # prepare the dataframes SERA_UNDER for the final output
    DF_SERA_UNDER = pd.concat([df_winLost_sera_Under.sum(axis=0), df_winLost_sera_sig_Under.sum(axis=0)], axis=1)
    DF_SERA_UNDER.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_SERA_UNDER["Win/Lost (%)"] = DF_SERA_UNDER["Win/Lost"] / df_winLost_sera_Under.shape[0]
    DF_SERA_UNDER["Win/Lost (Significant) (%)"] = DF_SERA_UNDER["Win/Lost (Significant)"] / \
                                                 df_winLost_sera_sig_Under.shape[0]
    DF_SERA_UNDER["Win/Lost (%)"] = DF_SERA_UNDER["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_UNDER["Win/Lost (Significant) (%)"] = DF_SERA_UNDER["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_UNDER["Win/Lost (%)"] = DF_SERA_UNDER["Win/Lost (%)"].astype(str)
    DF_SERA_UNDER["Win/Lost (Significant) (%)"] = DF_SERA_UNDER["Win/Lost (Significant) (%)"].astype(str)

    # prepare the dataframes SERA_OVER for the final output
    DF_SERA_OVER = pd.concat([df_winLost_sera_Over.sum(axis=0), df_winLost_sera_sig_Over.sum(axis=0)], axis=1)
    DF_SERA_OVER.columns = ["Win/Lost", "Win/Lost (Significant)"]
    DF_SERA_OVER["Win/Lost (%)"] = DF_SERA_OVER["Win/Lost"] / df_winLost_sera_Over.shape[0]
    DF_SERA_OVER["Win/Lost (Significant) (%)"] = DF_SERA_OVER["Win/Lost (Significant)"] / \
                                                 df_winLost_sera_sig_Over.shape[0]
    DF_SERA_OVER["Win/Lost (%)"] = DF_SERA_OVER["Win/Lost (%)"].apply(lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_OVER["Win/Lost (Significant) (%)"] = DF_SERA_OVER["Win/Lost (Significant) (%)"].apply(
        lambda x: "{:.2f}%".format(x * 100))
    DF_SERA_OVER["Win/Lost (%)"] = DF_SERA_OVER["Win/Lost (%)"].astype(str)
    DF_SERA_OVER["Win/Lost (Significant) (%)"] = DF_SERA_OVER["Win/Lost (Significant) (%)"].astype(str)

    # create the win/loss bar plots directory
    createRequiredDirectories(path_Win_loss_BARS)


    ################### Create plots Separately ###################
    # # create bar plots for the win/loss UNDER
    # create_win_loss_bars(DF_PHI_Under, path_Win_loss_BARS, f"{approach_name}US_phi.png", caption="")
    # create_win_loss_bars(DF_NORMAL_UNDER, path_Win_loss_BARS, f"{approach_name}US_normal.png", [-13, -5, -2, 2, 4],caption="")
    # create_win_loss_bars(DF_SERA_UNDER, path_Win_loss_BARS, f"{approach_name}US_sera.png", caption="")
    # # create bar plots for the win/loss OVER
    # create_win_loss_bars(DF_PHI_Over, path_Win_loss_BARS, f"{approach_name}OS_phi.png", caption="")
    # create_win_loss_bars(DF_NORMAL_OVER, path_Win_loss_BARS, f"{approach_name}OS_normal.png", [-13, -5, -2, 2, 4],
    #                      caption="")
    # create_win_loss_bars(DF_SERA_OVER, path_Win_loss_BARS, f"{approach_name}OS_sera.png", caption="")
    #
    # print(f"The win/loss bar plots have been created and saved in {path_Win_loss_BARS}.")


    ################### Create plots in one figure for UnderSampling method ###################
    barCaption = ""
    fig = plt.figure(figsize=(5, 1.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1],wspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])]
    handles, labels = create_win_loss_bars_subplot(DF_PHI_Under, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
    create_win_loss_bars_subplot(DF_SERA_UNDER, axes[1], [-4, -2, 2, 5, 10], barCaption, "SERA", False)
    create_win_loss_bars_subplot(DF_NORMAL_UNDER, axes[2], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
    plt.savefig(f"{path_Win_loss_BARS}/{approach_name}US_METRIC.png", dpi=600, bbox_inches="tight")

    ################### Create plots in one figure for OverSampling method ###################
    barCaption = ""
    fig = plt.figure(figsize=(5, 1.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1],wspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])]
    handles, labels = create_win_loss_bars_subplot(DF_PHI_Over, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
    create_win_loss_bars_subplot(DF_SERA_OVER, axes[1], [-4, -2, 2, 5, 10], barCaption, "SERA", False)
    create_win_loss_bars_subplot(DF_NORMAL_OVER, axes[2], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
    plt.savefig(f"{path_Win_loss_BARS}/{approach_name}OS_METRIC.png", dpi=600, bbox_inches="tight")

    print(f"The win/loss bar plots have been created and saved in {path_Win_loss_BARS}.")



if __name__ == "__main__":
    main()
