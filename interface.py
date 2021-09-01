# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 16:33:59 2021

@author: Raj Patel
"""

import pandas as pd
from tkinter import ttk
import tkinter
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

#call all the method and integrate all of them 
def merge_all_functions():
        import pandas as pd
        import numpy as np
        df_final_person = pd.read_csv('Final_person.csv', index_col=0)
        df_all = pd.read_csv('df_all.csv', index_col=0)
        infile = open('tfidf_vectorizer.pk', 'rb')
        tfidf_vectorizer = pickle.load(infile)
        infile.close()
        infile_2 = open('tfidf_jobid.pk', 'rb')
        tfidf_jobid = pickle.load(infile_2)
        infile_2.close()
        user_id_dataset = int(User_id.get())
        index = np.where(df_final_person['Applicant_id'] == int(User_id.get()))[0][0]
        user_q = df_final_person.iloc[[index]]
        output2 = calculate_cosine_similarity(user_q,tfidf_vectorizer,tfidf_jobid)
        top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:20]
        list_scores = [output2[i][0][0] for i in top]
        top10_recommendation = get_recommendation(top, df_all, list_scores, user_id_dataset)
        update_value(top10_recommendation)
        tkinter.Label(root, text = "User profile details: \n" + str(user_q.iat[0,1]), bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=50, y=150)

# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = User_id.get()
	return userInput

#calculate cosine similarity
def calculate_cosine_similarity(user_q, tfidf_vectorizer, tfidf_jobid):
	user_tfidf = tfidf_vectorizer.transform(user_q['text'])
	cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x),tfidf_jobid)
	output2 = list(cos_similarity_tfidf)
	return output2

#get top 10 recommendation
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
def update_value(df):
    remove_entries()
    for i in range(df.shape[0]):
        job_id = df.iloc[i][1]
        job_title = df.iloc[i][2]
        tree.insert("", 0, values=(job_id, job_title))


# clears the entry for next 10 recommendation
def remove_entries():
    X = tree.get_children()
    for item in X:
        tree.delete(item)


root = tkinter.Tk()

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
tkinter.Label(root, text='Enter the user id:', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=50, y=59)

# This is the section of code which creates a text input box
User_id = tkinter.Entry(root)
User_id.place(x=180, y=59)

# This is the section of code which creates a button
tkinter.Button(root, text='Select the user', bg='#F0F8FF', font=('arial', 10, 'normal'), command=merge_all_functions).place(x=180, y=99)

TableMargin = tkinter.Frame(root, width=600)
TableMargin.pack(side=tkinter.RIGHT)
scrollbarx = tkinter.Scrollbar(TableMargin, orient=tkinter.HORIZONTAL)
scrollbary = tkinter.Scrollbar(TableMargin, orient=tkinter.VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Job_id", "Job_details"), height=400, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=tkinter.RIGHT, fill=tkinter.Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=tkinter.BOTTOM, fill=tkinter.X)
tree.heading('Job_id', text="Job_id", anchor=tkinter.W)
tree.heading('Job_details', text="Job_details", anchor=tkinter.W)
tree.column('#0', stretch=tkinter.NO, minwidth=0, width=0)
tree.column('#1', stretch=tkinter.NO, minwidth=0, width=200)
tree.column('#2', stretch=tkinter.NO, minwidth=0, width=500)
tree.pack()


# ============================INITIALIZATION==============================
if __name__ == '__main__':
	
	root.mainloop()


