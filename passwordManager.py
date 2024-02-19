from tkinter import *
from tkinter import messagebox
import random
from tkinter import ttk
import sqlite3
import csv
#import pandas as pd
#from openpyxl import Workbook
from  datetime import  date
from pass_tips import passwordtips
from tkinter import filedialog
from cryptography.fernet import Fernet
import string
import secrets 


global admin_name_enter
  

root=Tk()
root.geometry("1150x700")
root.title("PASSWORD GENERATOR")
root.iconbitmap("icon_password.ico")
global rows
global admin_enter
global admin_password
admin_enter=""
admin_password=""

#MENU

def my_command():
    quit_program=messagebox.askyesno("QUIT","Do you want to quit ? (y/n)")
    if quit_program==True:
        root.destroy
    else:
        pass
    
    

my_menu=Menu(root)
root.config(menu=my_menu)

file_menu=Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="QUIT", command=my_command)


# TREE VIEW STYLE
style=ttk.Style()
style.theme_use("alt")
style.configure("root",
                  background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="silver"
                )
style.map('Treeview',
          background=[('selected', 'green')])
style.map('race_box',
          background=[('selected', 'blue')])


#TREE VIEWS
tree=ttk.Treeview(root)
tree.place(x=10, y=260)
tree["columns"]=("one","two", "three", "four", "five", "six", "seven")
tree.column('#0', width=0)
tree.column("one", width=150) #site name
tree.column("two", width=150) #user name 
tree.column("three", width=200) #email
tree.column("four", width=150) #password
tree.column("five", width=150) #Player No
tree.column("six", width=90) #pass created date
tree.column("seven", width=50) #pass strength 


tree.heading("one",text="SITE NAME")
tree.heading("two",text="USER NAME")
tree.heading("three",text= "EMAIL")
tree.heading("four",text="PASSWORD")
tree.heading("five", text="CREATED DATE ")
tree.heading("six", text="STRENGTH")
tree.heading("seven", text="ID")

tree.tag_configure('encrypted',background='red')
tree.tag_configure('decrypted',background='white')

scrollbar_tree=Scrollbar(root)
scrollbar_tree.pack(side=RIGHT, fill=Y)
scrollbar_tree.config(command=tree.yview)



#CHARACTER LISTS
raw_list="abcdefghjklmnoqprstuwxz1234567890!+%&/()=?_£#$½\|@<>{[]}"
upper_list=raw_list[:23].upper()
main_list=raw_list+upper_list
lower_list=['a', 'b', 'c', 'd', 'e', 'f', 'g' , 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'q', 'p', 'r', 's', 't', 'u', 'w', 'x', 'z']
special_char_list=[ '!', '+' ,'%' , '&' , '/' , '(' , ')',  '=', '?', '_',  ' £' , ' # ', '$', '½', 'a', '|', '@', '<', '>']
numeric_list=[ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]


#GLOBAL SHOW RECORDS
global enter_record
enter_record=["Null", "Null","Null","Null"]
global My_Pass
My_Pass=""
global entry_create_password


#CREATE DATABASE AND INIT address, user, email, password
conn=sqlite3.connect("sample_1.db")
c=conn.cursor()
table1="""CREATE TABLE IF NOT EXISTS drecords(adres text, kullanici_adi text , kullanici_email text, parola text, created_date text, strength)"""
c.execute(table1)
conn.commit()
conn.close()



#PASS_CREATE FUNCTION
def create_password():
    pass_len=int(entry_password_length.get())
    
        
    Fpassword=""
    temp_list=[]
    counter=0
    
    game=True
    while counter<pass_len:
         a=random.choice(main_list) #need global?
         if a not in temp_list:
            temp_list.append(a)
            counter+=1
           
    My_Pass="".join(temp_list)
    entry_create_password.delete(0, END)
    entry_create_password.insert(0,My_Pass)
    


#SHOW RECORDS

def show_records():
    global admin_name_enter
    global admin_password
    global admin_enter
    global admin_password
    if admin_enter=="test" and admin_password=="test":
        

    #open database
        conn=sqlite3.connect("sample_1.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM drecords")
        rows=c.fetchall()
    
    #put into treeview
        
        for i in tree.get_children():
            tree.delete(i)

        for row in rows:
            #print(row)
            tree.insert("","end", text=row[0], values=row)

        conn.commit()
        conn.close()
        
    else:
        messagebox.showwarning("Admin Input", "You need to enter password")
        
