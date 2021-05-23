from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QPoint, QTimer, QTime, QDateTime

import sys
import os
import datetime
import sqlite3
import time


global conn
conn = sqlite3.connect('ProjectNimarkoh-Test.db')

global cur
cur = conn.cursor()

#TskQuery = """SELECT """
##Query must be dynamically constructed
##You can have multiple hardcoded queries that are switched between
##That shit won't always work well though



g=0
#This value counts the number of far deadline tasks present


dayz = 30
#Default value for the deadline parameters



CrntD = datetime.datetime.now()
format_str = "%d/%m/%y"
CD = str(CrntD.day)+"/"+str(CrntD.month)+"/"+str(CrntD.year)[2]+str(CrntD.year)[3]
#print(CD)
datetime_obj = datetime.datetime.strptime(CD, format_str)
#print(datetime_obj)
crntD = datetime_obj.date()
#print(crntD)
#Current Date as a datetime object
#crntD should be used everywhere

    
class Dive:
    #Database searching class   ADD DRIB AND PrioCount ass classmethods!!!
    def PrioCount():
        query = """SELECT Priority, GoalID FROM PNTask WHERE Priority>4;"""
        q=cur.execute(query)
        #query
        a=cursor.fetchall()
        #mutable & callable results of the query
        f=0
        for row in q:
            f=f+1
        #print(f)
        #Count number of high priority tasks
        query2 = """SELECT Priority, GoalID FROM PNTask WHERE Priority<4;"""
        q2=cur.execute(query2)
        g=0
        for row in q2:
            g=g+1
        #print(g)
        g2 = (f/4)*3

        if g >= g2:
            #Populate 3 slots with low prio tasks
            taskbox = QGroupBox("  ")   #
            #return taskbox
            pass
        else:
            #Populate all with high prio tasks
            #return taskbox
            pass
            

        
    def DRIB(QryRslt):
        L=0
    #This value is a binary switch that will allow for the while loop to end
        while L==0:
        
            t=0
            #Counts the number of close DL tasks on each loop
            global poop
            poop=[]
            #Stores the close DL tasks on each loop
            for row in QryRslt:
                
                    global dayz
                    DL=row[1]
                    #print(DL)
                    #print(DL,"Processed")

                    datetime_obj2 = datetime.datetime.strptime(DL, format_str)
                    #print(datetime_obj2)
                    DL2= datetime_obj2.date()
                    #print(DL2)
                    #convert DL to datetime object

                    CMPR = DL2-crntD
                    CMPR1 = CMPR.days    #Convert the difference into days
                    #print("This is t:"+str(t))
                    #print(CMPR1)
                    #compare the two values
                    #print(CMPR)

                    if CMPR1 >dayz:   #If the difference in days is greater than the threshold previously set, do the following
                        #print("don't worry bro")
                        

                        if row[3]==1: #SETS THE Overlay column to 0, indicating that the task is no longer on display
                            TKN = row[0]
                            sql= "UPDATE PNTask SET OVR=0 WHERE TaskName=?"
                            cur.execute(sql, (TKN,))
                            conn.commit()
                        
                    if CMPR1 < dayz and row[3]==0:
                        #print("worry.")
                        t=t+1
                        
                        #Add the tasks to the task list array (A)
                        
