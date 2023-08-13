##!/bin/python3 repro1.2.py
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar, DateEntry
import sys, os, re
from datetime import datetime,date,timedelta
import csv
import webbrowser
#-----------------------------------
import tempfile

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
    b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
#-------------------------------------------------
mypath = os.getcwd()

def callback_fisa(x): # open fisa
    #webbrowser.open_new(mypath+'\\'+"Alerts.txt")
    webbrowser.open_new(mypath+'\\'+x)
def fisadealerte():# content fisa 
    name= "Alerts"
    with open(mypath+'\\'+ name + ".txt", "w") as f:
        f.write(str(azi)[ :10] +' \n'
                '     Fisa de alerte\n'
                '   _______________________________\n'
                ' \n' + '\n'.join(list2.get(0, 'end')))
    callback_fisa(name+".txt")  

def efectiv_total():# content fisa
    name= "Listing"
    with open(mypath+'\\'+ name + ".txt", "w") as f:
        f.write(str(azi)[ :10] +' \n'
                '     Listing\n'
                '   _______________________________\n'
                ' \n' + '\n')
        for k, v in db.items():
            f.write(str(k)+' : '+' '.join(v)+' \n')
    callback_fisa(name+".txt") 

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

def age(b): ### nzdif(datetime.strptime(mydate,"%Y-%m-%d"))
    azi=datetime.now()
    return (str(round((azi - b).days / 31))+ ' luni, ')

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

read_from_file() ###*** read file

def write_to_file(): ###*** write to file when close
    with open('excsvfile.csv', 'w') as f:
        for k,v in db.items():
            f.write("%s,%s\n"%(str(k),','.join(v)))
    return f

def write_deleted(*args,**kargs): ###*** track deleted records
    with open('deletedcsvfile.csv', 'a') as fd:
        fd.write("%s,%s,%s\n"%(str(args),','.join(kargs),
            ('stearsa in ',azi)))    
    return fd


###  add,change,delete,show_all,show_one,important_messages
def calculate_age(born):
    age = (datetime.datetime.now()-datetime.datetime(born)).days
    print(age)
#calculate_age(datetime.datetime(1967, 10, 1))
    
def add_new_records(): ###*** add interface
    renunta()# clear label, entry and buttons if exists
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    lblx1.place(x=10,y=50)
    lblx1A.place(x=10,y=75)
    lblx2.place(x=10,y=100)
    lblx3.place(x=10,y=125)
    enterx1.place(x=200,y=50)
    enterx1.focus()
    enterx1A.place(x=200,y=75)
    enterx2.place(x=200,y=100)
    enterx2.current()
    enterx3.place(x=200,y=125)
    save_add_btn.place(x=120, y=150)
    renunta_btn.place(x=280,y=150)
    
def process_add():
    la=[] # list for event and date
    if enterx1.get()=='' or enterx1A.get()=='' or enterx2.get()=='' or \
            enterx3.get()=='':    
        messagebox.showerror('Completati toate campurile ......   ')
        return    
    ka = enterx1.get()  # key(id) for  dict
    if ka in db:
        messagebox.showerror('Exista deja in baza...')
        enterx1.delete(0,END)
        enterx1A.delete(0,END)
        enterx2.set('')
        enterx3.delete(0,END)
        #search.insert(-1, 'Cauta')
        search.focus()
        return
    datanasterii = enterx1A.get()
    if nzdif(datetime.strptime(datanasterii,"%Y-%m-%d")) < 0:
        messagebox.showerror(' --> Data e din viitor???- incearca din nou...')
        enterx1A.delete(0,END)
        return
    elif 0 < nzdif(datetime.strptime(datanasterii,"%Y-%m-%d")) < 360:
        messagebox.showerror(' --> E cam tinara???- incearca din nou...')
        enterx1A.delete(0,END)
        return
    va = enterx2.get() # event
    dataa = enterx3.get() # date
    if nzdif(datetime.strptime(dataa,"%Y-%m-%d")) < 0:
        messagebox.showerror(' --> Data e din viitor???- incearca din nou...')
        enterx3.delete(0,END)
        return
    la.append('Data nasterii')
    la.append(datanasterii)# append datanasterii
    la.append(va) # append event
    la.append(dataa) # append date
    db[ka]=la # insert in dict

    list_all.delete(0,END) # clear list_all
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    outputx.insert(END, 'OK am inregistrat -  '+ ka +' - '+ str(db[ka]))
    enterx1.delete(0,END)
    enterx1A.delete(0,"end")
    enterx2.set('')
    enterx3.delete(0,"end")
    search.focus()
    outputx.config(state='disabled')
    important_messages() # populate important_messages
    show_all() # insert list_all
    lblx1.place_forget()
    lblx1A.place_forget()
    lblx2.place_forget()
    lblx3.place_forget()
    enterx1.place_forget()
    enterx1A.place_forget()
    enterx2.place_forget()
    enterx3.place_forget()
    save_add_btn.place_forget()
    renunta_btn.place_forget()
    return db
   
    
