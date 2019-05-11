"""
Author: Mohit
Status: Development
Date: 15/04/2019
"""
import numpy as np
import os
import pandas as pd


class Table:
    """Table process the html table and handles them in pandas.
    """
    def __init__(self, html_str):
        self.df = pd.read_html(html_str)[0]
    
    def process(self, file_path=''):
        """Process the table dataframe and saves 4 csv.
        """
        try:
            # processing the order no. column
            self.df['Order No.'] = self.df['Order No.'].str.replace("opens in new window ", '')

            # Marking where we need to break the dataframe.
            self.df['break'] = ~self.df['Sr No'].str.isnumeric()
            self.df['break'] = self.df['break'].astype('int')

            break_list = list(self.df[self.df['break'] ==1].index)
            self.df.drop('break', axis=1, inplace=True)

            dfs = list()
            df_name = list()
            start = 0

            for i in range(0, len(break_list)):
                start = break_list[i]
                if break_list[i] == break_list[-1]:
                    end = len(self.df.index)+1
                else:
                    end = break_list[i+1]
                curr_df = self.df.iloc[start+1: end, :]
                dfs.append(curr_df)
                df_name.append(self.df.iloc[break_list[i],0])
                df_name[i] = df_name[i].replace(',', '')
                df_name[i].replace(' ', '_')
                curr_df.to_csv(os.path.join(file_path, df_name[i] + '.csv'), index=False)
                print(df_name[i] + ' saved.')
                
        except Exception as ex:
            print("Table dataframe not formed properly.")
            print(ex)
