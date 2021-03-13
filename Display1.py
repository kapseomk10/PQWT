from tkinter import * 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector 
from tkinter import font

root = Tk()

my_font = font.Font(size=16,weight="bold")

def update():
    mydb = mysql.connector.connect(host="",user="", passwd="", database="", auth_plugin="mysql_native_password")

    cursor = mydb.cursor()

    for i in trv.get_children():
        trv.delete(i)
    for i in trv2.get_children():
        trv2.delete(i)

    query = "Select patientID, name, pwt from livetasks where status='waiting'"
    cursor.execute(query)
    rows = cursor.fetchall()

    query2 = "Select patientID, name, pst from livetasks where status='inservice'"
    cursor.execute(query2)
    rows2 = cursor.fetchall()
    
    for i in rows:
        trv.insert('','end',values=i)
    for i in rows2:
        trv2.insert('','end',values=i)
    root.after(1000,update)

wrapper1 = LabelFrame(root, text="Wait Queue", font=my_font)
wrapper2 = LabelFrame(root, text="Service Queue", font=my_font)

wrapper1.pack(fill="both",expand="yes",padx=10,pady=10)
wrapper2.pack(fill="both",expand="yes",padx=10,pady=10)
    
trv = ttk.Treeview(wrapper1, columns=(1,2,3), show="headings", height="10")
trv.pack()

style=ttk.Style()
style.configure("Treeview.Heading",font=(None,16,'bold'))
style.configure("Treeview",rowheight=35,font=(None,16,'bold'),background="#baf3fe")

trv.heading(1,text="Patient ID")
trv.heading(2,text="Name")
trv.heading(3,text="Wait Time")

trv.column(1,width=300,stretch=NO,anchor="center")
trv.column(2,width=300,stretch=NO,anchor="center")
trv.column(3,width=300,stretch=NO,anchor="center")

trv2 = ttk.Treeview(wrapper2, columns=(1,2,3), show="headings", height="10")
trv2.pack()

trv2.heading(1,text="Patient ID")
trv2.heading(2,text="Name")
trv2.heading(3,text="Service Time")

trv2.column(1,width=300,stretch=NO,anchor="center")
trv2.column(2,width=300,stretch=NO,anchor="center")
trv2.column(3,width=300,stretch=NO,anchor="center")

update()

root.title("Task Queue Status")
root.geometry("1000x1000")
root.mainloop()
