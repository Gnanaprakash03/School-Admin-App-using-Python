from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con

ui, _ =loadUiType('school.ui')

class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.create_db_and_table()
        self.tabWidget.setCurrentIndex(0)   #for displaying the first page of login
        self.tabWidget.tabBar().setVisible(False)   #to hide tab bar
        self.menubar.setVisible(False)    #to hide the menu bar
        self.b01.clicked.connect(self.login)
        
        # for tabs
        self.menu11.triggered.connect(self.show_add_new_student_tab)
        self.menu12.triggered.connect(self.edit_or_delete_student_tab)
        self.menu21.triggered.connect(self.marks_details_tab)
        self.menu31.triggered.connect(self.Attendance_details_tab)
        self.menu41.triggered.connect(self.Fees_details_tab)
        self.menu61.triggered.connect(QApplication.instance().quit)

        # for buttons
        self.b12.clicked.connect(self.save_student_details)
        self.b13.clicked.connect(self.edit_student_details)
        self.b14.clicked.connect(self.delete_student_details)
        self.b15.clicked.connect(self.save_marks_details)
        self.bge.clicked.connect(self.get_exams)
        self.b16.clicked.connect(self.get_marks)
        self.b17.clicked.connect(self.edit_marks_details)
        self.b18.clicked.connect(self.delete_marks_details)
        self.b19.clicked.connect(self.save_attendance_details)
        self.b20.clicked.connect(self.get_details)
        self.b21.clicked.connect(self.edit_attendance_details)
        self.b22.clicked.connect(self.delete_attendance_details)
        self.b23.clicked.connect(self.save_fees_details)
        self.b24.clicked.connect(self.edit_fees_details)
        self.b25.clicked.connect(self.delete_fees_details)

   ####### Login form #######

    def login(self):
        un=self.tb01.text()
        pw=self.tb02.text()
        if(un=="" and pw==""):  #username and password is fixed
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"School Management System", "Invalid admin login details, Try again !")
            self.l01.setText("Invalid admin login details, Try again !")

     ####### Add new student ####### 

    def show_add_new_student_tab(self):   #menu11 calling event
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()

    def fill_next_registration_number(self):
        try:
            rn=0
            qry="select * from student"
            result=self.sql(qry)
            # print(result)
            if result:
                for stud in result:
                    rn+=1
            self.tb11.setText(str(rn+1))
            self.tb12.setText('')
            self.tb13.setText('')
            self.tb14.setText('')
            self.mtb11.setText('')
            self.tb15.setText('')
            self.tb16.setText('')
        except con.Error as e:
            print("Error occured in select student reg number" ,e)

    def save_student_details(self):
        try:
            registration_number=self.tb11.text()
            full_name=self.tb12.text()
            gender=self.cb11.currentText()
            date_of_birth=self.tb13.text()
            age=self.tb14.text()
            address=self.mtb11.toPlainText()
            phone=self.tb15.text()
            email=self.tb16.text()
            standard=self.cb12.currentText()

            qry="insert into student (registration_number,full_name,gender,date_of_birth,age,address,phone_no,email,standard) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"   #%s-placeholders
            value=(registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard)    #variable names

            self.sql(qry,value)   

            self.l11.setText("Students details saved successfully")
            QMessageBox.information(self,"School management system","Students details added successfully!")
            self.fill_next_registration_number()
        except con.Error as e:
            print("Error in save student form" + str(e))
            self.l11.setText(self,"Error in save student form" + str(e))

    def edit_or_delete_student_tab(self):   #menu12 calling event
        self.tabWidget.setCurrentIndex(3)
        qry="select registration_number from student"
        reg_nos=self.getsql(qry)
        self.cb21.clear()
        for reg_no in reg_nos:
            self.cb21.addItem(reg_no[0])

        self.tb21.setText('')
        self.tb22.setText('')
        self.tb23.setText('')
        self.mtb21.setText('')
        self.tb24.setText('')
        self.tb25.setText('')

    def edit_student_details(self):
        try:
            registration_number=self.cb21.currentText()
            full_name=self.tb21.text()
            gender=self.cb22.currentText()
            date_of_birth=self.tb22.text()
            age=self.tb23.text()
            address=self.mtb21.toPlainText()
            phone=self.tb24.text()
            email=self.tb25.text()
            standard=self.cb26.currentText()

            qry="update student set full_name=%s,gender=%s,date_of_birth=%s,age=%s,address=%s,phone_no=%s,email=%s,standard=%s where registration_number = %s"   #%s-placeholders
            value=(full_name,gender,date_of_birth,age,address,phone,email,standard,registration_number)    #variable names
            self.sql(qry,value)
        
            self.l12.setText("Students details updated successfully")
            QMessageBox.information(self,"School management system","Students details updated successfully!")
            self.edit_or_delete_student_tab()
        except con.Error as e:
            print(str(e))
            # self.l12.setText("Error in update student form" + str(e))
            QMessageBox.information(self,"Error in update student form" + str(e))

    

    def delete_student_details(self):
        try:
            registration_number=self.cb21.currentText()
            qry="delete from student where registration_number = %s"   #%s-placeholders
            value=(registration_number,)    
            self.sql(qry,value)
            # self.l12.setText("Students details deleted successfully")
            QMessageBox.information(self,"School management system","Students details deleted successfully!")
            self.edit_or_delete_student_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in delete student form" + str(e))

    def marks_details_tab(self):
        self.tabWidget.setCurrentIndex(4)
        qry="select registration_number from student"
        reg_nos=self.getsql(qry)
        self.cb31.clear()
        for reg_no in reg_nos:
            self.cb31.addItem(reg_no[0])
        qry="select registration_number from marks group by registration_number"
        mark_regs=self.getsql(qry)
        self.cb32.clear()
        for mark_reg in mark_regs:
            self.cb32.addItem(mark_reg[0])
        self.tb31.setText('')
        self.tb32.setText('')
        self.tb33.setText('')
        self.tb34.setText('')
        self.tb35.setText('')
        self.tb36.setText('')
        self.cb33.clear()
        self.tb37.setText('')
        self.tb38.setText('')
        self.tb39.setText('')
        self.tb40.setText('')
        self.tb41.setText('')

    def save_marks_details(self):
        try:
            registration_number=self.cb31.currentText()
            exam_name=self.tb31.text()
            language=self.tb32.text()
            english=self.tb33.text()
            maths=self.tb34.text()
            science=self.tb35.text()
            social=self.tb36.text()

            qry="insert into marks values(%s,%s,%s,%s,%s,%s,%s)"
            value=(registration_number,exam_name,language,english,maths,science,social)    #variable names
            self.sql(qry,value)
        
            self.l13.setText("Students mark uploaded successfully")
            QMessageBox.information(self,"School management system","Students marks uploaded successfully!")
            self.marks_details_tab()
        except con.Error as e:
            print(str(e))
            # self.l12.setText("Error in update student form" + str(e))
            QMessageBox.information(self,"Error in add marks form" + str(e))


    def get_exams(self):
        try:
            registration_number=self.cb32.currentText()
            qry="Select exam_name from marks where registration_number = %s"
            value = (registration_number,)
            exam_names=self.getsql(qry,value)
            self.cb33.clear()
            for exam_name in exam_names:
                self.cb33.addItem(exam_name[0])
            self.show()
        except con.Error as e:
            print(str(e))
            # self.l12.setText("Error in update student form" + str(e))
            QMessageBox.information(self,"Error in add marks form" + str(e))

    def get_marks(self):
        try:
            registration_number=self.cb32.currentText()
            exam_name=self.cb33.currentText()
            qry = "select language,english,maths,science,social from marks where registration_number = %s and exam_name = %s"
            value = (registration_number,exam_name)
            marks=self.getsql(qry,value)
            self.tb37.setText(marks[0][0])
            self.tb38.setText(marks[0][1])
            self.tb39.setText(marks[0][2])
            self.tb40.setText(marks[0][3])
            self.tb41.setText(marks[0][4])

        except con.Error as e:
            print(str(e))
            # self.l12.setText("Error in update student form" + str(e))
            QMessageBox.information(self,"Error in getting marks" + str(e))

    def edit_marks_details(self):
        try:
            language=self.tb37.text()
            english=self.tb38.text()
            maths=self.tb39.text()
            science=self.tb40.text()
            social=self.tb41.text()

            registration_number=self.cb32.currentText()

            qry="update marks set language = %s,english = %s,maths = %s,science = %s,social = %s where registration_number = %s"   #%s-placeholders
            value=(language,english,maths,science,social,registration_number)
            self.sql(qry,value)

            self.l14.setText("Students marks updated successfully")
            QMessageBox.information(self,"School management system","Students marks updated successfully!")
            self.marks_details_tab()
            
        except con.Error as e:
            print(str(e))
            # self.l12.setText("Error in update student form" + str(e))
            QMessageBox.information(self,"Error in Updating marks" + str(e))

    def delete_marks_details(self):
        try:
            registration_number=self.cb32.currentText()
            qry="delete from marks where registration_number = %s"   #%s-placeholders
            value=(registration_number,)    
            self.sql(qry,value)
        
            # self.l12.setText("Students details deleted successfully")
            QMessageBox.information(self,"School management system","Marks details deleted successfully!")
            self.marks_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in delete marks" + str(e))



    def Attendance_details_tab(self):
        self.tabWidget.setCurrentIndex(5)
        qry="select registration_number from student"
        reg_nos=self.getsql(qry)
        self.cb41.clear()
        for reg_no in reg_nos:
            self.cb41.addItem(reg_no[0])

        qry="select registration_number from attendance group by registration_number"
        reg_nos=self.getsql(qry)
        self.cb42.clear()
        for reg_no in reg_nos:
            self.cb42.addItem(reg_no[0])

        qry="select date from attendance group by date"
        dates=self.getsql(qry)
        self.cb43.clear()
        for date in dates:
            self.cb43.addItem(date[0])

    def save_attendance_details(self):
        try:
            registration_number=self.cb41.currentText()
            date=self.tb51.text()
            morning=self.cb44.currentText()
            afternoon=self.cb45.currentText()
            qry="insert into attendance values(%s,%s,%s,%s)"
            value=(registration_number,str(date),morning,afternoon)    #variable names
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","Attendance details Saved successfully!")
            self.Attendance_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in Attendance form"+str(e))

    def get_details(self):
        try:
            registration_number=self.cb42.currentText()
            date=self.cb43.currentText()
            qry = "select morning,afternoon from attendance where registration_number = %s and date = %s"
            value = (registration_number,date)
            datas=self.getsql(qry,value)
            self.tb54.setText(datas[0][0])
            self.tb55.setText(datas[0][1])

        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in get details "+str(e))

    def edit_attendance_details(self):
        try:
            registration_number=self.cb42.currentText()
            date=self.cb43.currentText()
            morning=self.tb54.text()
            afternoon=self.tb55.text()
            qry="update attendance set morning =%s,afternoon=%s where registration_number = %s and date = %s"   #%s-placeholders
            value=(morning,afternoon,registration_number,date)    #variable names
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","School attedance details updated successfully")
            self.Attendance_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in edit attendance detail")

    def delete_attendance_details(self):
        try:
            registration_number=self.cb42.currentText()
            date = self.cb43.currentText()
            qry="delete from attendance where registration_number = %s and date = %s"
            value = (registration_number,date)
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","School attedance detail deleted successfully")
            self.Attendance_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in delete attendance detail")

    def Fees_details_tab(self):
        self.tabWidget.setCurrentIndex(6)
        rn=0
        qry="select receipt_number from fees"
        result=self.getsql(qry)
        if result:
            for rec in result:
                rn+=1
        self.tb61.setText(str(rn+1))
        qry="select registration_number from student"
        reg_nos=self.getsql(qry)
        self.cb51.clear()
        for reg_no in reg_nos:
            self.cb51.addItem(reg_no[0])
        self.tb62.setText("")
        self.tb63.setText("")
        self.tb64.setText("")

        qry="select receipt_number from fees"
        reg_nos=self.getsql(qry)
        self.cb53.clear()
        for reg_no in reg_nos:
            self.cb53.addItem(reg_no[0])
        qry="select registration_number from fees group by registration_number"
        reg_nos=self.getsql(qry)
        self.cb52.clear()
        for reg_no in reg_nos:
            self.cb52.addItem(reg_no[0])
        self.tb66.setText("")
        self.tb67.setText("")
        self.tb68.setText("")

    def save_fees_details(self):
        try:
            receipt_number=self.cb61.currentText()
            registration_number=self.cb51.currentText()
            payment_reason=self.tb62.text()
            amount=self.tb63.text()
            date=self.tb64.text()
            qry=("insert into fees values(%s,%s,%s,%s,%s)")
            value=(receipt_number,registration_number,payment_reason,amount,date)
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","Fees details Saved successfully!")
            self.Fees_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in fees form"+str(e))
    
    def edit_fees_details(self):
        try:
            receipt_no=self.cb53.currentText()
            registration_number=self.cb52.currentText()
            payment_reason=self.tb66.text()
            amount=self.tb67.text()
            date=self.tb68.text()
            qry="update fees set payment_reason = %s,amount= %s,date= %s where receipt_number = %s and registration_number = %s"
            value = (receipt_no,registration_number,payment_reason,amount,date)
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","School fees details updated successfully")
            self.Fees_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in fees edit form"+str(e))

    def delete_fees_details(self):
        try:
            receipt_no=self.cb53.currentText()
            registration_number=self.cb52.currentText()
            qry='delete from fees where receipt_number= %s and registration_number = %s'
            value = (receipt_no,registration_number)
            self.sql(qry,value)
            QMessageBox.information(self,"School management system","School fees details delete successfully")
            self.Fees_details_tab()
        except con.Error as e:
            print(str(e))
            QMessageBox.information(self,"Error in fees delete form"+str(e))

    def sql(self,qry,value=list()):
        f = open("MySql_Log.txt","r")
        mydb=con.connect(host="localhost",user=f.readline(),password=f.readline(),db="school")
        cursor=mydb.cursor()
        cursor.execute(qry,value)
        mydb.commit()
        f.close()

    def getsql(self,qry,value=list()):
        f = open("MySql_Log.txt","r")
        mydb=con.connect(host="localhost",user=f.readline(),password=f.readline(),db="school")
        cursor=mydb.cursor()
        cursor.execute(qry,value)
        result=cursor.fetchall()
        f.close()
        return result
    
    def create_db_and_table(self):
        qry='CREATE DATABASE IF NOT EXISTS school'
        self.sql(qry)
        qry='CREATE TABLE IF NOT EXISTS student(registration_number varchar(10) primary key,full_name varchar(50),gender varchar(10),date_of_birth varchar(10),age varchar(3),address varchar(100),phone_no varchar(10),email varchar(30),standard varchar(20))'
        self.sql(qry)
        qry='CREATE TABLE IF NOT EXISTS marks(registration_number varchar(10) primary key,exam_name varchar(30),language varchar(30),english varchar(30),maths varchar(30),science varchar(30),social varchar(30))'
        self.sql(qry)
        qry='CREATE TABLE IF NOT EXISTS attendance(registration_number varchar(10),date varchar(15),Morning varchar(10),Afternoon varchar(10))'
        self.sql(qry)
        qry='CREATE TABLE IF NOT EXISTS fees(receipt_number varchar(30),registration_number varchar(10),payment_reason varchar(50),Amount varchar(15),date varchar(15))'
        self.sql(qry)

def main():
     app = QApplication(sys.argv)
     window = MainApp()
     window.show()
     app.exec_()

if __name__ == '__main__':
    main()