def change_a_value():###*** add event ins, fat sau avort interface
    renunta() # clear label, entry and buttons if exists
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    lblx1.place(x=10,y=50)
    lblx2.place(x=10,y=80)
    lblx3.place(x=10,y=110)
    enterx1.place(x=200,y=50)
    enterx1.focus()
    enterx2.place(x=200,y=80)
    enterx2.current()
    enterx3.place(x=200,y=110)
    save_process_change_btn.place(x=120, y=150)
    renunta_btn.place(x=280,y=150)


def process_change_a_value():
    le=[]
    if enterx1.get()=='' or enterx2.get()=='' or enterx3.get()=='':
        messagebox.showerror('Completati toate campurile........      ')
        return
    ke = enterx1.get()
    if ke not in db:
        messagebox.showerror('Nu exista in baza.......     ')
        enterx1.delete(0,END)
        enterx2.set('')
        enterx3.delete(0,"end")
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
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    outputx.insert(END, 'OK am inregistrat ')
    outputx.insert(END, (ke, le[-2],le[-1]))
    outputx.config(state='disabled')
    important_messages()
    show_all()
    lblx1.place_forget()
    lblx2.place_forget()
    lblx3.place_forget()
    enterx1.place_forget()
    enterx2.place_forget()
    enterx3.place_forget()
    save_process_change_btn.place_forget()
    renunta_btn.place_forget()
    return db
 

def delete_records(): ###*** delete interface
    renunta() # clear label, entry and buttons if exists
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    lblx1.place(x=10,y=50)
    enterx1.place(x=200,y=50)
    save_delete_btn.place(x=120, y=150)
    renunta_btn.place(x=280,y=150)


def process_delete():    
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
            outputx.delete(0.0,END)
            write_deleted(kd,db[kd])
            del db[kd]
            list_all.delete(0,END)
            enterx1.delete(0,END)
            outputx.config(state='normal')
            outputx.delete(0.0,END)
            outputx.insert(END, ('OK am sters ', kd))
            outputx.config(state='disabled')
            important_messages()
            show_all()
            lblx1.place_forget()
            enterx1.place_forget()
            save_delete_btn.place_forget()
            renunta_btn.place_forget()
            return db
        
def renunta(): # clear label, entry and buttons if exists
    lblx1.place_forget()
    lblx1A.place_forget()
    lblx2.place_forget()
    lblx3.place_forget()
    enterx1.place_forget()
    enterx1A.place_forget()
    enterx2.place_forget()
    enterx3.place_forget()
    save_add_btn.place_forget()
    save_process_change_btn.place_forget()
    save_delete_btn.place_forget()
    renunta_btn.place_forget()

