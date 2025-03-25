import os
from consts import *
from pool_functions import *

################### Create plots in one figure for UnderSampling method ###################

# DF_PHI_Under
########################################Sample of DF################################################################
#                                              Win/Lost Win/Lost (Significant) Win/Lost (%) Win/Lost (Significant) (%)
# PERCEPTRON_base<PERCEPTRON_cheby                     1                      1        7.69%                      7.69%
# PERCEPTRON_base>PERCEPTRON_cheby                    12                     10       92.31%                     76.92%
# FIMTDD_base<FIMTDD_cheby                             2                      2       15.38%                     15.38%
# FIMTDD_base>FIMTDD_cheby                            11                     11       84.62%                     84.62%
# TargetMean_base<TargetMean_cheby                     1                      1        7.69%                      7.69%
# TargetMean_base>TargetMean_cheby                    12                     12       92.31%                     92.31%
# AMRulesRegressor_base<AMRulesRegressor_cheby         1                      1        7.69%                      7.69%
# AMRulesRegressor_base>AMRulesRegressor_cheby        12                     12       92.31%                     92.31%
########################################################################################################################

# DF_NORMAL_UNDER
########################################Sample of DF################################################################
#                                              Win/Lost Win/Lost (Significant) Win/Lost (%) Win/Lost (Significant) (%)
# PERCEPTRON_base<PERCEPTRON_cheby                     1                      1        7.69%                      7.69%
# PERCEPTRON_base>PERCEPTRON_cheby                    12                     10       92.31%                     76.92%
# FIMTDD_base<FIMTDD_cheby                             2                      2       15.38%                     15.38%
# FIMTDD_base>FIMTDD_cheby                            11                     11       84.62%                     84.62%
# TargetMean_base<TargetMean_cheby                     1                      1        7.69%                      7.69%
# TargetMean_base>TargetMean_cheby                    12                     12       92.31%                     92.31%
# AMRulesRegressor_base<AMRulesRegressor_cheby         1                      1        7.69%                      7.69%
# AMRulesRegressor_base>AMRulesRegressor_cheby        12                     12       92.31%                     92.31%
########################################################################################################################
#RMSE\\phi

