HIST="hist"
CHEBY="cheby"
approach_name=CHEBY # "hist" or "cheby"

LEARNERS = ["AMRules", "Perceptron", "FIMTDD", "TargetMean"]

COLUMN_NAMES = [
    "AMRules_baseline", f"AMRules_{approach_name}US", f"AMRules_{approach_name}OS",
    "Perceptron_baseline", f"Perceptron_{approach_name}US", f"Perceptron_{approach_name}OS",
    "FIMTDD_baseline", f"FIMTDD_{approach_name}US", f"FIMTDD_{approach_name}OS",
    "TargetMean_baseline", f"TargetMean_{approach_name}US", f"TargetMean_{approach_name}OS"
]

COLUMN_NAMES_UNDER = [
    "AMRules_baseline", f"AMRules_{approach_name}US",
    "Perceptron_baseline", f"Perceptron_{approach_name}US",
    "FIMTDD_baseline", f"FIMTDD_{approach_name}US",
    "TargetMean_baseline", f"TargetMean_{approach_name}US"
]

COLUMN_NAMES_OVER = [
    "AMRules_baseline", f"AMRules_{approach_name}OS",
    "Perceptron_baseline", f"Perceptron_{approach_name}OS",
    "FIMTDD_baseline", f"FIMTDD_{approach_name}OS",
    "TargetMean_baseline", f"TargetMean_{approach_name}OS"
]

COLUMN_NAMES_UN_vs_OS = [
    f"AMRules_{approach_name}US", f"AMRules_{approach_name}OS",
    f"Perceptron_{approach_name}US", f"Perceptron_{approach_name}OS",
    f"FIMTDD_{approach_name}US", f"FIMTDD_{approach_name}OS",
    f"TargetMean_{approach_name}US", f"TargetMean_{approach_name}OS"
]



phi = "\u03C6"
plusMinus = "\u00b1"
plusMinusLatex = " $\pm$ "
boldLatex = '\\bftab '
triRightLatex= "$\\triangleright$"
triLeftLatex= "$\\triangleleft$"
PHI_UN_OS = "phi_Un_OS"
NORMAL_UN_OS = "normal_Un_OS"
SERA_UN_OS = "sera_Un_OS"
_chebyshevNewResults = "../_chebyshevNewResults"
_HistogramNewResults = "../_HistogramNewResults"


# destination folder to save the pickle files Means and Vars
MEANS_AND_VARS = "./Means_and_Vars"
Synthetic_results = "./synthetic_results"

# Destination folder to save the pickle files SignificancyFiles
SignificancyFiles = "./SignificancyFiles"

# Kotlin Generated csv files in the Results folder
Results_OS_US = "./Results_OS_US"

# Destination for win/lost BARS
Win_loss_BARS = "./win_loss_BARS"

# Destination for win/lost tables
Win_loss_tables = "./win_loss_tables"

# Destination to save latex tables
Latex_tables_folder = "./latexTables"
latex_tables_folder_springer = "./springerLatexTables"

DF_WINLOST_phi_Under_pkl = "df_winLost_phi_Under.pkl"
DF_WINLOST_phi_Over_pkl = "df_winLost_phi_Over.pkl"
DF_WINLOST_normal_Under_pkl = "df_winLost_normal_Under.pkl"
DF_WINLOST_normal_Over_pkl = "df_winLost_normal_Over.pkl"
DF_WINLOST_sera_Under_pkl = "df_winLost_sera_Under.pkl"
DF_WINLOST_sera_Over_pkl = "df_winLost_sera_Over.pkl"
DF_WINLOST_phi_Under_vs_Over_pkl = "df_winLost_phi_Under_vs_Over.pkl"
DF_WINLOST_normal_Under_vs_Over_pkl = "df_winLost_normal_Under_vs_Over.pkl"
DF_WINLOST_sera_Under_vs_Over_pkl = "df_winLost_sera_Under_vs_Over.pkl"
DF_MEANS_PHI_Un_OS_pkl = "df_means_phi_Un_OS.pkl"
DF_VARS_PHI_Un_OS_pkl = "df_vars_phi_Un_OS.pkl"
DF_MEANS_NORMAL_Un_OS_pkl = "df_means_normal_Un_OS.pkl"
DF_VARS_NORMAL_Un_OS_pkl = "df_vars_normal_Un_OS.pkl"
DF_MEANS_SERA_Un_OS_pkl = "df_means_sera_Un_OS.pkl"
DF_VARS_SERA_Un_OS_pkl = "df_vars_sera_Un_OS.pkl"


RANKE_TABLE = "./Rank_table"

# Destination for CD diagrams
CD_disagrams = "./CD_disagrams"

