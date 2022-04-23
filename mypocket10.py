#!/bin/python3 mypocket7.py
#pyinstaller --hidden-import babel.numbers mypocket7.py -w -F
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar, DateEntry
import sys
import os
import re
import time
from datetime import datetime,date,timedelta
import csv
import webbrowser

def callback(): # open Ionut in browser 
    webbrowser.open_new("https://my-online.ro/programe-utile/")


azi = datetime.now()
db={} ###*** Working dict
fname='excsvfile.csv' ###*** CSV file stock

if os.path.isfile(fname):  ###*** create if not
    pass
else:
    with open('excsvfile.csv', 'w') as f:
        f.write('')
        
def nzdif(b): ###*** return days number
    azi=datetime.now()
    return (azi - b).days

def is_date(ds): ###*** check date format
    if re.match(r'\d{4}-\d{2}-\d{2}', ds):
        return True                                                                         
    return False

def read_from_file():###*** read file and push in db
    global db
    with open('excsvfile.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row != '':
                k, v = row[0],row[1:]
                db[k] = v
            else:
                db={}
    return db

read_from_file() ###*** Citeste fisierul

def write_to_file(): ###*** write to file when close
    with open('excsvfile.csv', 'w') as f:
        for k,v in db.items():
            f.write("%s,%s\n"%(str(k),','.join(v)))
    return f

def write_deleted(*args,**kargs): ###*** track deleted records
    with open('deletedcsvfile.csv', 'a') as fd:
        fd.write("%s,%s,%s\n"%(str(args),','.join(kargs),('stearsa in ',azi)))    
    return fd


###  add,change,delete,show_all,show_one,important_messages
    
def add_new_records(): ###*** add
    
    la=[]
    outputx.delete(0.0,END)
    
    if enterx1.get()=='' or enterx2.get()=='' or enterx3.get()=='':    
        messagebox.showerror('Completati toate campurile ......   ')
        return
    
    ka = enterx1.get()
    
    if ka in db:
        messagebox.showerror('Exista deja in baza...')
        enterx1.delete(0,END)
        enterx2.set('')
        enterx3.delete(0,END)
        search.insert(-1, 'Cauta')
        search.focus()
        return
    va = enterx2.get()
    dataa = enterx3.get()
    if nzdif(datetime.strptime(dataa,"%Y-%m-%d")) < 0:
        messagebox.showerror(' --> Data e din viitor???- incearca din nou...')
        return
    la.append(va)
    la.append(dataa)
    db[ka]=la

    list_all.delete(0,END)

    outputx.insert(END, 'OK am inregistrat -  '+ ka +' - '+ str(db[ka]))
    enterx1.delete(0,END)
    enterx2.set('')
    enterx3.delete(0,"end")
    search.focus()
    important_messages()
    show_all()
    return db
   
    
def change_a_value():###*** add event ins, fat sau avort   
    le=[]
    outputx.delete(0.0,END)
    if enterx1.get()=='' or enterx2.get()=='' or enterx3.get()=='':
        messagebox.showerror('Completati toate campurile........      ')
        return
    ke = enterx1.get()
    if ke not in db:
        messagebox.showerror('Nu exista in baza.......     ')
        return
    
    ve = enterx2.get()
    datae = enterx3.get()
    
    if len(datae)!=10:
        messagebox.showerror('  -->!! Ops format data incorect... ')
        return
    if nzdif(datetime.strptime(datae,"%Y-%m-%d")) < 0:
        messagebox.showerror('  -->Data e din viitor???- incearca din nou')
        return
    if nzdif(datetime.strptime(datae,"%Y-%m-%d")) > nzdif(datetime.strptime(db[ke][-1],"%Y-%m-%d")):
        messagebox.showerror('  -->Data e anterioara ultimei inregistrari??? - incearca din nou')
        return
    le.append(ve)
    le.append(datae)
    db[ke].extend(le)
    
    list_all.delete(0,END)    
    enterx1.delete(0,END)
    enterx2.set('')
    enterx3.delete(0,"end")
    outputx.insert(END, 'OK am inregistrat ')
    outputx.insert(END, (ke, le[-2],le[-1]))
    important_messages()
    show_all()
    return db
 

def delete_records(): ###*** delete
    
    outputx.delete(0.0,END)
    if enterx1.get()=='':
        messagebox.showerror('Completati crotalia...                ')
        return
    kd = enterx1.get()
    if kd not in db:
        enterx1.delete(0,END)
        messagebox.showerror('Nu exista in baza aceasta crotalie...       ')
        return
        
    if kd in db:
        res = messagebox.askokcancel( message="Sigur vreti sa stergeti, OK or Cancel")
        if res == 1:
            write_deleted(kd,db[kd])
            del db[kd]
            list_all.delete(0,END)
            enterx1.delete(0,END)
            outputx.insert(END, ('OK am sters ',kd))
            important_messages()
            show_all()
            
            return db
    

def show_all(): ###*** all list in show_all  
    list_all.delete(0,END)
    for k,v in sorted(db.items(),reverse=True):
        my_str=v[-1]
        idate=datetime.strptime(my_str,"%Y-%m-%d")
        msg = (" --> {} :  are {} zile de la {}".format(k,nzdif(idate),v[-2]))
        #{key:d[key] for key in sorted(d.keys())}
        if v[-2]=='insamintare':
            if nzdif(idate) in range(17,24):
                msg = (" --> {} are {} zile de la insamintare de urmarit".\
                       format(k,nzdif(idate)))
            elif nzdif(idate) in range(210,270) and 'fatare' in db[k]:
                msg = (" --> {} -intarcare(gestanta de {} zile)".format(k,nzdif(idate)))
            elif nzdif(idate) in range(270,280):
                msg = (" --> {} -mutata in boxa de fatare(gestanta de {} zile)".\
                       format(k,nzdif(idate)))
            elif nzdif(idate) in range(280,300):
                msg = (" -->  {} ar trebui sa fete(gestanta de {} zile)".\
                       format(k,nzdif(idate)))
            elif nzdif(idate)>=300:
                msg = (" -->!!!!! {} - Oops - {} - zile ?????".\
                       format(k,nzdif(idate)))
        if v[-2]=='fatare' or 'avort':
            if nzdif(idate)>60:
                msg = (" --> {} a depasit 60 zile de la {} si nu a intrat in calduri ({} zile)".\
                       format(k,v[-2],nzdif(idate)))        
        list_all.insert(0,'  --   '+k+'  =   '+ v[-2]+'   in   '+ v[-1])
    list_all.insert(0,'                                              ')   
    
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'avort'}))
                    + " avortate.")
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'fatare'}))
                    + " fatate.")
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'insamintare'}))
                    + " insamintate.")
    list_all.insert(0,'                                              ')
    list_all.insert(0,"     {} inregistrari. ".format(len(db)))
    
    


