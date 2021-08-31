
from tkinter import *
from subprocess import call


# this is a function to get the user input from the text input box
def getInputBoxValue():
    userInput = User_id.get()
    file = open("user_id.txt", 'w')
    file.write(userInput)
    file.close()
    root.destroy()
    call(["python", "Load_pk.py"])


root = Tk()

# This is the section of code which creates the main window
# root.geometry('880x600')
width = 450
height = 200
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
Button(root, text='Select the user', bg='#F0F8FF', font=('arial', 10, 'normal'), command=getInputBoxValue).place(x=180, y=99)


# ============================INITIALIZATION==============================
if __name__ == '__main__':
    root.mainloop()