#ENCRYPT RECORDS
global encrypted_values_list       
def encrypt_records():
    #load_key 
    
    #open database
    try:
        global encrypted_list
        encrypted_list=[]
        string_value_list=[]        
        #record_id=id_entry.get()
        today=date.today()
        d1=today.strftime("%d/%m/%Y")
        
        global f
        global key
        

        #select tree item
        selected_item=tree.selection()[0] #or this selected_item=tree.selection()

        
        row=tree.item(selected_item)        
        values=row["values"]
        values_1=[]
        plain_bytes=[]
        site_name=values[0]
        record_id=values[6]
        print (values[0])

        for x in values:
            plain_bytes.append(str(x).encode()) #byte conversion

        for i in plain_bytes:
            encrypted_list.append(f.encrypt(i))

        #from byte list to string list
        for b in encrypted_list:
            string_value=b.decode('utf-8')
            string_value_list.append(string_value)
           

        #UPDATE DATABASE WITH ENCRYPTED DATA
        conn=sqlite3.connect("sample_1.db")
        c=conn.cursor()

        c.execute(
            'UPDATE drecords SET adres=?, kullanici_adi=?, kullanici_email=?, parola=?,created_date=?,strength=? WHERE oid=?',
            (site_name,string_value_list[1], string_value_list[2],string_value_list[3],d1,
             string_value_list[5],int(record_id))
             )
        conn.commit()
        conn.close()

        show_records()

        
        
    except Exception as e:
        messagebox.showwarning("KEY ERROR", e)

#DECRYPT RECORDS

def decrypt_records():
    global key
    global f
    decrypted_list=[]
    data_bytes_list=[]
    record_id=id_entry.get() #can changed by value treeview?
    today=date.today()
    d1=today.strftime("%d/%m/%Y")

   
    #this program gets  alternative: get values from treeview
    selected_item=tree.selection()
    row=tree.item(selected_item)
    values=row["values"]
    print(values[0])
    site_name=values[0]
    

    new_values=[values[1],values[2],values[3],values[5]] #omitted values[0]
    #print(new_values)
    


    for value in new_values:
        value_bytes=value.encode()
        decrypted_data_bytes=f.decrypt(value_bytes)
        decrypted_data_str=decrypted_data_bytes.decode()
        decrypted_list.append(decrypted_data_str)

    #print(decrypted_list)

    show_password_window=Toplevel(root)
    show_password_window.title("SHOW DECRYPTED PASSWORD")
    show_password_window.geometry("460x220")
    show_password_window.config(bg="#ADD8E6")
    
    info_text=Text(show_password_window,width=50, height=5,borderwidth=3,wrap=WORD,spacing3=5,font=("Bahnschrift",11))
    info_text.place(x=15,y=15)
    text=f"""SITE NAME:{site_name}\nUSER NAME:{decrypted_list[0]}\nEMAIL:{decrypted_list[1]}\nPASSWORD:{decrypted_list[2]}\nCREATED DATE:{d1}"""
    
    info_text.insert(END,text)
    info_text.config(state="disabled")

    show_password_window_button=Button(show_password_window,text="Close Window",command=show_password_window.destroy)
    show_password_window_button.place(x=170,y=180)
    
    show_password_window.mainloop()

   
    
#SUBMIT RECORDS

def submit_records():
    if admin_enter=="test" and admin_password=="test":
        
        today=date.today()
        d1=today.strftime("%d/%m/%Y")
        check_pass=str(len(entry_create_password.get()))
    
        #print(check_pass)
        #print (entry_site_name.get()+"\t"+entry_user_name.get()+"\t"+entry_email.get()+"\t"+entry_create_password.get()+"\t"+d1+"\t"+check_pass)
    #open database to enter data
        conn=sqlite3.connect("sample_1.db")
        c=conn.cursor()
        c.execute("""
    INSERT INTO drecords(adres, kullanici_adi, kullanici_email, parola, created_date,strength )
    VALUES(?, ?, ?, ?,?,?)
    """,(entry_site_name.get(), entry_user_name.get(), entry_email.get(), entry_create_password.get(), d1, check_pass))

        conn.commit()
        conn.close()
        #print(len(entry_create_password.get()))

    else:
        messagebox.showwarning("NOT CONNECTED", "ADMIN NAME OR PASSWORD IS WRONG")
    entry_site_name.delete("0",END)
    entry_user_name.delete("0",END)
    entry_email.delete("0",END)
    entry_create_password.delete("0",END)
    

 #HIDE RECORDS
