from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk, Frame, Label, PhotoImage, Button

start_p = Tk()
w = 860
h = 630
start_p.geometry(f'{w}x{h}+{250}+{40}')
start_p.overrideredirect(True)
start_p.iconbitmap(r'sis.ico')
start_p.configure(background="black")
start_p.resizable(False, False)
start_p.attributes('-alpha', 0.5)

conn = sqlite3.connect('StudentsList.db')
c = conn.cursor()



c.execute("""CREATE TABLE IF NOT EXISTS studentlist (
          name,
          idnum,
          gender,
          course_code,
          year_lvl                
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS courselist (       
          course_code, 
          course
                        
          )""")



# sis Gif animation
frameCnt = 10
frames = [PhotoImage(file='loading1.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
            ind = 0
    label.configure(image=frame, bg='black')
    start_p.after(50, update, ind)

label = Label(start_p)
label.place(x=200, y=20)
start_p.after(0, update, 0)


def student_list_p():
    root2 = Tk()
    w = 995
    h = 500
    root2.geometry(f'{w}x{h}+{200}+{110}')
    root2.resizable(False, False)
    root2.configure(background="#161618")
    root2.iconbitmap(r'sis.ico')
    root2.overrideredirect(True)

    # sis Gif animation
    frameCnt = 40
    frames = [PhotoImage(file='giphy.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame, bg='#161618')
        root2.after(50, update, ind)

    label = Label(root2)
    label.place(x=750, y=-30)
    root2.after(0, update, 0)

    def search_p():
        root3 = Tk()
        w = 995
        h = 250
        root3.geometry(f'{w}x{h}+{280}+{200}')
        root3.title('Record')
        root3.iconbitmap(r'sis.ico')
        root3.resizable(False, False)
        root3.configure(background="#161618")

        if srch_entry.get() == "":
            messagebox.showwarning("Search Warning", "Please Input ID Number...")
        else:
            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()


            c.execute("""SELECT name,idnum,gender,courselist.course_code,year_lvl,courselist.course 
                          FROM studentlist 
                          INNER JOIN courselist  ON courselist.course_code = studentlist.course_code WHERE idnum =?
                           """, (srch_entry.get(),))
            records = c.fetchall()

            def back():
                root3.destroy()

            ttk.Style().theme_use("clam")
            ttk.Style().configure("Treeview", background="light blue",
                                  foreground="black", fieldbackground="light blue")
            ttk.Style().map('Treeview', background=[('selected', 'black')])

            frm = Frame(root3)
            frm.pack(side=tk.LEFT, padx=5, pady=(90, 10))

            tv = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height="15")
            tv.pack()

            tv.heading(1, text="NAME", anchor=tk.CENTER)

            tv.heading(2, text="ID NUMBER", anchor=tk.CENTER)
            tv.column("2", minwidth=0, width=150)

            tv.heading(3, text="GENDER", anchor=tk.CENTER)
            tv.column("3", minwidth=0, width=150)

            tv.heading(6, text="COURSE", anchor=tk.CENTER)
            tv.column("6", minwidth=0, width=280)

            tv.heading(4, text="COURSE CODE", anchor=tk.CENTER)
            tv.column("4", minwidth=0, width=100)

            tv.heading(5, text="YEAR LEVEL", anchor=tk.CENTER)
            tv.column("5", minwidth=0, width=100)

            b = Button(root3, text="Return", bg="gray",
                       borderwidth=1, activebackground="#161618", command=back)
            b.place(x=938, y=60)
          
            sea_lbl = Label(root3, text="Data Search Found...", font=('helvetica', 18), bg="#161618", fg="white")
            sea_lbl.place(x=400, y=16)

            for i in records:
                tv.insert('', 'end', value=i)

            if not records:
                root3.destroy()
                messagebox.showinfo("Search Information", "Student Doesn't Exist or Wrong Input")



        root3.mainloop()

    def delete():
        if messagebox.askyesno("Delete Confirmation", "Do you wanna Delete this Student") == False:
            return
        else:
            messagebox.showinfo("Delete Confirmation", "Successfully Deleted")
            conn = sqlite3.connect("StudentsList.db")
            c = conn.cursor()
            for selected_item in tv.selection():
                c.execute("DELETE FROM studentlist WHERE idnum=?", (tv.set(selected_item, '#2'),))
                conn.commit()
                tv.delete(selected_item)
            conn.close()

    def select():
        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        name.delete(0, END)
        idnum.delete(0, END)
        gender.delete(0, END)
        course.delete(0, END)
        yr_lvl.delete(0, END)

        selected = tv.focus()
        values = tv.item(selected, 'values')

        name.insert(0, values[0])
        idnum.insert(0, values[1])
        gender.insert(0, values[2])
        course.insert(0, values[3])
        yr_lvl.insert(0, values[4])


        conn.commit()
        conn.close()

    def updates():
        if messagebox.askyesno("Update","Are you sure you want to update this ") == False:
            return
        else:
            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()
            messagebox.showinfo("Update Info", "Yey you have update successfully")
            data1 = name.get()
            data2 = idnum.get()
            data3 = gender.get()
            data4 = course.get()
            data5 = yr_lvl.get()

            selected = tv.selection()
            tv.item(selected, values=(data1, data2, data3, data4, data5))

            c.execute("UPDATE studentlist set  name=?, idnum=?, gender=?, course_code=?, year_lvl=?  WHERE idnum=? ",
                      (data1, data2, data3, data4, data5, data2))

            conn.commit()
            conn.close()


    def refresh():
        root2.destroy()
        refe = Tk()
        w = 350
        h = 350
        refe.geometry(f'{w}x{h}+{510}+{200}')
        refe.overrideredirect(True)
        refe.configure(background="black")
        refe.resizable(False, False)

        refe.attributes('-alpha', 0.2)



        # sis Gif animation
        frameCnt = 8
        frames = [PhotoImage(file='refresh.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame, bg='black')
            refe.after(50, update, ind)

        label = Label(refe)
        label.place(x=5, y=5)
        start_p.after(0, update, 0)


        def des():
            refe.destroy()

        refe.after(1000, lambda: (des(), student_list_p()))
        refe.mainloop()



    def register():
        root1 = Tk()
        w = 400
        h = 400
        root1.geometry(f'{w}x{h}+{480}+{170}')
        root1.configure(background="#161618")
        root1.resizable(False, False)
        root1.iconbitmap(r'sis.ico')
        #root1.overrideredirect(True)
        fa = Frame(root1, width=410, height=340, highlightbackground="white", highlightthickness=1, bg="#161618")
        fa.place(x=20, y=20)

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        def register():

            if name.get() == '':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")
            elif idnum.get() == '':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")
            elif gender.get() == 'Gender':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")
            elif course_code.get() == 'Course Code':
                 return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")
            elif course.get() == 'Year Level':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")

            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()

            c.execute("INSERT INTO studentlist VALUES(:name, :idnum, :gender, :course_code,:year_lvl)",
                      {
                          'name': name.get(),
                          'idnum': idnum.get(),
                          'gender': gender.get(),
                          'course_code': course_code.get(),
                          'year_lvl': yr_lvl.get()

                      })

            conn.commit()
            messagebox.showinfo("Register Confirmation", "Successfully Registered")
            conn.close()

            # To reset the given value
            name.delete(0, END)
            idnum.delete(0, END)
            gender.set("Gender")
            course_code.set("Course Code")
            yr_lvl.set("Year Level")
            root1.destroy()

        def back():
            root1.destroy()

        name = Entry(root1, width=30)
        name.place(x=115, y=80)

        idnum = Entry(root1, width=30)
        idnum.place(x=115, y=110)

        gender = ttk.Combobox(root1, width=12)
        gender.set("Gender")
        gender['values'] = ("Male", "Female", "Transgender", "Gender queer", "Gender Neutral", "Others")
        gender.place(x=40, y=150)

        c.execute("SELECT course_code FROM courselist")
        cd = c.fetchall()

        course_code = ttk.Combobox(root1, width=12)
        course_code.set("Course Code")
        course_code['values'] = (cd)
        course_code.place(x=160, y=150)

        yr_lvl = ttk.Combobox(root1, width=12)
        yr_lvl.set("Year Level")
        yr_lvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
        yr_lvl.place(x=280, y=150)

        register_lbl = Label(root1, bg="#161618", text="REGISTER", font=('Helvetica', 25, 'bold'), fg="White")
        register_lbl.place(x=115, y=5)

        name_lbl = Label(root1, bg="#161618", fg='white', text="Complete Name:", font=('helvetica', 10))
        name_lbl.place(x=7, y=80)

        idnum_lbl = Label(root1, bg="#161618", text="ID Number:", fg='white', font=('helvetica', 10))
        idnum_lbl.place(x=7, y=110)

        register_btn = Button(root1,text="REGISTER", borderwidth=5,width=15,
                              activebackground="#161618", bg="white", command=register)
        register_btn.place(x=151, y=210)

        b = Button(root1, text="Return", bg="gray",
                   borderwidth=1, activebackground="#161618", command=back)
        b.place(x=313, y=290)

        conn.commit()
        conn.close()
        root1.mainloop()

    def cr():
        root5 = Tk()
        w = 400
        h = 200
        root5.geometry(f'{w}x{h}+{480}+{170}')
        root5.configure(background="#161618")
        root5.resizable(False, False)
        root5.iconbitmap(r'sis.ico')
        # root1.overrideredirect(True)

        def register_c():

            if course_code.get() == '':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")

            elif courses.get() == '':
                return messagebox.showwarning("Warning!", "PLEASE COMPLETE THE INPUT")

            else:

                conn = sqlite3.connect('StudentsList.db')
                c = conn.cursor()

                c.execute("SELECT course_code FROM courselist")
                c_d = c.fetchall()

                for i in c_d:
                    if course_code.get() in i:
                        return messagebox.showwarning("Course Register Warning", "Course Already Register")



                else:
                    conn = sqlite3.connect('StudentsList.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO courselist VALUES(:course_code, :course)",
                              {

                                  'course_code': course_code.get(),
                                  'course': courses.get()

                              })

                    conn.commit()

                    conn.close()

                    # To reset the given value
                    course_code.delete(0, END)
                    courses.delete(0, END)





            messagebox.showinfo("Register Confirmation", "Successfully Registered")

        course_code = Entry(root5, width=30)
        course_code.place(x=115, y=80)

        courses = Entry(root5, width=30)
        courses.place(x=115, y=110)

        ex = Label(root5, text="ADD COURSE", font=("Helvitica", 18, "bold"), bg="#161618", fg="white")
        ex.place(x=130, y=5)

        cc_lbl = Label(root5, bg="#161618", fg='white', text="Course Code:", font=('helvetica', 10))
        cc_lbl.place(x=7, y=80)

        c_lbl = Label(root5, bg="#161618", text="Course:", fg='white', font=('helvetica', 10))
        c_lbl.place(x=7, y=110)

        register_btn = Button(root5, text="Register Course", borderwidth=5, width=15,
                              activebackground="#161618", bg="white", command=register_c)
        register_btn.place(x=151, y=150)

        root5.mainloop()





    def exit():
        if messagebox.askyesno("Exit","Do You Want To Quit T.T?") == False:
            return
        else:
            root2.destroy()


    f = Frame(root2, width=0, height=510, highlightbackground="white", highlightthickness=4, bg="#161618")
    f.place(x=400, y=0)

    f2 = Frame(root2, width=260, height=0, highlightbackground="white", highlightthickness=4, bg="#161618")
    f2.place(x=400, y=80)

    # delete button
    delete_more_btn = Button(root2, bg="#161618", text="DELETE", fg="white", width= 9,command=delete)
    delete_more_btn.place(x=50, y=10)

    # Update button
    update_btn = Button(root2, bg="#161618", text="UPDATE", fg="white",width= 9, command=updates)
    update_btn.place(x=140, y=10)

    # Select Button
    slc_btn = Button(root2, bg="#161618", text="SELECT", fg="white",width= 9, command=select)
    slc_btn.place(x=230, y=10)

    c1 = PhotoImage(file="refresh.png")
    ref_btn = Button(root2, image=c1, compound=CENTER, bg="#161618", borderwidth=0
                    , activebackground="#161618", command=refresh)
    ref_btn.place(x=330, y=9)

    # exit button
    c4 = PhotoImage(file="exit.png")
    ex_btn = Button(root2, image=c4, compound=CENTER, bg="#161618", borderwidth=0
                    , activebackground="#161618", command=exit)
    ex_btn.place(x=5, y=100)

    #search button
    slc_btn = Button(root2, bg="#161618", text="Search", fg="white", width=9, activebackground="#161618", command=search_p)
    slc_btn.place(x=583, y=50)


    register_btn = Button(root2, text="Register Student", bg="white", borderwidth=1,
                          activebackground="#161618", command=register)
    register_btn.place(x=485, y=90)


    cc = Button(root2, text="Course Register", bg="yellow", borderwidth=3,
                          activebackground="#161618", command=cr)
    cc.place(x=485, y=120)


    #combobox Entry
    gender = ttk.Combobox(root2, width= 12)
    gender.set("Gender")
    gender['values'] = ("Male", "Female", "Transgender", "Gender queer", "Gender Neutral", "Others")
    gender.place(x=290, y= 80)

    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()

    c.execute("SELECT course_code FROM courselist")
    cd = c.fetchall()

    course = ttk.Combobox(root2, width=12)
    course.set("Course Code")
    course['values'] = (cd)
    course.place(x=180, y=120)


    yr_lvl = ttk.Combobox(root2, width=12)
    yr_lvl.set("Year Level")
    yr_lvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    yr_lvl.place(x=290, y=120)

    name = Entry(root2, width=20, borderwidth=0, bg="white")
    name.place(x=150, y=80)

    idnum = Entry(root2, width=5, borderwidth=0,bg="gray")
    idnum.place(x=10, y=500)

    srch_entry = Entry(root2, width=20, borderwidth=4)
    srch_entry.place(x=460 ,y=50)

    #label
    mins = PhotoImage(file="mini search.png")
    minse = Label(root2, image=mins,bg="#161618")
    minse.place(x=425 ,y=51)

    minse = Label(root2, text="Type ID No...", font=("Helvitica",18,"italic"), bg="#161618", fg="white")
    minse.place(x=458, y=5)

    ex = Label(root2, text="EXIT", font=("Helvitica", 8, "italic"), bg="#161618", fg="white")
    ex.place(x=20, y=92)

    #re = Label(root2, text="REGISTER", font=("Helvitica", 7, "italic"), bg="#161618", fg="white")
    #re.place(x=513, y=83)

    #Frame Table
    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()
    

    c.execute("""SELECT name,idnum,gender,courselist.course_code,year_lvl,courselist.course 
              FROM studentlist 
              INNER JOIN courselist  ON courselist.course_code = studentlist.course_code;
               """)
    records = c.fetchall()

    ttk.Style().theme_use("clam")
    ttk.Style().configure("Treeview", background="light gray",
                          foreground="black", fieldbackground="gray")
    ttk.Style().map('Treeview', background=[('selected', 'black')])

    frm = Frame(root2)
    frm.pack(side=tk.LEFT, padx=5, pady=(150,0))

    tv = ttk.Treeview(frm, columns=(1,2,3,4,5,6), show="headings", height="15")
    tv.pack()

    vsb = ttk.Scrollbar(root2, orient="vertical", command=tv.yview)
    vsb.place(x=782 + 190 + 2, y=188, height=300)

    tv.configure(yscrollcommand=vsb.set)

    tv.heading(1, text="NAME", anchor=tk.CENTER)

    tv.heading(2, text="ID NUMBER", anchor=tk.CENTER)
    tv.column("2", minwidth=0, width=150)

    tv.heading(3, text="GENDER", anchor=tk.CENTER)
    tv.column("3", minwidth=0, width=150)

    tv.heading(6, text="COURSE", anchor=tk.CENTER)
    tv.column("6", minwidth=0, width=280)

    tv.heading(4, text="COURSE CODE", anchor=tk.CENTER)
    tv.column("4", minwidth=0, width=100)

    tv.heading(5, text="YEAR LEVEL", anchor=tk.CENTER)
    tv.column("5", minwidth=0, width=100)

    for i in records:
        tv.insert('', 'end', value=i)

    conn.commit()
    conn.close()
    root2.mainloop()



def des():
    start_p.destroy()

start_p.after(1000, lambda :(des(), student_list_p()))
conn.commit()

start_p.mainloop()