##                        #SETS THE Overlay column to 1, indicating that the task is on the overlay
##                        TKN = row[0]
##                        sql= "UPDATE PNTask SET OVR=1 WHERE TaskName=?"
##                        cur.execute(sql, (TKN,))
##                        conn.commit()
                        #Premature OVR changing means that it will treat any task that fits the above criteria as being on display, this is not desired
                        #print(row)
                        poop.append(row[0:5])
                        #print(poop)

                    """else:
                        t=t+1
                        print(t)"""

                        
                           
                            
                                               
            if t>=3:
                L=1
                #print(poop)
                
                
            else:
                dayz=dayz*2

            return poop
    
    def getpoop():
        return poop

    def OVR_Reset():
        sql= "UPDATE PNTask SET OVR=0 WHERE OVR=1"
        cur.execute(sql)
        conn.commit()
    


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createTimeBox(), 0, 0)
        #LAYOUT CONDITIONS FOR EACH GENERATION FUNCTION BEING USED
        #if x=0:
            #pass

        #else:
            #pass
        #################################################################
            
        grid.addWidget(self.createDLLo(), 1, 0)
        grid.addWidget(self.createDLHi(), 0, 1)
        grid.addWidget(self.createDLLo(), 1, 1)
        
        self.AddTsk=QPushButton()
        self.AddTsk.setIcon(QIcon('plus-icon.png'))
        self.AddTsk.clicked.connect(self.addTask)   #window2
        self.AddTsk.setGeometry(0, 0, 10, 10)
        grid.addWidget(self.AddTsk, 2,0)

        self.ViewTsk=QPushButton()
        self.ViewTsk.setIcon(QIcon('view-icon.png'))
        self.ViewTsk.clicked.connect(self.viewTask)
        self.ViewTsk.setGeometry(0, 0, 10, 10)
        grid.addWidget(self.ViewTsk, 2, 1)

        
        self.setLayout(grid)


        Dive.OVR_Reset()

        self.setWindowTitle("Nimarkoh V2")
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.setWindowFlags(flags)

        sizegrip = QSizeGrip(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 650, 400)


    
    def addTask(self):
        self.w2=TaskForm()
        self.w2.show()
        #self.hide()

    def viewTask(self):
        self.w3=TaskView()
        self.w3.show()
        #self.hide()
        
    def mousePressEvent(self, event):
         self.oldPos = event.globalPos()
         #print("poop.")

    def mouseMoveEvent(self, event):
            delta = QPoint (event.globalPos() - self.oldPos)
            #print(delta)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
    
    def createTimeBox(self): #Unique in that it must constantly be refreshed
        timebox = QGroupBox("Calendar")
        timebox.setStyleSheet("color: rgb(255, 255, 255);")
        timebox.setFont(QFont('Yu Gothic Light', 10))

        
        t= datetime.datetime.now()
        t2= str(datetime.datetime.now().time())
        t3 = str(t.day)+" / "+str(t.month)+" / "+str(t.year)[0]+str(t.year)[1]

        Time =QLabel()
        Time.setStyleSheet("color: rgb(255, 255, 255);")
        Time.setFont(QFont('Yu Gothic Light', 36, 63))
        Date =QLabel()
        Date.setStyleSheet("color: rgb(255, 255, 255);")
        Date.setText(t3)
        Date.setFont(QFont('Yu Gothic Light', 30, 63))
        
        #Time.setText(t2[0:5])

        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('hh:mm')#:ss dddd')
        Time.setText(timeDisplay)

        
        
        
        """ def showTime():
            crntT=QTime.currentTime()
            label_time=crntT.toString('hh:mm:ss')
            Time.setText(label_time)
            
        timer=QTimer()
        timer.timeout.connect(showTime)
        timer.start(1000)"""
        
        

        vbox = QVBoxLayout()
        #vbox.addWidget(AddTsk)
        vbox.addWidget(Time)
        vbox.addWidget(Date)
        timebox.setLayout(vbox)

        return timebox

    def createDLHi(Self): #NOW FUNCTIONAL, NOW ADD A TASK DESCRIPTION COLUMN TO THE DATABASE    ##MISSION ACCOMPLISHED
        query = """SELECT TaskName, TaskDL, Priority, OVR, TaskDesc FROM PNTask WHERE Priority>4;"""
        q=cur.execute(query)
        a=cur.fetchall()
        #print(a)
        

        
        #activateDive=Dive.getpoop()
        #activateDive
        #poop is returned anyway

        

        try:
            Dive.DRIB(a)
            #print(poop)
            scoop=poop[0]
            #print(scoop)

            sql= "UPDATE PNTask SET OVR=1 WHERE TaskName=?"
            cur.execute(sql,(scoop[0],))
            conn.commit()
   
            groupBox = QGroupBox(scoop[0])
            groupBox.setStyleSheet("color: rgb(255, 255, 255);")
            groupBox.setFont(QFont('Yu Gothic Light', 10))
            
            tskPrt=QLabel("High")
            tskPrt.setStyleSheet("color: rgb(255, 255, 255);")
            tskPrt.setFont(QFont('Yu Gothic Light', 36, 55))
                
            tskDesc=QLabel(scoop[4])
            tskDesc.setStyleSheet("color: rgb(255, 255, 255);")
            tskDesc.setFont(QFont('Yu Gothic Light', 15, 25))
            
            tskDL=QLabel(scoop[1])
            tskDL.setStyleSheet("color: rgb(255, 255, 255);")
            tskDL.setFont(QFont('Yu Gothic Light', 20, 45))

            vbox= QVBoxLayout()
            vbox.addWidget(tskPrt)
            vbox.addWidget(tskDesc)
            vbox.addWidget(tskDL)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            return groupBox
        
        except IndexError:
            sql= "UPDATE PNTask SET OVR=0 WHERE OVR=1"
            cur.execute(sql)
            conn.commit()

    

    def createDLLo(Self):
        query = """SELECT TaskName, TaskDL, Priority, OVR, TaskDesc FROM PNTask WHERE Priority<=4;"""
        q=cur.execute(query)
        a=cur.fetchall()
        

        Dive.DRIB(a)
        activateDive=Dive.getpoop()
        activateDive
        
            
        try:
            scoop=poop[0]
            #print(scoop)
            
            sql= "UPDATE PNTask SET OVR=1 WHERE TaskName=?"
            cur.execute(sql,(scoop[0],))
            conn.commit()
            
            groupBox = QGroupBox(scoop[0])
            groupBox.setStyleSheet("color: rgb(255, 255, 255);")
            groupBox.setFont(QFont('Yu Gothic Light', 10))
            
            
            tskPrt=QLabel("Low")
            tskPrt.setStyleSheet("color: rgb(255, 255, 255);")
            tskPrt.setFont(QFont('Yu Gothic Light', 36, 47))
                
            tskDesc=QLabel(scoop[4])
            tskDesc.setStyleSheet("color: rgb(255, 255, 255);")
            tskDesc.setFont(QFont('Yu Gothic Light', 15, 25))
            
            tskDL=QLabel(scoop[1])
            tskDL.setStyleSheet("color: rgb(255, 255, 255);")
            tskDL.setFont(QFont('Yu Gothic Light', 20, 45))

            vbox= QVBoxLayout()
            vbox.addWidget(tskPrt)
            vbox.addWidget(tskDesc)
            vbox.addWidget(tskDL)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            return groupBox
        
        except IndexError:
            sql= "UPDATE PNTask SET OVR=0 WHERE OVR=1"
            cur.execute(sql)
            conn.commit()

        
class TaskForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test')
        self.resize(200, 150)

        layout=QGridLayout()

        label_TN=QLabel('<font size="4"> Task Name: </font>')
        self.lineEdit_TN = QLineEdit()
        self.lineEdit_TN.setPlaceholderText('Please enter the name of the task')
        layout.addWidget(label_TN, 0, 0)
        layout.addWidget(self.lineEdit_TN, 0, 1)

        label_TD=QLabel('<font size="4"> Task Description: </font>')
        self.lineEdit_TD= QLineEdit()
        self.lineEdit_TD.setPlaceholderText('Please enter a brief description of the task')
        layout.addWidget(label_TD, 1, 0)
        layout.addWidget(self.lineEdit_TD, 1, 1)

        label_DL=QLabel('<font size="4"> Deadline: </font>')
        self.lineEdit_DL= QLineEdit()
        self.lineEdit_DL.setPlaceholderText('Please enter the deadline of the task')
        layout.addWidget(label_DL, 2, 0)
        layout.addWidget(self.lineEdit_DL, 2, 1)

        label_P=QLabel('<font size="4"> Priority Level: </font>')
        self.lineEdit_P= QLineEdit()
        self.lineEdit_P.setPlaceholderText('Please enter the priority level of the task (1-7)')
        layout.addWidget(label_P, 3, 0)
        layout.addWidget(self.lineEdit_P, 3, 1)

        button_Send = QPushButton('Enter')
        button_Send.clicked.connect(self.Send)
        layout.addWidget(button_Send, 4, 0)
        # button_login.clicked.connect()

        """flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)"""

        
        self.setLayout(layout)
        

    def Send(self):
        sql="INSERT INTO PNTask (TaskName, TaskDL, Priority, TaskDesc) VALUES(?,?,?,?);"
        A=self.lineEdit_TN.text()
        B=self.lineEdit_DL.text()
        C=int(self.lineEdit_P.text())
        D=self.lineEdit_TD.text()
        print(A,B,C,D)
        cur.execute(sql,(A, B, C, D))

        PopUpDlg=QMessageBox()
        PopUpDlg.setWindowTitle("Add Task")
        PopUpDlg.setText('Task Created')
        PopUpDlg.setInformativeText('A new task was created')
        PopUpDlg.exec_()
        
        conn.commit()
        
    """loop = 1
    while loop ==1:  
            Time.setText(t2)
            Date.setText(t3)"""
        
        
        
    #ATTEMPT AT TIME/DATE UPDATER
    ##TRY DEFINING AN UPDATE FUNCTION, THEN CALL UPON IT REGULARLY

    