def hide_records():
     for i in tree.get_children():
        tree.delete(i)
 

#SAVE CSV

def save_csv():
    
      
    with open("new.csv", "w", newline='') as myfile:
        cswriter=csv.writer(myfile, delimiter= '\t')
        for row_id in tree.get_children():
            row=tree.item(row_id)['values']
            print('save row:', row)
            cswriter.writerow(row)
            

#DELETE RECORD
def delete_record():
    global admin_enter
    global admin_password

    if admin_enter=="test" and admin_password=="test":
        
        delete_player_message=messagebox.askyesno("DELETE RECORD", f" do you want to delete record no {id_entry.get()}")
        if delete_player_message==True:
        
            conn=sqlite3.connect("sample_1.db")
            c=conn.cursor()
            c.execute("DELETE FROM drecords WHERE oid="+id_entry.get())
            conn.commit()
            conn.close()
        
        for i in tree.get_children():
            tree.delete(i)
        conn=sqlite3.connect("sample_1.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM drecords")
        rows=c.fetchall()
        for row in rows:
            tree.insert("","end", text="user", values=row)

        conn.commit
        conn.close()
        
    else:
        messagebox.showwarning("Error", "Password or Admin Name Wrong")
    
    
 

 #UPDATE RECORD

def edit_record():

    if admin_enter=="test" and admin_password=="test":

        entry_site_name.delete(0,END)
        entry_user_name.delete(0,END)
        entry_email.delete(0,END)
        entry_create_password.delete(0,END)
        conn=sqlite3.connect("sample_1.db")
        c=conn.cursor()
        record_id=id_entry.get()

    #need check if record_id is not null 
        #print (record_id)
        try:
        
            c.execute("SELECT * FROM drecords  WHERE oid= " + record_id)
            records=c.fetchall()
            for record in records:
                #print(record[0])
                entry_site_name.insert(0,record[0])
                entry_user_name.insert(0,record[1])
                entry_email.insert(0,record[2])
        #entry_password_length.insert(0,record[5])
                entry_create_password.insert(0,record[3])
        
            conn.commit()
            conn.close()
        except:
            record_id=""
    else:
        messagebox.showwarning("Connection Error","Password or Admin name wrong")
        
    
    
def update_record():

    

    if admin_enter=="test" and admin_password=="test":
    
        today=date.today()
        d1=today.strftime("%d/%m/%Y")
        check_pass=str(len(entry_create_password.get()))
    #adres, kullanici_adi, kullanici_email, parola, created_date,strength
        record_id=id_entry.get()
        update_warning=messagebox.askyesno("UPDATE RECORD", f"Are you sure  record ID  {record_id} should be updated?")
    
        if update_warning==True:
            conn=sqlite3.connect("sample_1.db")
            c=conn.cursor()
        #record_id=id_entry.get()

           

            c.execute(
           'UPDATE drecords SET adres=?, kullanici_adi=?, kullanici_email=?, parola=?, created_date=?, strength=? WHERE oid=?',
           (entry_site_name.get(), entry_user_name.get(), entry_email.get(),entry_create_password.get(),d1,check_pass, int(record_id))
           )

            conn.commit()
            conn.close()
        else:
            messagebox.showwarning("Connection Error","Password or Admin name wrong")
      
#TIPPS WINDOW
def tipps(): #notes: here opened a child window and made text widget state disabled, and added scrollbar
    tip_window=Toplevel(root)
    tip_window.title("TIPS FOR GOOD PASSWORD")
    tip_window.geometry("730x650")

    info_text=Text(tip_window, wrap=WORD, borderwidth=5, spacing3=5)
    info_text.place(x=15,y=15)
    info_text.insert(END, passwordtips)
    info_text.config(state="disabled")
    
    scrollbar=ttk.Scrollbar(tip_window, orient="vertical", command=info_text.yview)
    info_text.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
                            
    button_exit=Button(tip_window, text="CLOSE THIS WINDOW", command=tip_window.destroy)
    button_exit.place(x=300,y=570)
  
    tip_window.mainloop()
    


