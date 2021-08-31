# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 16:33:59 2021

@author: Raj Patel
"""

import pandas as pd
from tkinter import ttk
from tkinter import *
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def load_data_model():
    df_final_person = pd.read_csv('Final_person.csv', index_col=0)

    df_all = pd.read_csv('df_all.csv', index_col=0)

    infile = open('tfidf_vectorizer.pk', 'rb')
    tfidf_vectorizer = pickle.load(infile)
    infile.close()

    infile = open('tfidf_jobid.pk', 'rb')
    tfidf_jobid = pickle.load(infile)
    infile.close()
    return df_final_person, df_all, tfidf_vectorizer, tfidf_jobid

def select_user_from_df(df_final_person):
	user_id =getInputBoxValue()
	index = np.where(df_final_person['Applicant_id'] == user_id)[0][0]
	user_q = df_final_person.iloc[[index]]
	return user_q

# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = User_id.get()
	return userInput

def calculate_cosine_similarity(user_q):
	user_tfidf = tfidf_vectorizer.transform(user_q['text'])
	cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x),tfidf_jobid)
	output2 = list(cos_similarity_tfidf)
	return output2

def get_recommendation(top, df_all, scores, user_id):
	recommendation = pd.DataFrame(columns = ['ApplicantID', 'JobID',  'title', 'score'])
	count = 0
	for i in top:
		recommendation.at[count, 'ApplicantID'] = user_id
		recommendation.at[count, 'JobID'] = df_all['Job.ID'][i]
		recommendation.at[count, 'title'] = df_all['Title'][i]
		recommendation.at[count, 'score'] =  scores[count]
		count += 1
	return recommendation

# insert_values from the tree
def update_value():
    remove_entries()
    df = pd.read_csv("top10_recommendation.csv", index_col=0)
    for i in range(df.shape[0]):
        job_id = df.iloc[i][1]
        job_title = df.iloc[i][2]
        tree.insert("", 0, values=(job_id, job_title))


# clears the entry for next 10 recommendation
def remove_entries():
    X = tree.get_children()
    for item in X:
        tree.delete(item)


root = Tk()

# This is the section of code which creates the main window
# root.geometry('880x600')
width = 1080
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.configure(background='#F0F8FF')
root.title('Recommendation System')

# This is the section of code which creates the a label
Label(root, text='Enter the user id:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=50, y=59)

# This is the section of code which creates a text input box
User_id = Entry(root)
User_id.place(x=180, y=59)

# This is the section of code which creates a button
Button(root, text='Select the user', bg='#F0F8FF', font=('arial', 10, 'normal'), command=select_user_from_df).place(x=180, y=99)

TableMargin = Frame(root, width=600)
TableMargin.pack(side=RIGHT)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Job_id", "Job_details"), height=400, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Job_id', text="Job_id", anchor=W)
tree.heading('Job_details', text="Job_details", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=500)
tree.pack()

# ============================INITIALIZATION==============================
if __name__ == '__main__':
	df_final_person, df_all, tfidf_vectorizer, tfidf_jobid = load_data_model()
	root.mainloop()
	user_q = select_user_from_df(df_final_person)
	output2 = calculate_cosine_similarity(user_q)
	top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
	list_scores = [output2[i][0][0] for i in top]
	top10_recommendation = get_recommendation(top, df_all, list_scores, user_id=getInputBoxValue())
	top10_recommendation.to_csv("top10_recommendation.csv")
	update_value()