def show_one(): ###*** one or many(detail) from SEARCH
    temp_list=[]
    outputx.delete(0.0,END)
    if SEARCH.get() =='':    
        messagebox.showerror('Completati crotalia...         ')
        return
    ko = SEARCH.get()
    msg_1=''
    msg_2=''
    msg_3=''
    
    dbt=[]
    for i  in list(db.keys()):
        if ko in i:
            dbt.append(i)
    if len(dbt) == 0:
        msg_1 = ('Nu exista aceasta crotalie in baza. ')
        outputx.insert(END,msg_1+'\n')
        SEARCH.set("")
        return
    else:
        for elem in dbt:        
            my_str=db[elem][-1]
            idate=datetime.strptime(my_str,"%Y-%m-%d")
            msg_1 = " {} :  {} \n".format(elem,db[elem])
            if db[elem][-2] == 'insamintare':
                msg_2='- {} zile de la insamintare. Prognoza fatare : {} ' \
                   .format(nzdif(idate),
                           str(datetime.strptime(db[elem][-1],"%Y-%m-%d") + timedelta(284))[ :10])
            if 'fatare' or 'avort' in db[elem]:
                msg_2 = "- {} zile de la {}.".format(nzdif(idate), db[elem][-2])
                msg_3 = "- {} fatari. ".format(db[elem].count('fatare'))   
                  
            outputx.insert(END,msg_1)
            outputx.insert(END,msg_2+'\n')
            outputx.insert(END,msg_3+'\n'+'\n')
        
    enterx1.delete(0,END)
    SEARCH.set("")
    search.focus()
    