# pickled means/vars files to save the dataframes
DF_MEANS_PHI_pkl = "df_means_phi.pkl"
DF_MEANS_NORMAL_pkl = "df_means_normal.pkl"
DF_VARS_PHI_pkl = "df_vars_phi.pkl"
DF_VARS_NORMAL_pkl = "df_vars_normal.pkl"
DF_MEANS_SERA_pkl = "df_means_sera.pkl"
DF_VARS_SERA_pkl = "df_vars_sera.pkl"

DF_MEANS_PHI_pkl_CHEBY_HIST_UNDER = "df_means_phi_CHEBY_HIST_UNDER.pkl"
DF_MEANS_NORMAL_pkl_CHEBY_HIST_UNDER = "df_means_normal_CHEBY_HIST_UNDER.pkl"
DF_MEANS_SERA_pkl_CHEBY_HIST_UNDER = "df_means_sera_CHEBY_HIST_UNDER.pkl"
DF_VARS_PHI_pkl_CHEBY_HIST_UNDER = "df_vars_phi_CHEBY_HIST_UNDER.pkl"
DF_VARS_NORMAL_pkl_CHEBY_HIST_UNDER = "df_vars_normal_CHEBY_HIST_UNDER.pkl"
DF_VARS_SERA_pkl_CHEBY_HIST_UNDER = "df_vars_sera_CHEBY_HIST_UNDER.pkl"
DF_MEANS_PHI_pkl_CHEBY_HIST_OVER = "df_means_phi_CHEBY_HIST_OVER.pkl"
DF_MEANS_NORMAL_pkl_CHEBY_HIST_OVER = "df_means_normal_CHEBY_HIST_OVER.pkl"
DF_MEANS_SERA_pkl_CHEBY_HIST_OVER = "df_means_sera_CHEBY_HIST_OVER.pkl"
DF_VARS_PHI_pkl_CHEBY_HIST_OVER = "df_vars_phi_CHEBY_HIST_OVER.pkl"
DF_VARS_NORMAL_pkl_CHEBY_HIST_OVER = "df_vars_normal_CHEBY_HIST_OVER.pkl"
DF_VARS_SERA_pkl_CHEBY_HIST_OVER = "df_vars_sera_CHEBY_HIST_OVER.pkl"


UNDER="Under"
OVER="Over"
RMSEPHI="RMSE_{\phi}"
RMSE="RMSE"
SERA="SERA"

# csv files to save the dataframes
DF_MEANS_PHI_csv = "df_means_phi.csv"
DF_MEANS_NORMAL_csv = "df_means_normal.csv"
DF_VARS_PHI_csv = "df_vars_phi.csv"
DF_VARS_NORMAL_csv = "df_vars_normal.csv"
DF_MEANS_SERA_csv = "df_means_sera.csv"
DF_VARS_SERA_csv = "df_vars_sera.csv"

# signifcancy dataframes
SIG_PHI_DF_UNDER = "sig_phi_df_Under.pkl"
SIG_PHI_DF_OVER = "sig_phi_df_Over.pkl"
SIG_NORMAL_DF_UNDER = "sig_normal_df_Under.pkl"
SIG_NORMAL_DF_OVER = "sig_normal_df_Over.pkl"
SIG_SERA_DF_UNDER = "sig_sera_df_Under.pkl"
SIG_SERA_DF_OVER = "sig_sera_df_Over.pkl"
SIG_PHI_DF_UNDER_VS_OVER = "sig_phi_df_Under_vs_Over.pkl"
SIG_NORMAL_DF_UNDER_VS_OVER = "sig_normal_df_Under_vs_Over.pkl"
SIG_SERA_DF_UNDER_VS_OVER = "sig_sera_df_Under_vs_Over.pkl"

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

path_to_Results_OS_US = f"{_HistogramNewResults}{Results_OS_US[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{Results_OS_US[1:]}"
path_MEANS_AND_VARS = f"{_HistogramNewResults}{MEANS_AND_VARS[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{MEANS_AND_VARS[1:]}"
path_win_loss_tables = f"{_HistogramNewResults}{Win_loss_tables[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{Win_loss_tables[1:]}"
path_SignificancyFiles = f"{_HistogramNewResults}{SignificancyFiles[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{SignificancyFiles[1:]}"
path_Latex_tables_folder = f"{_HistogramNewResults}{Latex_tables_folder[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{Latex_tables_folder[1:]}"
path_Win_loss_BARS = f"{_HistogramNewResults}{Win_loss_BARS[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{Win_loss_BARS[1:]}"
path_CD_disagrams = f"{_HistogramNewResults}{CD_disagrams[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{CD_disagrams[1:]}"
path_RANK_TABLE = f"{_HistogramNewResults}{RANKE_TABLE[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{RANKE_TABLE[1:]}"
path_Latex_tables_folder_springer = f"{_HistogramNewResults}{latex_tables_folder_springer[1:]}" if approach_name==HIST else f"{_chebyshevNewResults}{latex_tables_folder_springer[1:]}"