#QUIT PROGRAM

def quit_program():
    quit_message=messagebox.askyesno("QUIT PROGRAM", "Are you sure to Quit ? (y/n) ?")
    if quit_message==True:
        root.destroy()



global security_level
global level_meter


#SECURITY CHECK

def security_check():
    global security_level
    global level_meter
    
    global sl
    global lm
    check_special_chars=[]
    check_uppercase=[]
    check_lowercase=[]
    check_numbers=[]
    char_counter=0
    number_counter=0
    upper_counter=0
    lower_counter=0
    security_level=["red", "orange","green", "#53b800"]
    level_meter=["very weak", "weak", "medium", "strong", "very strong"]
    sl=security_level[0]
    lm=level_meter[0]
    
    
    
    
    global entry_create_password
    password_to_check=entry_create_password.get()

    
    if len(password_to_check)<5:
        sl=security_level[0]
        lm=level_meter[0]
        
        
    if len(password_to_check)>5 and len(password_to_check)<7:
        sl=security_level[0]
        lm=level_meter[1]
        
    if len(password_to_check)>7 and len(password_to_check)<10:
        sl=security_level[2]
        lm=level_meter[2]

    if len(password_to_check)>10 and len(password_to_check)<12:
        sl=security_level[3]
        lm=level_meter[3]

    if len(password_to_check)>12:
        sl=security_level[3]
        lm=level_meter[4]
       
    
    
       #ANALYZE PASS chars, nums, upper, 
    for i in special_char_list:
        if i in password_to_check:
            print(i)
            check_special_chars.append(i)
            
    for j in numeric_list:
        if j in password_to_check:
            check_numbers.append(j)

    for t in upper_list:
        if t in password_to_check:
            check_uppercase.append(t)

    for z in lower_list:
        if z in password_to_check:
            check_lowercase.append(z)
            
    print(f"in the password exists  {len(check_special_chars)} and these : {check_special_chars}")
    print(password_to_check)

    
    label_length.config(text=f"Created Password has {len(password_to_check)}   characters") 
    
    
    label_strength_level.config(text=lm,fg=sl)
    label_special_chars.config(text=f"Created Password has {len(check_special_chars)} special characters")

    label_numbers.config(text=f"Created Password has {len(check_numbers)} numbers")

    label_uppercase.config(text=f"Created Password has {len(check_uppercase)} uppercase characters")
    label_lowercase.config(text=f"Created Password has {len(check_lowercase)} lowercase characters")
    
def clear_security_display():
    label_length.config(text="")
    label_strength_level.config(text="")
    label_special_chars.config(text="")
    label_numbers.config(text="")
    label_uppercase.config(text="")
    label_lowercase.config(text="")
    
    return

def admin_check():
    global entry_admin_name
    global entry_admin_password
    global admin_enter
    global admin_password
    admin_enter=entry_admin_name.get()
    admin_password=entry_admin_password.get()
    entry_admin_name.delete(0,END)
    entry_admin_password.delete(0, END)
    if admin_enter=="test" and admin_password=="test":
        connection_status.config(text="Login Successfull", fg="blue")
    else:
        connection_status.config(text="Login Failed", fg="red")
    

global key
global f
def load_key():
    global admin_enter
    global admin_password
    global key
    global f
  

    if admin_enter=="test" and admin_password=="test":
        root.filename=filedialog.askopenfilename(initialdir="/python", title="SELECT A KEY FILE", filetypes=(("key files", "*.key"), ("all files","*.*")))
        key_file=open(root.filename,"rb")
        key=key_file.read()
        f=Fernet(key)
        #print(key)
        key_status_label.config(text="KEY LOADED", fg="blue")

    else:
        messagebox.showwarning("ATTENTION", "Wrong Password or Admin Name")
        
