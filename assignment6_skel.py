import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt


class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        # QLineEdit : 값을 입력
        self.lneName = QLineEdit()
        self.lneAge = QLineEdit()
        self.lneScore = QLineEdit()
        self.lneAmount = QLineEdit()

         # QTextEdit : 결과 화면
        self.txtResult = QTextEdit()

        # QComboBox : 정렬 키
        self.comKey = QComboBox()
        self.comKey.addItem("Name")
        self.comKey.addItem("Age")
        self.comKey.addItem("Score")
        self.initUI() 
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Assignment6')    


    
        # QLabel : 글자
        lblName = QLabel('Name:')
        lblAge = QLabel('Age:')
        lblScore = QLabel('Score:')
        lblAmount = QLabel('Amount:')
        lblKey = QLabel('Key:')
        lblResult = QLabel('Result:')

        
        

        #QPushButton : 명령
        btnAdd = QPushButton("Add", self)
        btnDel = QPushButton("Del", self)
        btnFind = QPushButton("Find", self)
        btnInc = QPushButton("Inc", self)
        btnShow = QPushButton("Show", self)

        # btn.clicked.connect() 메소드
        btnAdd.clicked.connect(self.AddClicked)
        btnDel.clicked.connect(self.DelClicked)
        btnFind.clicked.connect(self.FindClicked)
        btnInc.clicked.connect(self.IncClicked)
        btnShow.clicked.connect(self.ShowClicked)



        #첫째줄
        hbox1 = QHBoxLayout() 

        hbox1.addWidget(lblName)
        hbox1.addWidget(self.lneName)
        hbox1.addWidget(lblAge)
        hbox1.addWidget(self.lneAge)
        hbox1.addWidget(lblScore)
        hbox1.addWidget(self.lneScore)

        #둘째줄
        hbox2 = QHBoxLayout()

        hbox2.addStretch(1)
        hbox2.addWidget(lblAmount)
        hbox2.addWidget(self.lneAmount)
        hbox2.addWidget(lblKey)
        hbox2.addWidget(self.comKey)

        #셋째줄
        hbox3 = QHBoxLayout()

        hbox3.addStretch(1)
        hbox3.addWidget(btnAdd)
        hbox3.addWidget(btnDel)
        hbox3.addWidget(btnFind)
        hbox3.addWidget(btnInc)
        hbox3.addWidget(btnShow)

        vbox = QVBoxLayout()

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(lblResult)
        vbox.addWidget(self.txtResult)

        self.setLayout(vbox)
        self.show()



    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self): # 파일을 읽음
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()


    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()



    def AddClicked(self):
        record = {'Name': self.lneName.text(), 'Age' : int(self.lneAge.text()), 'Score' : int(self.lneScore.text())}
        self.scoredb.append(record)
        self.showScoreDB()   

    def DelClicked(self):
        for p in self.scoredb:
                if p['Name'] == self.lneName.text():
                    self.scoredb.remove(p)
        self.showScoreDB()

    def FindClicked(self):
        resultText = ''
        for p in self.scoredb:
            if p['Name'] == self.lneName.text():
                for attr in sorted(p):
                    resultText += attr + "=" + str(p[attr]) + "    "
                resultText += "\n"
        self.txtResult.setText(resultText)

    def IncClicked(self):
        for p in self.scoredb:
                if p['Name'] == self.lneName.text():
                    p['Score'] = int(p['Score']) + int(self.lneAmount.text())
        self.showScoreDB()

    def ShowClicked(self):
        self.showScoreDB()
  

    def showScoreDB(self): # 정렬
        comKey_text = self.comKey.currentText()
        for p in sorted(self.scoredb, key=lambda person: person[comKey_text]): #sorted <-정렬된 결과를 반환. 변형 없음
            resultText = ""
            for attr in sorted(p):
                resultText += attr + "=" + str(p[attr]) + " "
            self.txtResult.append(resultText)


	


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

