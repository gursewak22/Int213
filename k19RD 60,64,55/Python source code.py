from tkinter import *
from tkinter import ttk
import mysql.connector
class Admission:
    def __init__(self,root):
        self.root=root
        self.root.title("College Admission Management System")
        self.root.geometry("1000x520")
        self.root.resizable(0,0)

      #   Designing the Window and adding a background image
        f2 = Frame(self.root, borderwidth=8, bg="grey", relief=SUNKEN)
        f2.pack(side=TOP, fill="x")
        title = Label(f2,text="College Admission Management System", font=("bold", 20), fg="green", bd=5, relief=SUNKEN, bg="black")
        title.pack(side="top")
    #           Variable which we will use to perform various functions
        self.nameval = StringVar()
        self.branchnameval = StringVar()
        self.sectionval = StringVar()
        self.regnoval = StringVar()
        self.genderval = StringVar()
        self.dobval = StringVar()
        self.searchby = StringVar()
        self.searhtxt = StringVar()
### the following code is used to create frame for performing function to add students details
        f1 = Frame(self.root, bg="grey", borderwidth=6, relief=SUNKEN)
        f1.place(x=7,y=65,height=450,width=450)
        a=Label(f1, text="Enter Student Details", font=10, bg="green", bd=7)
        a.grid(columnspan=3,pady=10)
        name = Label(f1, text="Name", font=5, bg="yellow", bd=4)
        name.grid(row=1,pady=10,padx=5)
        namee=Entry(f1, font=8, bd=6,textvariable=self.nameval)
        namee.grid(row=1,column=2,padx=60)
        Branch = Label(f1, text="Branch Name", font=(5), bg="yellow", bd=4)
        Branch.grid(row=2, pady=10, padx=5)
        branchh= Entry(f1, font=(8), bd=6,textvariable=self.branchnameval)
        branchh.grid(row=2, column=2, padx=60)
        dob = Label(f1, text="Date-Of-Birth", font=(5), bg="yellow", bd=4)
        dob.grid(row=3, pady=10, padx=5)
        DOB= Entry(f1, font=(8), bd=6,textvariable=self.dobval)
        DOB.grid(row=3, column=2)
        reg= Label(f1, text="Registration No", font=(5), bg="yellow", bd=4)
        reg.grid(row=4, pady=10, padx=5)
        REG = Entry(f1, font=(8), bd=6,textvariable=self.regnoval)
        REG.grid(row=4, column=2)
        sec = Label(f1, text="Section", font=(5), bg="yellow", bd=4)
        sec.grid(row=6, pady=10, padx=5)
        SEC = Entry(f1, font=(8), bd=6,textvariable=self.sectionval)
        SEC.grid(row=6, column=2)
        gen= Label(f1, text="Gender", font=(5), bg="yellow", bd=4)
        gen.grid(row=5, pady=10, padx=5)

        combo=ttk.Combobox(f1,textvariable=self.genderval,font=(8))
        combo['values']=("Male","Female","Others")
        combo.grid(row=5, column=2)




        frame3= Frame(self.root, bg="grey", borderwidth=6, relief=SUNKEN)
        frame3.place(x=7, y=460, width=450)
        ##  the button created on root is used to crete buttons. As soon as someone clicks this button, we call the function.
        # We call a function by specifying the command parameter equal to the name of the function.

        button1=Button(frame3,text="Add",width=10,command=self.addstudent).grid(row=0,column=0,padx=10,pady=10)
        button2 = Button(frame3, text="Update", width=10,command=self.update).grid(row=0, column=1, padx=10, pady=10)
        button3 = Button(frame3, text="Delete", width=10,command=self.delete).grid(row=0, column=2, padx=10, pady=10)
        button4 = Button(frame3, text="Clear", width=10,command=self.clear).grid(row=0, column=3, padx=10, pady=10)


        frame4= Frame(self.root, bg="grey", borderwidth=6, relief=SUNKEN)
        frame4.place(x=465, y=65, width=530,height=450)

        search = Label(frame4, text="Search By", font=(5), bg="green", bd=6)
        search.grid(padx=10, pady=10)
        comboo = ttk.Combobox(frame4, font=(8),width=8,textvariable=self.searchby)
        comboo['values'] = ("Name", "Reg no", "Section")
        comboo.grid(column=1, row=0)


        s = Entry(frame4, font=(4), bd=6,textvariable=self.searhtxt)
        s.grid(row=0, column=2,padx=15)

        butto = Button(frame4, text="Search", width=10).grid(row=0, column=3,  pady=6)

        frame5 = Frame(frame4, bg="grey", borderwidth=6, relief=SUNKEN)
        frame5.place(x=5, y=60, width=500, height=380)
        # ================TABLE FRAME===============================
        scroll_x = Scrollbar(frame5, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame5, orient=VERTICAL)

        self.studenmttable =ttk.Treeview(frame5,columns=("Name","Branchname","DOB","RegNo","Gender","Section"), yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command= self.studenmttable.xview)
        scroll_y.config(command= self.studenmttable.yview)
        self.studenmttable.heading('Name', text='Name')
        self.studenmttable.heading('Branchname', text='Branchname')
        self.studenmttable.heading('DOB', text='DOB')
        self.studenmttable.heading('RegNo', text='RegNo')
        self.studenmttable.heading('Gender', text='Gender')
        self.studenmttable.heading('Section', text='Section')

        self.studenmttable['show'] = 'headings'

        self.studenmttable.column('Name', width=200)
        self.studenmttable.column('Branchname', width=200)
        self.studenmttable.column('DOB', width=300)
        self.studenmttable.column('RegNo', width=200)

        self.studenmttable.column('Gender', width=100)
        self.studenmttable.column('Section', width=150)
        self.studenmttable.pack(fill=BOTH, expand=1)
        self.studenmttable.bind("<ButtonRelease-1>",self.getcursor)
        self.fetchdata()

    def addstudent(self):
        con = mysql.connector.connect(host='localhost',
                                      database='admission',
                                      user='root',
                                      password='Patanahi1@')
        cur = con.cursor()
        cur.execute("insert into std_admission values(%s,%s,%s,%s,%s,%s)",
                    (self.nameval.get(), self.branchnameval.get(), self.dobval.get(), self.regnoval.get(),
                     self.genderval.get(), self.sectionval.get()))
        con.commit()
        self.fetchdata()
        self.clear()
        con.close()
    def fetchdata(self):
        con = mysql.connector.connect(host='localhost',
                                      database='admission',
                                      user='root',
                                      password='Patanahi1@')
        cur = con.cursor()
        cur.execute("select *from  std_admission")
        rows=cur.fetchall()
        if len(rows) !=0:
            self.studenmttable.delete(*self.studenmttable.get_children())
            for  row in rows:
                self.studenmttable.insert('', END, values=row)
                con.commit()
        con.close()

    def clear(self):
        self.nameval.set("")
        self.branchnameval.set("")
        self.dobval.set("")
        self.regnoval.set("")
        self.genderval.set("")
        self.sectionval.set("")

    def getcursor(self,ev):
        cursorrow=self.studenmttable.focus()
        contents=self.studenmttable.item(cursorrow)
        row=contents['values']
        self.nameval.set(row[0])
        self.branchnameval.set(row[1])
        self.dobval.set(row[2])
        self.regnoval.set(row[3])
        self.genderval.set(row[4])
        self.sectionval.set(row[5])


    def update(self):
        con = mysql.connector.connect(host='localhost',
                                      database='admission',
                                      user='root',
                                      password='Patanahi1@')
        cur = con.cursor()
        cur.execute("update  std_admission set name=%s,branchname=%s,dob=%s,gender=%s,section=%s where regno=%s",
                    (self.nameval.get(), self.branchnameval.get(), self.dobval.get(), self.regnoval.get(),
                     self.genderval.get(), self.sectionval.get()))
        con.commit()
        self.fetchdata()
        self.clear()
        con.close()

    def delete(self):
        con = mysql.connector.connect(host='localhost',
                                      database='admission',
                                      user='root',
                                      password='Patanahi1@')
        cur = con.cursor()
        cur.execute("DELETE FROM  admission.std_admission where name=%s",self.nameval.get())
        con.commit()
        con.close()
        self.fetchdata()
        self.clear()

    def search_data(self):
        con = mysql.connector.connect(host='localhost',
                                      database='admission',
                                      user='root',
                                      password='Patanahi1@')
        cur = con.cursor()
        cur.execute(
            "select * from students where" + str(self.search_by.get()) + " LIKE '%" + str(self.search_txt.get()) + "%'")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', END, values=row)
            con.commit()
        con.close()
root= Tk()
object=Admission(root)
root.mainloop()