def alt_create_pass(value): #pw_length

    

    global alt_site_new_password_entry
    letters=string.ascii_letters
    digits=string.digits
    special_chars=string.punctuation

    alt_site_new_password_entry.delete(0,END)

                                       

    alphabet=letters+digits+special_chars

    pwd=''

    pw_strong=False

    while not pw_strong:

        pwd='' # password 
        for i in range(value):
            pwd+=''.join(secrets.choice(alphabet))

        if (any(char in special_chars for char in pwd) and
            sum(char in digits for char in pwd) >=2):
            pw_strong=True
    print(pwd)
    alt_site_new_password_entry.insert(0,pwd)

   

def alt_submit():

    alt_submit=messagebox.askquestion("UPDATE RECORD",f"Are you sure to update Record :{alt_record_id} (y/n) ?")

    if alt_submit=='yes':
        print("yes")

    else:
        print("no")

    

def alt_edit():
    global key
    global f
    decrypted_list=[]
    global alt_site_new_password_entry
    global alt_record_id

    selected_item=tree.selection()
    row=tree.item(selected_item)
    values=row["values"]
    
    new_values=[values[1],values[2],values[3],values[5]] #values 0 omitted
    alt_created_date=values[4] #CREATED DATE
    alt_record_id=values[6] #RECORD ID
    alt_site_name=values[0]

    
    

    for value in new_values:
        print(value)
        value_bytes=value.encode()
        decrypted_data_bytes=f.decrypt(value_bytes)
        decrypted_data_str=decrypted_data_bytes.decode()
        decrypted_list.append(decrypted_data_str)

    print(decrypted_list)
        
   

    alt_edit=Toplevel(root)
    
    alt_edit.title("EDIT A RECORD")
    alt_edit.geometry("730x650")
    
    
    alt_site_name_label=Label(alt_edit,text="SITE NAME  :", bg="white")
    alt_site_name_label.place(x=10,y=10)

    alt_site_name_entry=Entry(alt_edit,width=50,bg="white")
    alt_site_name_entry.place(x=125,y=10)

    alt_site_user_name_label=Label(alt_edit,text="USER NAME :", bg="white")
    alt_site_user_name_label.place(x=10,y=50)

    alt_site_user_name_entry=Entry(alt_edit,width=50,bg="white")
    alt_site_user_name_entry.place(x=125,y=50)

    alt_site_email=Label(alt_edit,text="E-MAIL  :", bg="white")
    alt_site_email.place(x=10,y=90)

    alt_site_email_entry=Entry(alt_edit,width=50,bg="white")
    alt_site_email_entry.place(x=125,y=90)

    alt_site_pass=Label(alt_edit,text="OLD PASSWORD :", bg="white")
    alt_site_pass.place(x=10,y=130)

    alt_site_pass_entry=Entry(alt_edit,bg="white", width=50)
    alt_site_pass_entry.place(x=125,y=130)

    alt_created_data_label=Label(alt_edit,text="CREATED DATE:",bg="white")
    alt_created_data_label.place(x=10,y=170)

    alt_created_data_entry=Entry(alt_edit,width=50,bg="white")
    alt_created_data_entry.place(x=125,y=170)

    alt_record_id_label=Label(alt_edit,text="ID NUMBER", bg="white")
    alt_record_id_label.place(x=10,y=210)

    alt_site_record_entry=Entry(alt_edit,width=20,bg="white")
    alt_site_record_entry.place(x=125,y=210)

    alt_site_new_password_label=Label(alt_edit,text="NEW PASSWORD", bg="white")
    alt_site_new_password_label.place(x=10,y=250)

    

    alt_site_new_password_entry=Entry(alt_edit,width=50,bg="white")
    alt_site_new_password_entry.place(x=125,y=250)


    alt_site_password_digit=Spinbox(alt_edit,from_=4, to=25) #take digit no here
    alt_site_password_digit.place(x=350,y=250)
    
    
    alt_site_create_button=Button(alt_edit,text="PRESS TO CREATE NEW PASSWORD",command=lambda:alt_create_pass(int(alt_site_password_digit.get())))
    alt_site_create_button.place(x=10,y=290)

    

    alt_site_submit_button=Button(alt_edit,text="SUBMIT RECORD",command=alt_submit)
    alt_site_submit_button.place(x=250,y=290)

    #GET DATA FROM TREEVIEW

    
    alt_site_name_entry.insert(0, alt_site_name)
    alt_site_user_name_entry.insert(0, decrypted_list[0])
    alt_site_email_entry.insert(0,decrypted_list[1])
    alt_site_pass_entry.insert(0,decrypted_list[2])

    alt_created_data_entry.insert(0,values[4])
    alt_site_record_entry.insert(0,values[6])


    alt_edit.mainloop()
    
    
    
