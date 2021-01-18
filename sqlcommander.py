import mysql.connector
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
import os
# ------------------------------MS imports for admin privileges start---------------------------------------------------
import ctypes
import enum
import sys
# ------------------------------MS imports for admin privileges end-----------------------------------------------------

class App():
    def __init__(self, root):
        #ri8misis - 8esh para8iroy
        self.root = root
        root.title("SQL Commander")
        root.resizable(False,False)
        self.widgets()
        win_width = root.winfo_reqwidth()
        win_hight = root.winfo_reqheight()
        pos_right = int(root.winfo_screenwidth()/3 - win_width/3)
        pos_down = int(root.winfo_screenheight()/3 - win_hight/3)
        root.geometry("800x450+{}+{}".format(pos_right, pos_down))
        self.host = ''
        self.user = ''
        self.pswd = ''
        self.db = ''

    def widgets(self):
        #basiko para8iro
        self.text = 'Δώστε εντολή sql και πατήστε "Εκτέλεση"'
        self.bt_text = 'Εκτέλεση'
        self.font = 'Arial 15 bold'
        self.error = tk.StringVar()
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=1, fill='both')
        self.canvas = tk.Canvas(self.frame, bg='lightblue')
        self.canvas.pack(expand=1, fill='both')
        #dimiourgia antikimenon ston camva
        self.image_bg = tk.PhotoImage(file='image.gif')
        self.canvas.create_image(0, 0, image=self.image_bg, anchor='nw')
        self.entry = tk.Entry(self.canvas, width=100, font='Arial 10')
        self.entry.pack()
        self.buttondb = tk.Button(self.canvas, text='Σύνδεση SQL db', font='Arial 12', command=self.db_connect, width=15,anchor='s')
        self.buttondb.pack()
        self.button1 = tk.Button(self.canvas, text=self.bt_text, font='Arial 12', command=self.sql_file, width=15, anchor='s')
        self.button1.pack()
        self.button2 = tk.Button(self.canvas, text='Έξοδος', font='Arial 12', command=self.root.destroy, width=10, anchor='s')
        self.button2.pack()
        self.buttoni = tk.Button(self.canvas, text='About ', font='Arial 8 bold', width=4, command=self.info, anchor='s')
        self.buttoni.pack()
        #topothetish antikimenon ston camva
        self.pos_text = self.canvas.create_text(400, 180, text=self.text, font=self.font, width=500, anchor='n', fill='white')
        self.pos_pg_bar = self.canvas.create_window(400, 250, anchor='s', window=self.entry, height=30)
        self.pos_db = self.canvas.create_window(100, 50, anchor='s', window=self.buttondb)
        self.pos_b1 = self.canvas.create_window(400,300, anchor='s', window=self.button1)
        self.pos_b2 = self.canvas.create_window(750, 400, anchor='se', window=self.button2)
        self.pos_bi = self.canvas.create_window(798, 0, anchor='ne', window=self.buttoni)


    def db_connect(self):
        self.buttondb["state"] = "disabled"
        x, y = self.root.winfo_x(), self.root.winfo_y()
        self.cf = tk.Toplevel(self.frame)
        self.cf.geometry('+{}+{}'.format(x + 30, y + 80))
        self.cf.resizable(False, False)
        self.cf.title('Σύνδεση SQL db')
        self.cf.attributes("-topmost", True)
        self.cf.overrideredirect(True)
        #host entry
        self.host = tk.Frame(self.cf, padx=4, pady=4)
        self.host.pack(fill='both', expand=1)
        self.hostl = tk.Label(self.host, text='Host')
        self.hostl.pack(fill='x')
        self.hoste = tk.Entry(self.host, font='Arial 15', relief='sunken')
        self.hoste.pack(expand=True, fill='both')
        #user entry
        self.user = tk.Frame(self.cf, padx=4, pady=4)
        self.user.pack(fill='both', expand=1)
        self.userl = tk.Label(self.user, text='User')
        self.userl.pack(fill='x')
        self.usere = tk.Entry(self.user, font='Arial 15', relief='sunken')
        self.usere.pack(expand=True, fill='both')
        #password entry
        self.pswd = tk.Frame(self.cf, padx=4, pady=4)
        self.pswd.pack(fill='both', expand=1)
        self.pswdl = tk.Label(self.pswd, text='Password')
        self.pswdl.pack(fill='x')
        self.pswde = tk.Entry(self.pswd, font='Arial 15', relief='sunken')
        self.pswde.pack(expand=True, fill='both')
        # db entry
        self.db = tk.Frame(self.cf, padx=4, pady=4)
        self.db.pack(fill='both', expand=1)
        self.dbl = tk.Label(self.db, text='Database')
        self.dbl.pack(fill='x')
        self.dbe = tk.Entry(self.db, font='Arial 15', relief='sunken')
        self.dbe.pack(expand=True, fill='both')
        #buttons
        self.btn = tk.Frame(self.cf, padx=10, pady=10)
        self.btn.pack(fill='both', expand=1)
        self.btn1 = tk.Button(self.btn, text='OK', font='Arial 10', command=self.dbCredentials)
        self.btn1.pack(side='left', expand=True, fill='both')
        self.btn2 = tk.Button(self.btn, text='Άκυρο', font='Arial 10', command=self.close)
        self.btn2.pack(side='left', expand=True, fill='both')

    def info(self):
        tk.messagebox.showinfo('About', ' SQL Commander version 3.1 \n Credits: \n Κωνσταντίνος Καρακασίδης \n Βασίλης Κουτκούδης')

    def close(self):
        self.buttondb["state"] = "normal"
        self.cf.destroy()

    def _on_mousewheel(self, event):
        self.li.yview_scroll(int(-1*(event.delta/120)), "units")

    def dbCredentials(self):
        self.buttondb["state"] = "normal"
        self.host = self.hoste.get().strip()
        self.user = self.usere.get().strip()
        self.pswd = self.pswde.get().strip()
        self.db = self.dbe.get().strip()
        self.cf.destroy()

    def sql_file(self):
        try:
            mydb = mysql.connector.connect(host=self.host, user=self.user, password=self.pswd, database=self.db)
            mycursor = mydb.cursor()
            sql = self.entry.get().strip()
            if sql[:6] == 'INSERT' or sql[:6] == 'insert' or sql[:6] == 'UPDATE' or sql[:6] == 'update' or sql[
                                                                                                           :6] == 'DELETE' or sql[
                                                                                                                              :6] == 'delete':
                mycursor.execute(sql + ';')
                mycursor.execute('COMMIT;')
                self.matrix = tk.Label(self.canvas, fg='lightgreen', bg='black', font="Arial 12", textvariable=self.error,width=50, height=4, anchor='nw', padx=10, pady=5, justify=tk.LEFT)
                self.matrix.pack(fill='both', expand=1)
                self.pos_matrix = self.canvas.create_window(400, 420, anchor='s', window=self.matrix)
                self.error.set('Η εντολή "{}" ολοκληρώθηκε με επιτυχία\nΕκτελέστε την εντολή\nSELECT * FROM "TABLE"\nγια να δείτε τις αλλαγές'.format(sql[:6]))
            else:
                mycursor.execute(sql + ';')
                myresult = mycursor.fetchall()
                display_first_row = ''
                display_second_row = ''
                display_third_row = ''
                display_forth_row = ''
                display_fifth_row = ''
                display_sixth_row = ''
                for x in myresult:
                    display_first_row += str(x[0])+'\n'
                    display_second_row += str(x[1])+'\n'
                    display_third_row += str(x[2])+'\n'
                    display_forth_row += str(x[3])+'\n'
                    display_fifth_row += str(x[4])+'\n'
                    display_sixth_row += str(x[5]) + '\n'

                x, y = self.root.winfo_x()-200, self.root.winfo_y()-200
                self.info = tk.Toplevel(self.root)
                self.info.title('SQL Commander')
                self.info.resizable(False, False)
                self.info.geometry('1024x768+{}+{}'.format(x, y + 60))
                self.info.attributes("-topmost", True)
                #canvas
                self.li = tk.Canvas(self.info, bg='lightgray')
                self.li.pack(expand=1, fill='both', side=LEFT)
                #canvas items
                self.pos_text = self.li.create_text(512, 3, text='Αποτελέσματα ερωτήματος', font='Arial 20 bold', width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(512, 50, text=sql, font='Arial 14', width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(40, 100, text=display_first_row, font=self.font, width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(200, 100, text=display_second_row, font=self.font, width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(450, 100, text=display_third_row, font=self.font, width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(600, 100, text=display_forth_row, font=self.font, width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(750, 100, text=display_fifth_row, font=self.font, width=500, anchor='n', fill='black')
                self.pos_text = self.li.create_text(900, 100, text=display_sixth_row, font=self.font, width=500, anchor='n', fill='black')
                #scrollbar
                self.vbar=ttk.Scrollbar(self.info,orient=VERTICAL, command=self.li.yview)
                self.vbar.pack(side=RIGHT,fill=Y)
                self.li.configure(yscrollcommand=self.vbar.set)
                self.li.bind('<Configure>', lambda e: self.li.configure(scrollregion=self.li.bbox('all')))
                self.li.bind_all("<MouseWheel>", self._on_mousewheel)
                self.error.set('Η εντολή "{}" ολοκληρώθηκε με επιτυχία'.format(sql))



        except (mysql.connector.Error, mysql.connector.Warning) as err:
            self.matrix = tk.Label(self.canvas, fg='lightgreen', bg='black', font="Arial 12", textvariable=self.error, width=50, height=4, anchor='nw', padx=10, pady=5, justify=tk.LEFT)
            self.matrix.pack(fill='both', expand=1)
            self.pos_matrix = self.canvas.create_window(400, 420, anchor='s', window=self.matrix)
            self.error.set(err)


# ------------------------------MS code for admin privileges start------------------------------------------------------
class SW(enum.IntEnum):

    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):

    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        root = tk.Tk()
        App(root)
        root.mainloop()
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))

# ------------------------------MS code for admin privileges end--------------------------------------------------------

if __name__ == '__main__':
    app = bootstrap()