class TaskView(QWidget):
    def __init__(self):
        super().__init__()
        grid=QGridLayout()
        grid.setColumnStretch
        self.setWindowTitle('Task Viewer')
        self.resize(400, 300)

        query="SELECT * FROM PNTask"    #SELECT ALL TASKS
        cur.execute(query)            #execute that shit boi
        qs2=cur.fetchall()                  #store 'em in a variable called a
        #print(a) #a is empty
                 #a is no longer empty
        
        x=0
        y=0

        

        def Edit(TID):
            #Initiate Task Form and set the placeholder text to the info from the record
            pass
            
        
        
        for row in qs2:      #For all tasks in the database
            
            #groupBox=QGroupBox(row[0])
            if row[2] >3:
                groupBox=QGroupBox("High Priority")
            else:
                groupBox=QGroupBox("Low Priority")

                
            print(row)
            TName=QLabel(row[0])
            print(row[0])
            TDL=QLabel("Deadline: "+row[1])
            TP=QLabel(row[6])
            TDlt=QPushButton()
            TEdit=QPushButton()



            def Delete(TID): #Implemented, REQUIRES CLEAN-UP OR REFRESH BUTTON
                sql= "DELETE FROM PNTask WHERE TaskID=?"
                cur.execute(sql, (TID,))
                conn.commit()



            TDlt.setIcon(QIcon('delete-icon.png'))
            TDlt.clicked.connect(lambda *args: Delete(row[3]))
            
            TEdit.setIcon(QIcon('edit-icon.png'))
            #TEdit.clicked.connect()

            vbox=QVBoxLayout()
            groupBox.setLayout(vbox)

            
            #print("hi")
            vbox.addWidget(TName)
            vbox.addWidget(TDL)
            vbox.addWidget(TP)
            vbox.addWidget(TDlt)
            #vbox.addWidget(TEdit)
            #vbox.addStretch()
            #print("hi")
            

            grid.addWidget(groupBox, y, x)
            print(y, x)

            if (x%2)== 0 and x!=0:
                x = 0
                y=y+1
                
            else:
                x=x+1
                
            

        """def CreateRecord():
            for row in qs2:
                groupBox=QGroupBox(row[0])
                print(row[0])
                TDL=QLabel(row[1])
                TP=QLabel(row[2])

                vbox=QVBoxlayout()
                groupBox.setLayout(vbox)
                vbox.addWidget(TName)
                vbox.addWidget(TDL)
                vbox.addWidget(TP)
                

                grid.addWidget(groupBox, y, x)

            if (n%3)== 0:
                x = 0
                y=+1
                
            else:
                x=+1"""
                
            
                

        self.setLayout(grid)
        

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
    
    
    
    """def updateTime():
        t= datetime.datetime.now()
        t2= str(datetime.datetime.now().time())
        t3= str(datetime.datetime.now().date())
        
        Window.timebox.Time.setText(t2)
        Window.timebox.Date.setText(t3)
    UPDATE TIME HERE"""
    
   #loop=5

    """def reload():
        print('hi')
        clock.hide()
        sys.exit(app.exec_())
        app.quit()
        clock.show()
        sys.exit(app.exec_())
        
        
        
    while loop==5:
        timer=QTimer()
        timer.start(5000)
        timer.timeout.connect(reload)
        print("reloaded")"""
        
        

    
        

    #timer = QtCore.QTimer()
    #timer.timeout.connect(updateTime)
    #timer.start(60000)
    
    #sys.exit(app.exec_())