def important_messages(): ###*** Alerts
    list2.delete(0,END)
    for k, v in db.items():
        my_str=v[-1]
        idate=datetime.strptime(my_str,"%Y-%m-%d")
        if v[-2]=='insamintare':
            if nzdif(idate) in range(17,24):
                list2.insert(END,
                ''.join(" -  {} are {} zile de la insamintare -> de urmarit!".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(210,270) and 'fatare' in db[k]:
                list2.insert(END,
                ''.join(" -  {} intarcare(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(270,280):
                list2.insert(END,
                ''.join(" -  {} mutata in boxa de fatare(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(280,300):
                list2.insert(END,
                ''.join(" -  {} ar trebui sa fete(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate)>=300:
                list2.insert(END,
                ''.join(" -  {}  ? ? ?  -  {} zile de la insamintare ? ? ?".\
                        format(k,nzdif(idate))))
                
        if v[-2]=='fatare' or v[-2]=='avort':
            if nzdif(idate)>60:           
                list2.insert(END,
                ''.join(" -  {}  a depasit 60 zile de la {} si nu a intrat in calduri ( {} zile). "\
                        .format(k,v[-2],nzdif(idate))))
                
def quit_app(): ###*** Close and write
    write_to_file()
    sys.exit
    my_window.destroy()

def do_nothing():
    pass


#INITIALIZARE MENU TKINTER
my_window = tk.Tk()

my_menu = tk.Menu(my_window,background='#000099', foreground='white',
               activebackground='#004c99', activeforeground='white')
my_window.title("REPRO DB")
my_window.configure(bg='blue')
my_window.geometry('1255x600+100+50')
my_window.resizable(width=False,height=False)
my_menu.add_command(label=' --- Vetit --- ',                                              
                    command=do_nothing)
my_menu.add_command(label='                                                 \
                                                                            \
                            Inchide programul',command=quit_app)
my_menu.add_command(label='                                  \
                             Copyright ©'+str(azi)[ :4],command=do_nothing)
my_menu.add_command(label="https://my-online.ro/programe-utile/",                                              
                    command=callback)
my_window.config(menu=my_menu)


#####################################################################################
### 4 FRAME  SHOW ALL (Listbox)
frame_show_all = tk.Frame(my_window,bg='light blue')
SEARCH = StringVar()

# BUTTONS
buttonx1 = tk.Button(frame_show_all,text='Adauga inregistrare',
                     relief=RAISED,fg='green',bg='white',bd=4,font='none 12',
                     command=lambda:add_new_records())
buttonx1.grid(row = 2, column = 2,pady=15,padx=15)

buttonx2 = tk.Button(frame_show_all,text='Adauga eveniment ',
                     relief=RAISED,fg='green',bg='white',bd=4,font='none 12',
                     command=lambda:change_a_value())
buttonx2.grid(row = 3, column = 2,pady=15,padx=15)

buttonx3 = tk.Button(frame_show_all,text='Sterge inregistrare  ',
                     relief=RAISED,fg='green',bg='white',bd=4,font='none 12',
                     command=lambda:delete_records())
buttonx3.grid(row = 4, column = 2,pady=15,padx=15)

# LABELS
lblx1 = tk.Label(frame_show_all,text='1 : Nr. crotal(id, nume)',
                 width = 30,borderwidth=4,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W).grid(row=2,column=0,padx=4 , pady=4)

lblx2 = tk.Label(frame_show_all,text='2 : Alege evenimentul.',
                 width = 30,borderwidth=4,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W).grid(row=3,column=0,padx=4 , pady=4)

lblx3 = tk.Label(frame_show_all,text='3 : Data evenimentului',
                 width = 30,borderwidth=4,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W).grid(row=4,column=0,padx=4 , pady=4)

# ENTRIES
enterx1 = tk.Entry(frame_show_all, width = 30,
                   borderwidth = 3,font= ('Arial', 11,'bold'))
enterx1.grid(row = 2, column = 1, columnspan = 1, padx =4 , pady = 4)
enterx1.focus()

enterx2 = ttk.Combobox(frame_show_all,width = 28,
                       state="readonly",font= ('Arial', 11, 'bold'))
enterx2['values']=('','insamintare','fatare','avort')
enterx2.grid(row = 3,column=1)
enterx2.current()

enterx3 = DateEntry(frame_show_all,date_pattern='YYYY-mm-dd',
                    borderwidth=3,width = 13,state="readonly")
enterx3.delete(0,"end")
enterx3.grid(row = 4, column = 1, columnspan = 3, padx =4 , pady = 4,sticky=W)


search_label=tk.Label(frame_show_all,text='Cauta').grid(row=5,column=2,sticky=W)
search = tk.Entry(frame_show_all,width = 11,bd=5,font='none 12',relief=RAISED,
                 fg='green',bg='white',textvariable=SEARCH)
search.grid(row = 5, column = 2,pady=5,padx=5)
search.focus()
search.bind("<Return>",(lambda event: show_one()))# bind enter to search

# OUTPUT TEXT
outputx = scrolledtext.ScrolledText(frame_show_all,width=68,
                  height=7,font= ('Arial', 10, 'bold'),
                  wrap=WORD,background='white',fg='green')#
outputx.grid(row=5,column=0,columnspan=4,padx=4,sticky=W)#

# LISTBOX
list_all = Listbox(frame_show_all,height=15, width=75,font='none 11',bg='lightskyblue')
list_all.grid(row=6,column=0,pady=8,padx=4,columnspan=3,rowspan=8,sticky=W)

# Create scrollbar
scrollbar = Scrollbar(frame_show_all)
scrollbar.grid(row=6,column=2,rowspan=8,sticky='ns',pady=5)

list_all.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list_all.yview)

frame_show_all.pack(side=LEFT)

#################################################################################
###    FRAME IMPORTANT MESSAGES    ###
frame_important_messages = tk.Frame(my_window,bg='red')
label_important_messages = tk.Label(frame_important_messages,
                                    text = '  ALERTE  ',
                                    font='none  ').pack(pady=5)
list2 = Listbox(frame_important_messages,height=35, width=75,font='none 10')
list2.pack(side=LEFT,pady=10,padx=5)

# Create scrollbar2
scrollbar2 = Scrollbar(frame_important_messages,orient=VERTICAL,command=list2.yview)
scrollbar2.pack(side=RIGHT,fill='y')

list2.configure(yscrollcommand=scrollbar2.set)


frame_important_messages.pack()

        
important_messages()
show_all()


if nzdif(datetime.strptime('2022-11-30',"%Y-%m-%d"))>= 0:
    frame_show_all.destroy()
    frame_important_messages.destroy()
    
my_window.mainloop()
#pyinstaller --onefile --windowed --icon=icons8_spring.ico --hidden-import "babel.numbers" mypocket10.py
'''
commit fe2a77de19a4330f900f5330b0d0cfb84473c563 (HEAD -> master)
Author: Iancu Ioan <iancuioan897@yahoo.ro>
Date:   Sat Apr 23 22:41:29 2022 +0300

    added mypocket10.py'''