def show_all(): ###*** all list in show_all  
    list_all.delete(0,END)
    for k,v in sorted(db.items(),reverse=True):
        my_str=v[-1]
        idate=datetime.strptime(my_str,"%Y-%m-%d")
        msg = (" --> {} :  are {} zile de la {}".format(k,nzdif(idate),v[-2]))
        #{key:d[key] for key in sorted(d.keys())}
        #list_all.insert(0, msg) 
        list_all.insert(0,'  --   '+k+'  =   ' +
                age(datetime.strptime(v[1],"%Y-%m-%d"))+' ' +
                str(v.count('fatare'))+' fatari. ')#v[-2]+'   in   '+ v[-1])
    list_all.insert(0,'                                              ')   
    
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'avort'}))
                    + " avortate.")
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'fatare'}))
                    + " fatate.")
    list_all.insert(0, "  - " + str(len({k:db[k] for k in db if db[k][-2] == 'insamintare'}))
                    + " insamintate.")
    list_all.insert(0,'                                              ')
    list_all.insert(0,"     {} inregistrari. ".format(len(db)))
    
    


def show_one(): ###*** one or many(detail) from SEARCH in outputx
    temp_list=[]
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    if SEARCH.get() =='':    
        messagebox.showerror('Completati crotalia...         ')
        return
    ko = SEARCH.get().strip()
    msg_1=''
    msg_2=''
    msg_3=''
    
    dbt=[] # list for key values
    for i in list(db.keys()):
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
            outputx.insert(END,msg_3+' '+
                    age(datetime.strptime(db[elem][1],"%Y-%m-%d")).replace(',','')+'\n')
    outputx.config(state='disabled')    
    SEARCH.set("")
    search.focus()
    
