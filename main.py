import a_create_df_means_and_vars
import b_save_df_means_and_vars_in_CSV_files
import c_check_significancy
import d_winlosts
import e_find_rank_and_draw_cd_diagrams
import f_createLatexTables
import g_us_vs_os


def main():
    print("Starting the steps...")
    print(60 * "-")
    print("Step 1: Creating the dataframes of means and vars and saving them in pickle files...")
    a_create_df_means_and_vars.main()
    print(60 * "-")
    print("Step 2: Saving the dataframes of means and vars in CSV files...")
    b_save_df_means_and_vars_in_CSV_files.main()
    print(60 * "-")
    print("Step 3: Checking the significancy of the dataframes...")
    c_check_significancy.main()
    print(60 * "-")
    print("Step 4: Calculating the winlosts of the dataframes...")
    d_winlosts.main()
    print(60 * "-")
    print("Step 5: Finding the rank and drawing the CD diagrams...")
    e_find_rank_and_draw_cd_diagrams.main()
    print(60 * "-")
    print("Step 6: Creating the Latex tables...")
    f_createLatexTables.main()
    print(60*"-")
    print("Step 7: Creating US vs OS plots...")
    g_us_vs_os.main()
    print("All the steps are done successfully!")


if __name__ == "__main__":
    main()
