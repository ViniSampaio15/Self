from re import I
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from numpy import double
import pandas as pd
import psycopg2
from psycopg2 import sql
from configparser import ConfigParser



class MainWindow(QDialog):
    def __init__(self, data, dbCursor):
        super(MainWindow, self).__init__()
        loadUi("main.ui",self)
        self.data = data
        self.cursor = dbCursor
        self.listaCompras.setColumnWidth(0,100)
        self.listaCompras.setColumnWidth(1,400)
        self.listaCompras.setColumnWidth(2,100)
        print(len(data))
        self.loaddata()
        self.lineEdit.setText('teste')
        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit.setFocus()
        self.lineEdit = MyLineEdit(self.lineEdit)


    def loaddata(self):
        #sampleProducts =[{"ID":123456,"Produto":"Alcool Gel","Preço":10.1}]
        #df = pd.DataFrame(sampleProducts)
        row=0
        print(len(self.data))
        self.valor.setText(str("{:.2f}".format(self.data["Preço"].sum())).replace(".", ","))
        self.listaCompras.setRowCount(len(self.data ))
        if len(self.data) > 0:
            for index in self.data.index:
                self.listaCompras.setItem(row, 0, QtWidgets.QTableWidgetItem(str(self.data["ID"][index])))
                self.listaCompras.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.data["Produto"][index])))
                self.listaCompras.setItem(row, 2, QtWidgets.QTableWidgetItem(str("{:.2f}".format(self.data["Preço"][index]).replace(".", ","))))
                row=row+1

    def keyPressEvent(self, event):
        print('pressed from myDialog: ', event.key())
        if (event.key() == 16777220) or (event.key() == 16777221):
            #print ("Enter Pressed")
            texto = self.lineEdit.text()
            #print(texto)
            query = sql.SQL("SELECT item.preco_temp, item.descricao FROM item WHERE item.codigo_barra LIKE '%s';" % (texto))
            #print(query)
            self.cursor.execute(query, texto)
            result = self.cursor.fetchall()
            #print(type(result))


            try:
               #print(result)
               self.data  = self.data.append({"ID": texto,
                "Produto": result[0][1],
                "Preço": float(result[0][0])}, ignore_index=True)
               self.loaddata()
            except:
                print("produto não registrado, adicione manualmente")
            
            
            self.lineEdit.setText("")

        event.accept()
    
    def focusOutEvent(self, event):
        self.lineEdit.setFocus(True)
        #print("focus out")

class MyLineEdit(QtWidgets.QLineEdit):

    def focusOutEvent(self, event):
        #print ('focus out event')
        # do custom stuff
        super(MyLineEdit, self).setFocus()
        super(MyLineEdit, self).focusOutEvent(event)


# main
column_names = ["ID", "Produto", "Preço"]

df = pd.DataFrame(columns = column_names)

df = df.append({"ID": "texto",
            "Produto": "teste",
            "Preço": 10.1000}, ignore_index=True)

df = df.append({"ID": "texto2",
            "Produto": "teste2",
            "Preço": 102.1000}, ignore_index=True)

conn = psycopg2.connect(
    host="localhost",
    port= 5434,
    database="banco001",
    user="postgres",
    password="1",
    options="-c search_path=public")
cur = conn.cursor()

app = QApplication(sys.argv)
mainwindow = MainWindow(df, cur)
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.resize(1024, 720)
#widget.showFullScreen()
widget.show()
mainwindow.lineEdit.setFocus()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")