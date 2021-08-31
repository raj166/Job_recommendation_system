# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 14:26:55 2021

@author: Raj Patel
"""

import pickle
import numpy as np
import pandas as pd
import warnings
from sklearn.metrics.pairwise import cosine_similarity
from subprocess import call
warnings.filterwarnings("ignore")


df_final_person = pd.read_csv('Final_person.csv', index_col=0)
df_final_person.head()

df_all = pd.read_csv('df_all.csv', index_col=0)

infile = open('tfidf_vectorizer.pk', 'rb')
tfidf_vectorizer = pickle.load(infile)
infile.close()

infile = open('tfidf_jobid.pk', 'rb')
tfidf_jobid = pickle.load(infile)
infile.close()


def select_user(user_id):
    index = np.where(df_final_person['Applicant_id'] == user_id)[0][0]
    user_q = df_final_person.iloc[[index]]
    return user_q


def calculate_cosine_similarity(user_q):
    user_tfidf = tfidf_vectorizer.transform(user_q['text'])
    cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x), tfidf_jobid)
    output2 = list(cos_similarity_tfidf)
    return output2


def get_recommendation(top, df_all, scores, user_id):
    recommendation = pd.DataFrame(columns=['ApplicantID', 'JobID', 'title', 'score'])
    count = 0
    for i in top:
        recommendation.at[count, 'ApplicantID'] = user_id
        recommendation.at[count, 'JobID'] = df_all['Job.ID'][i]
        recommendation.at[count, 'title'] = df_all['Title'][i]
        recommendation.at[count, 'score'] = scores[count]
        count += 1
    return recommendation




with open("user_id.txt", "r") as myfile:
    data = myfile.read().splitlines()
user_id = data[0]
print("User_id: ", user_id)
user_q = select_user(int(user_id))
file = open("user_details.txt", 'w')
file.write(str(user_q.iat[0,1]))
file.close()
print("calculating the cosine similarity")
output2 = calculate_cosine_similarity(user_q)
print("Creating a list of top 20 recommendation for user with user_id: ", user_id)
top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:25]
list_scores = [output2[i][0][0] for i in top]
top10_recommendation = get_recommendation(top, df_all, list_scores, 326)
top10_recommendation.to_csv("top10_recommendation.csv")
call(["python", "simple_gui.py"])
