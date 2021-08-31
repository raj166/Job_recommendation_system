# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 16:33:59 2021

@author: Raj Patel
"""

from tkinter import ttk
from tkinter import *
import pandas as pd


# this is a function to get the user input from the text input box
def getInputBoxValue():
    userInput = User_id.get()
    return userInput


# this is the function called when the button is clicked
def Select_user():
    update_value()


# insert_values from the tree
def update_value():
    remove_entries()
    df = pd.read_csv("top10_recommendation.csv", index_col=0)
    for i in range(df.shape[0]):
        job_id = df.iloc[24-i][1]
        job_title = df.iloc[24-i][2]
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
with open ("user_id.txt", "r") as myfile:
    data = myfile.read().splitlines()
user_id = "".join(str(data[0]))
User_id.insert(0,str(user_id))
User_id.place(x=180, y=59)

with open ("user_details.txt", "r") as myfile:
    data = myfile.read().splitlines()
user_details = data[0]
Label(root, text = "User profile details: " + user_details, bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=50, y=150)
# This is the section of code which creates a button
Button(root, text='Select the user', bg='#F0F8FF', font=('arial', 10, 'normal'), command=Select_user).place(x=180, y=99)

TableMargin = Frame(root, width=700)
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
tree.column('#1', stretch=NO, minwidth=0, width=70)
tree.column('#2', stretch=NO, minwidth=0, width=500)
tree.pack()

# ============================INITIALIZATION==============================
if __name__ == '__main__':
    update_value()
    root.mainloop()
