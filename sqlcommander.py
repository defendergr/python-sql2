import mysql.connector
import datetime
import tkinter as tk
from tkinter import simpledialog
import os
import ctypes
import enum
import sys

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
        tk.messagebox.showinfo('About', ' SQL Commander version 2 \n Credits: \n Βασίλης Κουτκούδης \n Κωνσταντίνος Καρακασίδης')

    def close(self):
        self.buttondb["state"] = "normal"
        self.cf.destroy()

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
# ------------------------------Βασίλης Κουτκούδης code start------------------------------------------------------------
                mycursor.execute(sql + ';')
                myresult = mycursor.fetchall()
                header = '''
                                                    <!doctype html>
                                                    <html lang="en">
                                                      <head>
                                                        <!-- Required meta tags -->
                                                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                                                        <style>
                                                            .top-space{{margin-top:70px;}}
                                                            .bottom-space{{margin-bottom:70px;}}
                                                            .center{{text-align:center;}}
                                                        </style>

                                                    	<!-- Bootstrap CSS -->
                                                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

                                                    	<!-- Font Awesome CSS -->
                                                        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">
                                                    	<title>Δοκιμαστική Σελίδα για ΒΔ Company!</title>
                                                      </head>
                                                      <body>
                                                          <div class="container top-space bottom-space">
                                                                <div class="center">
                                                                    <h3>Αποτελέσματα ερωτήματος</h3>
                                                                    <p>"{sql}"</p>
                                                                </div>
                                                              <table width="100%" colspan="2" rowspan="2">
                                                    '''.format(sql=sql)

                footer = '''
                                                            </div>

                                                                </table >


                                                        <!-- Optional JavaScript -->
                                                        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                                                        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                                                        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                                                        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
                                                      </body>
                                                    </html>
                                                    '''

                # i = 1 #TODO 1.1 bazei arithmo stis seires

                # Δημιουργώ τον φάκελο "company" στον C για να έχουμε κοινό σημείο όλοι.
                path = 'C:\\company\\'
                if not os.path.isdir(path):
                    os.mkdir(path)

                f = open('C:\\company\\index.html', "w")  # Αυτό είναι το html αρχείο που δημιουργείται.

                f.write(header)
                for record in myresult:

                    f.write('<tr>')

                    # f.write('<td width="10px">')  #TODO 1.2 bazei arithmo stis seires
                    # f.write(str(i))
                    # f.write('</td>')

                    for data in record:
                        f.write('<td>')
                        f.write(str(data.day) + '-' + str(data.month) + '-' + str(data.year)) if isinstance(data,
                                                                                                            datetime.date) else f.write(
                            str(data))
                        f.write('</td>')

                    f.write('</tr>')
                    # i = i + 1 #TODO 1.3 bazei arithmo stis seires
                f.write(footer)

                f.close()
# ------------------------------Βασίλης Κουτκούδης code end-------------------------------------------------------------
                os.startfile('C:\\company\\index.html')
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
