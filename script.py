import PySimpleGUI as sg
import _sqlite3
from random import randint
import datetime


class Login_Signin(object):
    def __init__(self):
        self.conn = _sqlite3.connect('passcodes.db', timeout=10)
        self.cur = self.conn.cursor()
        self.layout = ""
        self.date_object = datetime.date.today()
        self.date = str(self.date_object.strftime("%d_%m_%Y"))
        self.ID = 0
        self.settings_list = []

    def database(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS passcode (Passcode_ID INTEGER NOT NULL, username TEXT, password TEXT,sq TEXT,email TEXT, PRIMARY KEY (Passcode_ID))")
        self.conn.commit()

    def get_passcode(self):
        self.database()
        self.layout = [[sg.Text("Login to your Account or type in desired Username and Password and press Sign in")], [sg.Text("Username"), sg.InputText()], [sg.Text("Password"), sg.InputText()],
                       [sg.Button("Login"), sg.Button("Sign in"), sg.Button("Forgot Password"), sg.Button("Delete Account"), sg.Exit()]]
        self.window = sg.Window("Login", self.layout)

        while True:
            event, values = self.window.read()
            self.text_input1 = str(values[0])
            self.text_input2 = str(values[1])

            if event in (None, "Exit"):
                break
                self.window.close()

            elif event in ("Delete Account"):
                self.security_question_delete = [
                    [sg.Text("Type in the answer for your security question.")], [sg.InputText()], [sg.Button("OK"), sg.Button("Exit")]]
                self.window_sq_delete = sg.Window(
                    "Delete", self.security_question_delete)
                while True:
                    event, values = self.window_sq_delete.read()
                    self.answersq_delete = str(values[0])
                    if event in (None, "Exit"):
                        self.window_sq_delete.close()
                        break

                    elif event in ("OK"):
                        self.cur.execute(
                            "SELECT sq FROM passcode WHERE username = ? AND sq = ?", (self.text_input1, self.answersq_delete))
                        self.get_sq = self.cur.fetchone()
                        if self.get_sq is None:
                            sg.popup("Wrong, please try again")
                        else:
                            self.window_sq_delete.close()
                            self.cur.execute(
                                "DELETE FROM passcode WHERE username = ?", (self.text_input1,))
                            self.conn.commit()
                            sg.popup("Account is deleted")
                            self.window.close()
                            break

            elif event in ("Login"):
                sg.popup("You entered", self.text_input1, self.text_input2)
                self.cur.execute(
                    "SELECT username FROM passcode WHERE username =?", (self.text_input1,))
                self.firste = self.cur.fetchone()
                if self.firste is not None:
                    self.cur.execute("SELECT password FROM passcode WHERE username=? AND password=?",
                                     (self.text_input1, self.text_input2))
                    self.second = self.cur.fetchone()
                    if self.second is not None:
                        sg.popup("Welcome")
                        self.set_ID()
                    else:
                        sg.popup("Error, please try again")
                else:
                    sg.popup(
                        "Username doesn't exits, please sign in or use other username")

            elif event in ("Sign in"):
                self.cur.execute(
                    "SELECT username FROM passcode WHERE username = ?", (self.text_input1,))
                self.check_username = self.cur.fetchone()

                if self.check_username is not None:
                    sg.popup(
                        "This username already exits, please choose another one")
                else:
                    self.ask_sq = [[sg.Text("What is your favorite animal?"), sg.InputText()], [sg.Text("Email"), sg.InputText()], [
                        sg.Button("OK"), sg.Button("EXIT")]]
                    self.window_make_sq = sg.Window(
                        "security question", self.ask_sq)

                    while True:
                        event, values = self.window_make_sq.read()
                        self.login_sq = str(values[0])
                        self.email_log = str(values[1])
                        if event in (None, "EXIT"):
                            self.window_make_sq.close()
                            break

                        elif event in ("OK"):
                            self.cur.execute(
                                "INSERT INTO passcode (username, password, sq, email) VALUES (?,?,?,?)", (self.text_input1, self.text_input2, self.login_sq, self.email_log))
                            self.conn.commit()
                            self.window_make_sq.close()
                            sg.popup(
                                "You signed in, now you can log in with your information")
                            break

            elif event in ("Forgot Password"):
                self.security_question_layout = [
                    [sg.Text("Type in the answer for your security question.")], [sg.InputText()], [sg.Button("OK"), sg.Button("Exit")]]
                self.window_sq = sg.Window(
                    "Forgot password", self.security_question_layout)
                while True:
                    event, values = self.window_sq.read()
                    self.answersq = str(values[0])
                    if event in (None, "Exit"):
                        self.window_sq.close()
                        break

                    elif event in ("OK"):
                        self.cur.execute(
                            "SELECT sq FROM passcode WHERE username = ? AND sq = ?", (self.text_input1, self.answersq))
                        self.get_sq = self.cur.fetchone()
                        if self.get_sq is None:
                            sg.popup("Wrong, please try again")
                        else:
                            self.window_sq.close()
                            self.new_password_func()
                            break

    def new_password_func(self):
        self.new_password = str(
            randint(10000, 99999))
        self.cur.execute(
            "UPDATE passcode SET password = ? WHERE username = ?", (self.new_password, self.text_input1))
        self.conn.commit()
        sg.popup("Your temporary password is:" + str(self.new_password) +
                 ". Please change it after you logged in.")

    def set_ID(self):
        self.cur.execute(
            "SELECT Passcode_ID FROM passcode WHERE username = ?", (self.text_input1,))
        self.IDE = self.cur.fetchone()
        for self.ID in self.IDE:
            self.ID = int(self.ID)

        # self.mainmenue()

    def account_settings(self):
        self.account_settings_layout = [[sg.Text("New password:")], [sg.InputText()], [sg.Text("Repeat new password")], [sg.InputText()], [sg.Text("New Username")], [
            sg.InputText()], [sg.Text("new Email")], [sg.InputText()], [sg.Text("new security answer")], [sg.InputText()], [sg.Button("SAVE"), sg.Button("EXIT")]]
        self.window_account_settings = sg.Window(
            "Account settings", self.account_settings_layout)
        while True:
            event, values = self.window_account_settings.read()
            self.new_password = str(values[0])
            self.new_password_repeat = str(values[1])
            self.new_username = str(values[2])
            self.new_email = str(values[3])
            self.new_secq = str(values[4])
            if event in (None, "EXIT"):
                self.window_account_settings.close()
                break

            elif event in ("SAVE"):
                self.settings_list = []
                if self.new_password is not None:
                    if self.new_password == self.new_password_repeat:
                        self.cur.execute(
                            "UPDATE passcode SET password = ? WHERE Passcode_ID = ?", (self.new_password, self.ID))
                        self.conn.commit()
                        self.settings_list.append("password")

                    else:
                        sg.popup("Passwords don't match")

                if self.new_username is not None:
                    self.cur.execute(
                        "UPDATE passcode SET username = ? WHERE Passcode_ID = ?", (self.new_username, self.ID))
                    self.conn.commit()
                    self.settings_list.append("username")

                if self.new_email is not None:
                    self.cur.execute(
                        "UPDATE passcode SET email = ? WHERE Passcode_ID = ?", (self.new_email, self.ID))
                    self.conn.commit()
                    self.settings_list.append("email")

                if self.new_secq is not None:
                    self.cur.execute(
                        "UPDATE passcode SET sq = ? WHERE Passcode_ID = ?", (self.new_secq, self.ID))
                    self.conn.commit()
                    self.settings_list.append("Security Question")

                sg.popup("You changed: ", str(self.settings_list))
                self.window_account_settings.close()
                break


test = Login_Signin()
print(test.get_passcode())
# print(test.account_settings(

"""from PySimpleGUI import Text, CBox, Input, Button, Window"""


"""def GUI():

    layout = [[Text(f'{i}. '), CBox(''), Input()]
              for i in range(1, 6)]
    layout += [[Button('Save'), Button('Exit')]]

    window = Window('Dayplanner', layout)
    event, values = window.read()"""