DF_PHI_Under = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [5, 5, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [8, 8, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [3, 3, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [10, 9, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [4, 4, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [10, 10, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [4, 4, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [9, 8, 61.54, 61.54]
})

DF_PHI_Over = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [3, 3, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [10, 10, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [3, 3, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [10, 10, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [3, 2, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [11, 11, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [3, 3, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [10, 10, 61.54, 61.54]
})


# /////////////////
DF_NORMAL_UNDER = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [5, 5, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [8, 8, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [4, 3, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [10, 10, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [4, 4, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [9, 9, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [5, 5, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [8, 8, 61.54, 61.54]
})


DF_NORMAL_Over = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [3, 3, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [10, 10, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [3, 3, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [11, 11, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [3, 2, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [9, 9, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [3, 3, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [10, 10, 61.54, 61.54]
})

column = ["Win/Lost", "Win/Lost (Significant)", "Win/Lost (%)", "Win/Lost (Significant) (%)"]
DF_PHI_Under = DF_PHI_Under.T
DF_NORMAL_UNDER = DF_NORMAL_UNDER.T
DF_PHI_Over = DF_PHI_Over.T
DF_NORMAL_Over = DF_NORMAL_Over.T

DF_PHI_Under = DF_PHI_Under.astype(int)
DF_NORMAL_UNDER = DF_NORMAL_UNDER.astype(int)
DF_PHI_Over = DF_PHI_Over.astype(int)
DF_NORMAL_Over = DF_NORMAL_Over.astype(int)


DF_PHI_Under.columns = DF_NORMAL_UNDER.columns = DF_PHI_Over.columns = DF_NORMAL_Over.columns = column


barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_Under, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
create_win_loss_bars_subplot(DF_NORMAL_UNDER, axes[1], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
plt.savefig(f"./{approach_name}US_BaseLine_METRIC_0.8.png", dpi=600, bbox_inches="tight")


################### Create plots in one figure for OverSampling method ###################
barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_Over, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
create_win_loss_bars_subplot(DF_NORMAL_Over, axes[1], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
plt.savefig(f"./{approach_name}OS_BaseLine_METRIC_0.8.png", dpi=600, bbox_inches="tight")

print(f"The win/loss bar plots have been created and saved!")

# ///////////////////////////////////////////////////// Phi = 0.0 /////////////////////////////////////////////////////

DF_PHI_Over = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [3, 3, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [10, 10, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [4, 3, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [9, 9, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [3, 3, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [10, 9, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [3, 3, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [10, 10, 61.54, 61.54]
})



DF_PHI_Under = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [5, 5, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [8, 8, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [4, 4, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [9, 9, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [5, 5, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [9, 8, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [5, 5, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [8, 8, 61.54, 61.54]
})

DF_NORMAL_Over = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [8, 8, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [5, 5, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [13, 12, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [0, 0, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [8, 6, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [5, 1, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [8, 8, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [5, 4, 61.54, 61.54]
})


DF_NORMAL_UNDER = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [12, 12, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [2, 2, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [12, 12, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [1, 1, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [12, 12, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [2, 1, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [12, 12, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [2, 2, 61.54, 61.54]
})

column = ["Win/Lost", "Win/Lost (Significant)", "Win/Lost (%)", "Win/Lost (Significant) (%)"]
DF_PHI_Under = DF_PHI_Under.T
DF_NORMAL_UNDER = DF_NORMAL_UNDER.T
DF_PHI_Over = DF_PHI_Over.T
DF_NORMAL_Over = DF_NORMAL_Over.T

DF_PHI_Under = DF_PHI_Under.astype(int)
DF_NORMAL_UNDER = DF_NORMAL_UNDER.astype(int)
DF_PHI_Over = DF_PHI_Over.astype(int)
DF_NORMAL_Over = DF_NORMAL_Over.astype(int)


DF_PHI_Under.columns = DF_NORMAL_UNDER.columns = DF_PHI_Over.columns = DF_NORMAL_Over.columns = column

barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_Under, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
create_win_loss_bars_subplot(DF_NORMAL_UNDER, axes[1], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
plt.savefig(f"./{approach_name}US_BaseLine_METRIC_0.0.png", dpi=600, bbox_inches="tight")


################### Create plots in one figure for OverSampling method ###################
barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_Over, axes[0], None, barCaption, "RMSE$\\phi$", True, add_legend=True)
create_win_loss_bars_subplot(DF_NORMAL_Over, axes[1], [-13, -5, -2, 2, 4], barCaption, "RMSE", False)

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
plt.savefig(f"./{approach_name}OS_BaseLine_METRIC_0.0.png", dpi=600, bbox_inches="tight")

print(f"The win/loss bar plots have been created and saved!")




# //////////////////////////////////// For LOW/High ////////////////////////////////////
DF_PHI_Under_LOW = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [1, 1, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [13, 13, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [2, 2, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [12, 11, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [2, 2, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [12, 12, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [1, 1, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [13, 13, 61.54, 61.54]
})

DF_PHI_Under_HIGH = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [0, 0, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [13, 13, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [2, 1, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [11, 10, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [3, 3, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [10, 10, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [2, 0, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [11, 11, 61.54, 61.54]
})

DF_PHI_OVER_LOW = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [1, 1, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [13, 13, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [1, 0, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [13, 13, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [1, 1, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [13, 11, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [1, 1, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [13, 12, 61.54, 61.54]
})

DF_PHI_OVER_HIGH = pd.DataFrame({
    "AMRulesRegressor_base<AMRulesRegressor_cheby": [0, 0, 38.46, 38.46],
    "AMRulesRegressor_base>AMRulesRegressor_cheby": [13, 13, 61.54, 61.54],
    "PERCEPTRON_base<PERCEPTRON_cheby": [1, 0, 25.00, 25.00],
    "PERCEPTRON_base>PERCEPTRON_cheby": [12, 12, 75.00, 75.00],
    "FIMTDD_base<FIMTDD_cheby": [0, 0, 30.77, 30.77],
    "FIMTDD_base>FIMTDD_cheby": [13, 13, 69.23, 69.23],
    "TargetMean_base<TargetMean_cheby": [0, 0, 30.77, 30.77],
    "TargetMean_base>TargetMean_cheby": [13, 13, 61.54, 61.54]
})

column = ["Win/Lost", "Win/Lost (Significant)", "Win/Lost (%)", "Win/Lost (Significant) (%)"]
DF_PHI_Under_LOW = DF_PHI_Under_LOW.T
DF_PHI_Under_HIGH = DF_PHI_Under_HIGH.T
DF_PHI_OVER_LOW = DF_PHI_OVER_LOW.T
DF_PHI_OVER_HIGH = DF_PHI_OVER_HIGH.T

DF_PHI_Under_LOW = DF_PHI_Under_LOW.astype(int)
DF_PHI_Under_HIGH = DF_PHI_Under_HIGH.astype(int)
DF_PHI_OVER_LOW = DF_PHI_OVER_LOW.astype(int)
DF_PHI_OVER_HIGH = DF_PHI_OVER_HIGH.astype(int)

DF_PHI_OVER_HIGH.columns = DF_PHI_OVER_LOW.columns = DF_PHI_Under_HIGH.columns = DF_PHI_Under_LOW.columns = column


barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_Under_LOW, axes[0], None, barCaption, "Low extreme rare cases "
                                                                                            "", True, add_legend=True)
create_win_loss_bars_subplot(DF_PHI_Under_HIGH, axes[1], [-13, -5, -2, 2, 4], barCaption, "High extreme rare cases ",
                             False)

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
plt.savefig(f"./{approach_name}US_BaseLine_RMSEPHI_LOW_HIGH_0.8.png", dpi=600, bbox_inches="tight")



barCaption = ""
fig = plt.figure(figsize=(5, 1.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1],wspace=0)
axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
handles, labels = create_win_loss_bars_subplot(DF_PHI_OVER_LOW, axes[0], None, barCaption, "Low extreme rare cases "
                                                                                            "", True, add_legend=True)
create_win_loss_bars_subplot(DF_PHI_OVER_HIGH, axes[1], [-13, -5, -2, 2, 4], barCaption, "High extreme rare cases ",
                             False)

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
plt.savefig(f"./{approach_name}OS_BaseLine_RMSEPHI_LOW_HIGH_0.8.png", dpi=600, bbox_inches="tight")