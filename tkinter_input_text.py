from tkinter import *
import tkinter as tk
root = tk.Tk()
root.geometry("500x150")
root.title('Player ID')

player_id = tk.StringVar(root)

label = Label(root, text='Input Player ID')
label.pack()

def getvalue():
    print(player_id.get())
    
e1 = Entry(root, textvariable=player_id, width=20, fg="blue", bd=3, selectbackground='violet').pack()
button1 = tk.Button(root, text='Save', fg='White', bg= 'dark green', height=1, width=10,command=getvalue).pack()
button2 = tk.Button(root, text='Quit', fg='White', bg= 'dark green', height=1, width=10,command=root.destroy).pack()

root.mainloop()