from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType
ui,_ = loadUiType('library.ui')


class MainApp(QMainWindow , ui):
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

    def Open_Users_Tab(self):
        self.tabwidget.setCurrentIndex(2)

    def Open_Settings_Tab(self):
        self.tabwidget.setCurrentIndex(3)

    ################################
    ############# Books #############
    def AddNewBook(self):
        self.db = MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur = self.db.cursor()
        book_title = self.edt_book_title.text()
        book_code = self.edt_book_code.text()
        book_price = self.edt_book_price.text()
        book_category = self.combo_category.CurrentText()
        book_author = self.combo_author.CurrentText()
        book_publisher = self.combo_publisher.CurrentText()
    def SearchBooks(self):
        pass

    def EditBooks(self):
        pass

    def DeleteBooks(self):
        pass

    ################################
    ############# Users #############
    def AddNewUser(self):
        pass

    def Login(self):
        pass

    def EditUser(self):
        pass

    ################################
    ############# Settings #############
    def AddCategory(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()
        category_name = self.add_category_edt_name.text()

        self.cur.execute('''
            INSERT INTO  category (category_name) VALUES (%s)
        ''',(category_name,))
        self.db.commit()
        self.statusBar().showMessage('new category added')
        self.add_category_edt_name.setText('')
        self.ShowCategory()

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
                    self.category_tabwidget.setItem(row,column,QTableWidgetItem(str(item)))
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

        for category in data:
            self.combo_book_category.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()

        for author in data:
            self.combo_book_author.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()

        for publisher in data:
            self.combo_book_publisher.addItem(publisher[0])

def main():
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()

if __name__ == '__main__':
    main()