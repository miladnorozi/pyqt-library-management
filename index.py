import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType
from xlrd import *
from xlsxwriter import *

ui, _ = loadUiType('library.ui')
login, _ = loadUiType('login.ui')

class Login(QWidget,login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.handelLogin)

    def handelLogin(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        userName = self.login_username.text()
        password = self.login_password.text()

        sql = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if userName == row[1] and password == row[3]:
                print('user match')
                self.mainWindow = MainApp()
                self.close()
                self.mainWindow.show()
            else:
                self.login_label.setText('Make Sure Your Enetered Username And Password Correct')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.ShowCategory()
        self.ShowAuthor()
        self.ShowPublisher()
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()
        self.showAllClients()
        self.showAllBooks()
        self.showAllOperations()

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabwidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.btn_theme.clicked.connect(self.Show_Themes)
        self.btn_close_theme.clicked.connect(self.Hiding_Themes)
        self.btn_daytoday.clicked.connect(self.Open_Day_To_Day_Tab)
        self.btn_book.clicked.connect(self.Open_Books_Tab)
        self.btn_users.clicked.connect(self.Open_Users_Tab)
        self.btn_setting.clicked.connect(self.Open_Settings_Tab)
        self.btn_add_book.clicked.connect(self.AddNewBook)
        self.add_category_btn_add.clicked.connect(self.AddCategory)
        self.add_author_btn_add.clicked.connect(self.AddAuthor)
        self.add_publisher_btn_add.clicked.connect(self.AddPublisher)
        self.search_btn.clicked.connect(self.SearchBooks)
        self.edit_btn_save.clicked.connect(self.EditBooks)
        self.edit_btn_delete.clicked.connect(self.DeleteBooks)
        self.add_user_btn.clicked.connect(self.AddNewUser)
        self.login_btn.clicked.connect(self.Login)
        self.edit_user_btn.clicked.connect(self.EditUser)
        self.theme_light.clicked.connect(self.light)
        self.theme_darkblue.clicked.connect(self.darkBlueTheme)
        self.theme_darkorange.clicked.connect(self.darkOrangeTheme)
        self.theme_qdark_gray.clicked.connect(self.qDarkGrayTheme)
        self.btn_clients.clicked.connect(self.Open_Clients_Tab)
        self.add_client_btn.clicked.connect(self.addNewClient)
        self.search_client_btn.clicked.connect(self.searchClient)
        self.edit_client_btn.clicked.connect(self.editClient)
        self.delete_client_btn.clicked.connect(self.deleteClient)
        self.daytoday_add_btn.clicked.connect(self.handelDayOperations)
        self.btn_export_daytoday.clicked.connect(self.exportDayToDay)
        self.btn_export_clients.clicked.connect(self.exportClients)
        self.btn_export_books.clicked.connect(self.exportBooks)

    def Show_Themes(self):
        self.groupbox_theme.show()

    def Hiding_Themes(self):
        self.groupbox_theme.hide()

    ################################
    ############# Tabs #############
    def Open_Day_To_Day_Tab(self):
        self.tabwidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabwidget.setCurrentIndex(1)

    def Open_Clients_Tab(self):
        self.tabwidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabwidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabwidget.setCurrentIndex(4)

    ################################
    ############# Books #############
    def AddNewBook(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        book_title = self.edt_book_title.text()
        book_description = self.edt_book_description.toPlainText()
        book_code = self.edt_book_code.text()
        book_price = self.edt_book_price.text()
        book_category = self.combo_book_category.currentText()
        book_author = self.combo_book_author.currentText()
        book_publisher = self.combo_book_publisher.currentText()

        self.cur.execute('''
            INSERT INTO book(book_name,book_description,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s, %s, %s,%s, %s, %s,%s)  
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.edt_book_title.setText('')
        self.edt_book_description.setText('')
        self.edt_book_code.setText('')
        self.edt_book_price.setText('')
        self.combo_book_category.setCurrentIndex(0)
        self.combo_book_author.setCurrentIndex(0)
        self.combo_book_publisher.setCurrentIndex(0)
        self.showAllBooks()

    def SearchBooks(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        book_title = self.search_book_title.text()

        sql = ''' SELECT * FROM book WHERE book_name = %s '''
        self.cur.execute(sql, [(book_title)])

        data = self.cur.fetchone()

        self.edit_title.setText(data[1])
        self.edit_description.setText(data[2])
        self.edit_code.setText(data[3])
        self.edit_combo_category.setCurrentText(data[4])
        self.edit_combo_author.setCurrentText(data[5])
        self.edit_combo_publisher.setCurrentText(data[6])
        self.edit_price.setText(data[7])

    def EditBooks(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        book_title = self.edit_title.text()
        book_description = self.edit_description.toPlainText()
        book_code = self.edit_code.text()
        book_price = self.edit_price.text()
        book_category = self.edit_combo_category.currentText()
        book_author = self.edit_combo_author.currentText()
        book_publisher = self.edit_combo_publisher.currentText()

        book_search_title = self.search_book_title.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s WHERE book_name=%s
        ''',(book_title,book_description,book_code,book_category,book_author,book_publisher,book_price,book_search_title))

        self.db.commit()
        self.statusBar().showMessage('book updated')
        self.showAllBooks()

    def DeleteBooks(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        book_title = self.edit_title.text()

        warning = QMessageBox.warning(self,'Delete book',"are you sure want to delete this book?",QMessageBox.Yes|QMessageBox.No)

        if warning == QMessageBox.Yes :
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql,[(book_title)])
            self.db.commit()
            self.statusBar().showMessage('book deleted')
        self.edit_title.setText('')
        self.edit_description.setText('')
        self.edit_code.setText('')
        self.edit_price.setText('')
        self.search_book_title.setText('')
        self.edit_combo_category.setCurrentIndex(0)
        self.edit_combo_author.setCurrentIndex(0)
        self.edit_combo_publisher.setCurrentIndex(0)
        self.showAllBooks()

    def showAllBooks(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_code,book_name,book_description,book_category,book_author,book_publisher,book_price FROM book ''')
        data = self.cur.fetchall()
        print(data)
        self.book_tabwidget.setRowCount(0)

        self.book_tabwidget.insertRow(0)

        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.book_tabwidget.setItem(row,column,QTableWidgetItem(str(item)))
                column+=1

            row_position = self.book_tabwidget.rowCount()
            self.book_tabwidget.insertRow(row_position)

        self.db.close()

    ################################
    ############# Users #############
    def AddNewUser(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        userName = self.add_user_username.text()
        email = self.add_user_email.text()
        password = self.add_user_password.text()
        passwordRepeat = self.add_user_password_repeat.text()

        if password == passwordRepeat:
            self.cur.execute('''
                INSERT INTO users(user_name,user_email,user_password) VALUES (%s,%s,%s)
            ''',(userName,email,password))
            self.db.commit()
            self.statusBar().showMessage('New User Added')
        else:
            self.label_validation.setText('please add a valid password twice')

    def Login(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        userName = self.login_username.text()
        password = self.login_password.text()

        sql = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if userName == row[1] and password == row[3]:
                print('user match')
                self.statusBar().showMessage('valid username and password')
                self.groupbox_edit_user.setEnabled(True)
                self.edit_user_username.setText(row[1])
                self.edit_user_email.setText(row[2])
                self.edit_user_password.setText(row[3])
                self.edit_user_password_repeat.setText(row[3])

    def EditUser(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        userName = self.edit_user_username.text()
        email = self.edit_user_email.text()
        password = self.edit_user_password.text()
        passwordRepeat = self.edit_user_password_repeat.text()

        if password == passwordRepeat:
            self.cur.execute('''
                UPDATE users SET user_name=%s , user_email = %s , user_password =%s WHERE user_name = %s
            ''', (userName, email, password,self.login_username.text()))
            self.db.commit()
            self.statusBar().showMessage('User Updated')
        else:
            print('make sure you entered your password correctly!')



    ################################
    ############# Settings #############
    def AddCategory(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        category_name = self.add_category_edt_name.text()

        self.cur.execute('''
            INSERT INTO  category (category_name) VALUES (%s)
        ''', (category_name,))
        self.db.commit()
        self.statusBar().showMessage('new category added')
        self.add_category_edt_name.setText('')
        self.ShowCategory()
        self.Show_Category_Combobox()

    def ShowCategory(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        if data:
            self.category_tabwidget.setRowCount(0)
            self.category_tabwidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.category_tabwidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.category_tabwidget.rowCount()
                self.category_tabwidget.insertRow(row_position)

    def AddAuthor(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        author_name = self.add_author_edt_name.text()

        self.cur.execute('''
             INSERT INTO  authors (author_name) VALUES (%s)
         ''', (author_name,))
        self.db.commit()
        self.statusBar().showMessage('new author added')
        self.add_author_edt_name.setText('')
        self.ShowAuthor()
        self.Show_Author_Combobox()

    def ShowAuthor(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()

        if data:
            self.author_tabwidget.setRowCount(0)
            self.author_tabwidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.author_tabwidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.author_tabwidget.rowCount()
                self.author_tabwidget.insertRow(row_position)

    def AddPublisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        publisher_name = self.add_publisher_edt_name.text()

        self.cur.execute('''
             INSERT INTO  publisher (publisher_name) VALUES (%s)
         ''', (publisher_name,))
        self.db.commit()
        self.statusBar().showMessage('new publisher added')
        self.add_publisher_edt_name.setText('')
        self.ShowPublisher()
        self.Show_Publisher_Combobox()

    def ShowPublisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()

        if data:
            self.publisher_tabwidget.setRowCount(0)
            self.publisher_tabwidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.publisher_tabwidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.publisher_tabwidget.rowCount()
                self.publisher_tabwidget.insertRow(row_position)

    ################################
    ############# Settings #############

    def Show_Category_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        self.combo_book_category.clear()
        for category in data:
            self.combo_book_category.addItem(category[0])
            self.edit_combo_category.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()
        self.combo_book_author.clear()
        for author in data:
            self.combo_book_author.addItem(author[0])
            self.edit_combo_author.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        self.combo_book_publisher.clear()
        for publisher in data:
            self.combo_book_publisher.addItem(publisher[0])
            self.edit_combo_publisher.addItem(publisher[0])

    ################################
    ############# UI Themes #############
    def darkBlueTheme(self):
        style = open('themes/darkblue.css','r')
        style = style.read()
        self.setStyleSheet(style)

    def darkOrangeTheme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def light(self):
        style = open('themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qDarkGrayTheme(self):
        style = open('themes/qdarkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    ################################
    ############# Clients #############
    def addNewClient(self):
        clientName = self.add_client_name.text()
        clientEmail = self.add_client_email.text()
        clientNationalId = self.add_client_nationalid.text()
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' INSERT INTO clients(client_name,client_email,client_nationalid) VALUES (%s,%s,%s)
        ''',(clientName,clientEmail,clientNationalId))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')
        self.showAllClients()
        self.add_client_name.setText('')
        self.add_client_email.setText('')
        self.add_client_nationalid.setText('')

    def showAllClients(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT client_name , client_email , client_nationalid FROM clients ''')
        data = self.cur.fetchall()
        print(data)
        self.client_tabwidget.setRowCount(0)

        self.client_tabwidget.insertRow(0)

        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.client_tabwidget.setItem(row,column,QTableWidgetItem(str(item)))
                column+=1

            row_position = self.client_tabwidget.rowCount()
            self.client_tabwidget.insertRow(row_position)

        self.db.close()

    def editClient(self):
        clientOriginalNationalId = self.search_client_nationalid.text()
        clientName = self.edit_client_name.text()
        clienEmail = self.edit_client_email.text()
        clientNationalId = self.edit_client_nationalid.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            UPDATE clients SET client_name=%s , client_email=%s , client_nationalid=%s WHERE client_nationalid=%s
        ''',(clientName,clienEmail,clientNationalId,clientOriginalNationalId))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client Data Updated')
        self.showAllClients()
        self.edit_client_name.setText('')
        self.edit_client_email.setText('')
        self.edit_client_nationalid.setText('')
        self.search_client_nationalid.setText('')

    def deleteClient(self):
        clientOriginalNationalId = self.search_client_nationalid.text()

        warningMessage = QMessageBox.warning(self,'Delete Client','are you sure you want to delete?',QMessageBox.Yes | QMessageBox.No)

        if warningMessage == QMessageBox.Yes:
            self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
            self.cur = self.db.cursor()

            sql = ''' DELETE FROM clients WHERE client_nationalid = %s '''
            self.cur.execute(sql,[(clientOriginalNationalId)])

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Client Deleted')
            self.edit_client_name.setText('')
            self.edit_client_email.setText('')
            self.edit_client_nationalid.setText('')
            self.search_client_nationalid.setText('')
            self.showAllClients()

    def searchClient(self):
        clientNationalId = self.search_client_nationalid.text()
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        sql = '''SELECT * FROM clients WHERE client_nationalid = %s'''
        self.cur.execute(sql,[(clientNationalId)])
        data = self.cur.fetchone()
        self.edit_client_name.setText(data[1])
        self.edit_client_email.setText(data[2])
        self.edit_client_nationalid.setText(data[3])

    ################################
    ############# Day to day operations #############

    def handelDayOperations(self):
        bookTitle = self.daytoday_booktitle.text()
        type = self.daytoday_type.currentText()
        days = self.daytoday_days.currentIndex() +1
        today_date = datetime.date.today()
        clientName = self.daytoday_clientname.text()
        to_date = today_date + datetime.timedelta(days=int(days))
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
            INSERT INTO dayoperations (book_name,type,days,date,client,to_date)
            VALUES (%s,%s,%s,%s,%s,%s)
        ''',(bookTitle,type,days,today_date,clientName,to_date))

        self.db.commit()
        self.statusBar().showMessage('New Operation Added')
        self.showAllOperations()

    def showAllOperations(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
            SELECT book_name,client,type,date,to_date FROM dayoperations
        ''')
        data = self.cur.fetchall()
        print(data)
        self.daytoday_tabwidget.setRowCount(0)
        self.daytoday_tabwidget.insertRow(0)

        for row,form in enumerate(data):
            for column,item in enumerate(form):
                self.daytoday_tabwidget.setItem(row,column,QTableWidgetItem(str(item)))
                column+=1
            row_position = self.daytoday_tabwidget.rowCount()
            self.daytoday_tabwidget.insertRow(row_position)


    ################################
    ############# Export Data #############

    def exportDayToDay(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
            SELECT book_name,client,type,date,to_date FROM dayoperations
        ''')
        data = self.cur.fetchall()
        wb = Workbook('day_operations.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'book title')
        sheet1.write(0, 1, 'client name')
        sheet1.write(0, 2, 'type')
        sheet1.write(0, 3, 'from - date')
        sheet1.write(0, 4, 'to - date')
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number,str(item))
                column_number += 1
            row_number += 1
        wb.close()
        self.statusBar().showMessage('Report Created Successfully')

    def exportBooks(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(
            ''' SELECT book_code,book_name,book_description,book_category,book_author,book_publisher,book_price FROM book ''')
        data = self.cur.fetchall()

        wb = Workbook('all_books.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Book Code')
        sheet1.write(0, 1, 'Book Name')
        sheet1.write(0, 2, 'Book Description')
        sheet1.write(0, 3, 'Book Category')
        sheet1.write(0, 4, 'Book Author')
        sheet1.write(0, 5, 'Book Publisher')
        sheet1.write(0, 6, 'Book Price')
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        wb.close()
        self.statusBar().showMessage('Report Created Successfully')

    def exportClients(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(
            ''' SELECT client_name , client_email , client_nationalid FROM clients ''')
        data = self.cur.fetchall()

        wb = Workbook('all_clients.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Client Name')
        sheet1.write(0, 1, 'Client Email')
        sheet1.write(0, 2, 'Client NationalId')
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        wb.close()
        self.statusBar().showMessage('Report Created Successfully')


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
