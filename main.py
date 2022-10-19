import pandas as pd
import numpy as np

us = pd.read_csv('data/Users.csv')
bk = pd.read_csv('data/Books.csv', low_memory=False)
rt = pd.read_csv('data/Ratings.csv')

flag = 0
while flag == 0:
    tl = input("Enter the name of the book:   ").lower()
    bk['lower'] = bk['Book-Title'].str.lower()
    contains = bk[bk['lower'].str.contains(tl) == True]
    DFtoChose = contains['Book-Title'].drop_duplicates().reset_index(drop=True)
    if DFtoChose.empty:
        print('Sorry, no such book was founded')
        flag = 0
    else:
        flag = 1
        print(DFtoChose)
        while flag == 1:
            numb = int(input("Enter the number of the most appropriate book:   "))
            if numb <= max(DFtoChose.index):
                flag = 2
                CorrectTitle = str(DFtoChose.iloc[numb])
                df_merged = bk.merge(rt)
                same_users = df_merged[(df_merged['Book-Title'] == CorrectTitle) & (df_merged['Book-Rating'] > 7)]
                users_id = same_users[['User-ID', 'lower']]
                users_choice = users_id.merge(rt)
                same_books_isbn = users_choice.loc[users_choice['Book-Rating'] > 7]
                merged_bk = same_books_isbn.merge(bk, on="ISBN")
                rec = pd.unique(merged_bk.loc[merged_bk['Book-Title'] != CorrectTitle, 'Book-Title'])
                if np.any(rec):
                    print('Your recommendations:   ', rec)
                else:
                    print("Sorry, recommendation was not found.")
            else:
                flag = 1
                print('You entered the wrong number. Please, try again!  ')