def important_messages(): ###*** Alerts
    list2.delete(0,END)
    l=[] # temporary list for alerts
    for k, v in db.items():
        my_str=v[-1]
        idate=datetime.strptime(my_str,"%Y-%m-%d")
        if v[-2]=='insamintare':
            if nzdif(idate) in range(17,24):
                #list2.insert(END,
                #''.join(" -  {} are {} zile de la insamintare -> de urmarit!".\
                #        format(k,nzdif(idate))))
                l.append(''.join(" -  {} are {} zile de la insamintare -> de urmarit!".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(210,270) and 'fatare' in db[k]:
                #list2.insert(END,
                #''.join(" -  {} intarcare(gestanta de {} zile).".\
                #        format(k,nzdif(idate))))
                l.append(''.join(" - {}   intarcare(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(270,280):
                #list2.insert(END,
                #''.join(" -  {} mutata in boxa de fatare(gestanta de {} zile).".\
                #        format(k,nzdif(idate))))
                l.append(''.join(" -  {}   mutata in boxa de fatare(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate) in range(280,300):
                #list2.insert(END,
                #''.join(" -  {} ar trebui sa fete(gestanta de {} zile).".\
                #        format(k,nzdif(idate))))
                l.append(''.join(" -  {}   ar trebui sa fete(gestanta de {} zile).".\
                        format(k,nzdif(idate))))
                
            elif nzdif(idate)>=300:
                #list2.insert(END,
                #''.join(" -  {}  ? ? ?  -  {} zile de la insamintare ? ? ?".\
                #        format(k,nzdif(idate))))
                l.append(''.join(" -  {}  ? ? ?  -  {} zile de la insamintare ? ? ?".\
                        format(k,nzdif(idate))))
                
        if v[-2]=='fatare' or v[-2]=='avort':
            if nzdif(idate)>60:           
                #list2.insert(END,
                #''.join(" -  {}  a depasit 60 zile de la {} si nu a intrat in calduri ( {} zile). "\
                #        .format(k,v[-2],nzdif(idate))))
                l.append(''.join(" -  {}  a depasit 60 zile de la {} si nu a intrat in calduri ( {} zile). "\
                        .format(k,v[-2],nzdif(idate))))
    def myfunc(e):
        return e[20: ]
    x=sorted(l, key=myfunc)
    for el in x:
        list2.insert(END,el)
    
    count_msg_lbl.config(text=str(len(list2.get(0,'end')))+' notificari')

def copy_paste_select_from_output():
    if outputx.selection_get() != '':
        #print('outputx.selection_get() = ',outputx.selection_get())
        enterx1.delete(0, END)
        enterx1.insert(END, outputx.selection_get())
        
def clear_entries():
    outputx.config(state='normal')
    outputx.delete(0.0,END)
    enterx1.delete(0, 'end')
    enterx2.set('')
    enterx3.delete(0, 'end')
    outputx.config(state='disabled')

                
def quit_app(): ###*** Close and write
    write_to_file()
    sys.exit
    my_window.destroy()

def do_nothing():
    pass


#INITIALIZARE MENU TKINTER
my_window = tk.Tk()

my_window.title("REPRO DB")
my_window.iconbitmap(ICON_PATH)
my_window.configure(bg='blue')
my_window.geometry('1155x600+100+50')
#my_window.iconphoto(False, PhotoImage(file='favicon.png'))
#my_window.resizable(width=False,height=False)



#####################################################################################
### 4 FRAME  SHOW ALL  left side
frame_show_all = tk.Frame(my_window)#,bg='light blue')
frame_show_all.pack(side=LEFT,expand=True,fill='both')
SEARCH = StringVar()

# BUTTONS
buttonx1 = tk.Button(frame_show_all,text='Adauga inregistrare',cursor='hand2',
                     relief=RAISED,fg='green',bg='white',bd=2,font='none 10',
                     command=lambda:add_new_records())
buttonx1.place(x=10, y=10)


buttonx2 = tk.Button(frame_show_all,text='Adauga eveniment ',cursor='hand2',
                     relief=RAISED,fg='green',bg='white',bd=2,font='none 10',
                     command=lambda:change_a_value())
buttonx2.place(x=150, y=10)


buttonx3 = tk.Button(frame_show_all,text='Sterge inregistrare  ',cursor='hand2',
                     relief=RAISED,fg='green',bg='white',bd=2,font='none 10',
                     command=lambda:delete_records())
buttonx3.place(x=290, y=10)

save_add_btn= tk.Button(frame_show_all,text='Salveaza inregistrarea ',
                    cursor='hand2',
                    relief=RAISED,fg='white',bg='darkgreen',bd=2,font='none 10',
                    command=lambda:process_add())
#save_add_btn.place(x=120, y=150)
save_process_change_btn= tk.Button(frame_show_all,text='Salveaza evenimentul ',
                    cursor='hand2',
                    relief=RAISED,fg='white',bg='darkgreen',bd=2,font='none 10',
                    command=lambda:process_change_a_value())
#save_process_change_btn.place(x=120, y=150)
save_delete_btn= tk.Button(frame_show_all,text='Valideaza stergerea ',
                    cursor='hand2',
                    relief=RAISED,fg='white',bg='darkgreen',bd=2,font='none 10',
                    command=lambda:process_delete())
#save_delete_btn.place(x=120, y=150)
renunta_btn=Button(frame_show_all,text='Renunta ',
                    cursor='hand2',
                    relief=RAISED,fg='white',bg='darkgreen',bd=2,font='none 10',
                    command=lambda:renunta())
#renunta_btn.place(x=180.y=150)

# LABELS
lblx1 = tk.Label(frame_show_all,text='Nr. crotal(id, nume)',
                 width = 18,borderwidth=1,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W)
#lblx1.place(x=10,y=50)

lblx1A = tk.Label(frame_show_all,text='Data nasterii',
                 width = 18,borderwidth=1,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W)
#lblx1.place(x=10,y=50)

lblx2 = tk.Label(frame_show_all,text='Alege evenimentul.',
                 width = 18,borderwidth=1,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W)
#lblx2.place(x=10,y=80)

lblx3 = tk.Label(frame_show_all,text='Data evenimentului',
                 width = 18,borderwidth=1,font= ('Arial', 10, 'bold'),
                 relief=RAISED,anchor=W)
#lblx3.place(x=10,y=110)

# ENTRIES
enterx1 = tk.Entry(frame_show_all, width = 22,
                   borderwidth = 1,font= ('Arial', 11,'bold'))
#enterx1.place(x=200,y=50)
#enterx1.focus()

enterx1A = DateEntry(frame_show_all,date_pattern='YYYY-mm-dd',
                    borderwidth=1,width = 14,state="readonly")

enterx2 = ttk.Combobox(frame_show_all,width = 20,
                       state="readonly",font= ('Arial', 11, 'bold'))
enterx2['values']=('','insamintare','fatare','avort')
#enterx2.place(x=200,y=80)
#enterx2.current()


enterx3 = DateEntry(frame_show_all,date_pattern='YYYY-mm-dd',
                    borderwidth=1,width = 14,state="readonly")
#enterx3.delete(0,"end")
#enterx3.place(x=200,y=110)


clear_btn = Button(frame_show_all, text='Clear', font='none 10 bold',
                   cursor='hand2',width = 10,command=clear_entries)
clear_btn.place(x=500, y=45)



search_label=tk.Label(frame_show_all,text='Cauta crotalie   ')
search_label.place(x=480,y=159)
search = tk.Entry(frame_show_all,width = 15,font='none 12',#,bd=5,relief=RAISED,
                 fg='green',bg='white',textvariable=SEARCH)
search.place(x=445,y=180)#y=205)
search.focus()
search.bind("<Return>",(lambda event: show_one()))# bind enter to search

print_all_btn = Button(frame_show_all, text='Listeaza tot efectivul', font='none 10',
                   cursor='hand2',width = 16,command=efectiv_total)
print_all_btn.place(x=445, y=270)


# OUTPUT TEXT
outputx = scrolledtext.ScrolledText(frame_show_all,width=58,
                  height=8,font= ('Arial', 10, 'bold'), cursor='arrow',
                  wrap=WORD,background='white')#
outputx.place(x=10, y=180)
outputx.bind("<Return>",(lambda event: copy_paste_select_from_output()))


# LISTBOX
list_all = Listbox(frame_show_all,height=14, width=70,
                   font='none 11',bg='lightskyblue')
list_all.place(x=10,y=320)
scrollbar = Scrollbar(frame_show_all)
scrollbar.place(x=556,y=320, height=255)#(x=556,y=320, height=255)
list_all.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list_all.yview)



#################################################################################
###    IMPORTANT MESSAGES   right side ###

label_important_messages = tk.Label(frame_show_all,
        text = '  Notificari  ',font='none 14 ',fg='red')
label_important_messages.place(x=600, y=12)

count_msg_lbl = tk.Label(frame_show_all,text='',
        font='none 8',fg='brown')
count_msg_lbl.place(x=700, y=18)

print_notificari_button = Button(frame_show_all,command=fisadealerte,
            text='Listeaza notificarile', cursor='hand2')
print_notificari_button.place(x=870,y=10)

close_button = Button(frame_show_all,command=quit_app,bg='darkgreen',fg='white',
            text='Inchide programul ', cursor='hand2')
close_button.place(x=1010,y=10)


list2 = Listbox(frame_show_all,height=31,
                fg='brown',width=73,font='none 10')
list2.place(x=610,y=40)
scrollbar2 = Scrollbar(frame_show_all,
                       orient=VERTICAL,command=list2.yview)
scrollbar2.place(x=1120,y=40,height=531)
list2.configure(yscrollcommand=scrollbar2.set)

copyright_label=Label(frame_show_all,font='none 6 ',
        text='Copyright ©'+str(azi)[ :4] +'    itvet@yahoo.com ')
copyright_label.place(x=880,y=580)
           
        
important_messages()
show_all()
    
    
my_window.mainloop()

#pyinstaller --onefile --windowed --icon=icons8_spring.ico --hidden-import "babel.numbers" repro1.2.py
'''







   