def import_csv():
    root.filename=filedialog.askopenfilename(initialdir="/python", title="SELECT A KEY FILE", filetypes=(("CSV files", "*.csv"), ("all files","*.*")))
    today=date.today()
    d1=today.strftime("%d/%m/%Y")

    #open database to update
    conn=sqlite3.connect("sample_1.db")
    c=conn.cursor()
    with open(root.filename,"r") as csv_f:
        reader=csv.reader(csv_f)
        for i, row in enumerate(reader):
            if i==0:
                continue
            #tree.insert(parent="",index=i-1,iid=i-1,text="",values=(row[0],row[1],row[2],row[3],d1,len(row[3]),i))
            c.execute("""
            INSERT INTO drecords(adres,kullanici_adi,kullanici_email,parola,created_date,strength)
            VALUES(?,?,?,?,?,?)
            """,(row[0],row[1],row[2],row[3],d1,len(row[3])))
    conn.commit()
    conn.close()
 
   
    
#LABELS and ENTRY
# will check if it needs GLOBAL values

global entry_site_name
   
    #SITE NAME 

label_site_name=Label(root, text= "SITE NAME    :",bg="white")
label_site_name.place(x=10, y=10)
entry_site_name=Entry(root, width=40, bg="white")
entry_site_name.place(x=95, y=10)

    #USER NAME
label_user_name=Label(root, text="USER NAME :", bg="white")
label_user_name.place(x=10, y=50)
entry_user_name=Entry(root, width=40, bg="white")
entry_user_name.place(x=95, y=50)

     #EMAIL

label_email=Label(root, text="E-MAIL        :", bg="white")
label_email.place(x=10, y=90)
entry_email=Entry(root, width=40, bg="white")
entry_email.place(x=95, y=90)

    #PASSWORD LENGTH
label_password_length=Label(root, text="PASS LENGTH : ", bg="white")
label_password_length.place(x=10, y=130)
entry_password_length= Spinbox(root, from_=4, to=20)                                      # try except ile alternatif Entry(root, width=10, bg="white")
entry_password_length.place(x=95, y=130)

    #ADMIN PASSWORD AND CONNECT 
global entry_admin_name
global entry_admin_password
label_admin_name=Label(root, text="ADMIN USER NAME:", bg="white")
label_admin_name.place(x=10, y=500)
entry_admin_name=Entry(root,width=40)
entry_admin_name.place(x=150, y=500)

label_admin_password=Label(root, text="ADMIN PASSWORD:", bg="white")
label_admin_password.place(x=10, y=540)
entry_admin_password=Entry(root, width=40, show="*") # show * eklenecek 
entry_admin_password.place(x=150, y=540)
button_admin_pass=Button(root, text="CONNECT TO DATABASE", command=admin_check)
button_admin_pass.place(x=10,y=580)
connection_status=Label(root, text="NOT CONNECTED", fg="red")
connection_status.place(x=60,y=640)

key_status_label=Label(root,text="KEY NOT LOADED", fg="red")
key_status_label.place(x=190,y=640)

#SEARCH ENTRY FIELD




def search_record():
    z=0
    search_term=search_var.get()
    for child in tree.get_children():
        text=tree.item(child)["text"]
        if search_term in text:
            
            tree.see(child)
            tree.selection_add(child)
            z+=1
        else:
            tree.selection_remove(child)
    print(z)       
    tree.update()

search_var=StringVar()


search_record_label=Label(root, text="SEARCH RECORD :",fg="blue")
search_record_label.place(x=320,y=640)

search_record_entry=Entry(root,width=50,textvariable=search_var)
search_record_entry.place(x=430,y=640)

search_record_button=Button(root,text="SEARCH",command=search_record)
search_record_button.place(x=740,y=640)

