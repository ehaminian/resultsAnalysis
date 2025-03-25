import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import arff


# set current directory to the path of the script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


title_y_size = 7
title_x_size = 7
green_blue = "#138874"
orange = "#d1560e"
pink = "#ec5077"
orange_alpha_02 = "#ff820033"
blue = "#2e86c1"


def get_plt_boxplot(values):
  plt.boxplot(values, vert=False, patch_artist=True, boxprops=dict(facecolor=orange))
  # plt.gcf().set_size_inches(8, 2.5)
  plt.title("", fontsize=title_y_size)
  plt.xlabel("Target value (y)", fontsize=title_x_size)
  plt.ylabel("Boxplot", fontsize=title_y_size)
  # move y label 1 cm to the left
  plt.gca().yaxis.set_label_coords(-0.1, 0.5)
  plt.setp(plt.gca().lines, color=blue)
  plt.setp(plt.gca().patches, color=pink)
  plt.yticks([])
  plt.xticks(fontsize=title_x_size)
  plt.gca().spines['bottom'].set_linewidth(0.5)
  plt.gca().spines['top'].set_linewidth(0.5)
  plt.gca().spines['right'].set_linewidth(0.5)
  plt.gca().spines['left'].set_linewidth(0.5)
  return plt

def get_plt_chebyshev(x,y):
  # plt.scatter(x, y, color=orange, s=1)
  plt.plot(x, y, color=orange, linewidth=1)
  # plt.gcf().set_size_inches(8, 2.5)
  plt.title("", fontsize=title_y_size)
  plt.ylabel("Chebyshev Probability", fontsize=title_y_size)
  plt.xlabel("", fontsize=title_x_size)
  plt.yticks(fontsize=title_y_size)
  plt.xticks([])
  plt.gca().spines['bottom'].set_linewidth(0.5)
  plt.gca().spines['top'].set_linewidth(0.5)
  plt.gca().spines['right'].set_linewidth(0.5)
  plt.gca().spines['left'].set_linewidth(0.5)
  return plt


# read the dataset
file_path = 'E:\\Rtest\\Datasets1\\2_FriedmanArtificialDomain.arff'
data, meta = arff.loadarff(file_path)
df_dataset = pd.DataFrame(data)



df_prob = pd.read_csv("C:\\Users\\Ehsan\\Desktop\\git\\eea1\\Results\\df_2_fried_cheby.csv")
df_prob = df_prob.sort_values(by="TrueValue")


fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 5))
fig.set_size_inches(4, 3)
plt.sca(axs[0])
plt = get_plt_chebyshev(df_prob["TrueValue"], df_prob["chevPropability"])
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.sca(axs[1])
plt = get_plt_boxplot(df_dataset["y"])
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.subplots_adjust(hspace=0.1)
plt.savefig("box_plot_fried.png", dpi=500, format="png",  bbox_inches='tight', pad_inches=0.1)