#ENCRYPT DATA

button_encrypt=Button(root,text="ENCRYPT DATA",command=encrypt_records)
button_encrypt.place(x=280,y=580)

#DECRYPT DATA
button_decrypt=Button(root,text="DECRYPT DATA", command=decrypt_records)
button_decrypt.place(x=400,y=580)

#ALT EDIT

button_alt=Button(root,text="ALT EDIT", command=alt_edit)
button_alt.place(x=550,y=580)

button_importfromcsv=Button(root,text="IMPORT FROM CSV",command=import_csv)
button_importfromcsv.place(x=650,y=580) 

    #LOAD FERNET KEY
button_load_key=Button(root,text="LOAD KEY", command=load_key)
button_load_key.place(x=170,y=580)

    #CREATE PASSWORD
button_create_password=Button(root, text="PRESS TO CREATE RANDOM PASSWORD", bg="white", command=create_password)
button_create_password.place(x=10,y=160)
entry_create_password=Entry(root,width=30,bg="white",  font=("Arial", 12))
entry_create_password.place(x=10,y=200)

# Or DECIDE YOUR OWN PASS WORD
label_decide_password=Label(root,  text="OR TYPE DOWN ")
label_decide_password.place(x=220, y=200)

#SUBMIT RECORD
button_submit_records=Button(root,text="SUBMIT RECORD", command=submit_records)
button_submit_records.place(x=10, y=230)


#SHOW RECORD

button_show_records=Button(root, text="SHOW RECORDS", command=show_records)
button_show_records.place(x=130, y=230)

 # HIDE RECORDS
button_hide_records=Button(root, text="HIDE RECORDS", command=hide_records)
button_hide_records.place(x=250, y=230)


#SAVE RECORDS TO CSV
button_saveto_csv=Button(root, text="SAVE AS CSV", command=save_csv)
button_saveto_csv.place(x=370, y=230)


#ID LABEL 
id_label=Label(root, text="ID NO:" )
id_label.place(x=480, y=235)
id_entry=Entry(root, width=10)
id_entry.place(x=520, y=235)


# ID RECORD DELETE
id_delete_button=Button(root, text="DELETE RECORD", command=delete_record)
id_delete_button.place(x=600, y=230)

# ID EDIT BUTTON
id_edit_button=Button(root, text="EDIT RECORD", command=edit_record)
id_edit_button.place(x=710,y=230)

#ID UPDATE BUTTON
id_update_button=Button(root, text="UPDATE RECORD", command=update_record)
id_update_button.place(x=820, y=230)


#TIPS FOR GOOD PASSWORD
button=Button(root, text="TIPS FOR GOOD PASSWORD", command=tipps)
button.place(x=950, y=650)


#QUIT PROGRAM BUTTON 
button_exit=Button(root, width=10, borderwidth=1, text="QUIT", command=quit_program, relief="raised", bd=1,activebackground='blue') #relief flat, groove, raised, ridge, solid, or sunken
button_exit.place(x=1050,y=230)





#PASSWORD SECURITY CHECK ZONE

frame_pass_control=LabelFrame(root, text="HOW SECURE IS YOUR PASSWORD" ,width=400, height=200, borderwidth=5, bg="white")
frame_pass_control.place(x=700,y=10)

label_length=Label(frame_pass_control)
label_length.place(x=10,y=10)

button_check_security=Button(frame_pass_control, text="SECURITY CHECK", command=security_check)
button_check_security.place(x=150,y=150)

button_clear_security=Button(frame_pass_control, text="CLEAR SCREEN", command=clear_security_display)
button_clear_security.place(x=280, y=150)


label_strength_level=Label(frame_pass_control, font=("Arial", 12, "bold"))
label_strength_level.place(x=10,y=30)

label_special_chars=Label(frame_pass_control, font=("Arial", 12, "bold"))
label_special_chars.place(x=10,y=50)

label_numbers=Label(frame_pass_control)
label_numbers.place(x=10, y=70)

label_uppercase=Label(frame_pass_control)
label_uppercase.place(x=10, y=90)

label_lowercase=Label(frame_pass_control)
label_lowercase.place(x=10, y=110)


        
root.mainloop()