

import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt


class ScoreDB(QWidget):

    def __init__(self): # __init__ 머선 뜻? 초기화?
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        nameLabel = QLabel("Name:", self) 
        self.nameEdit = QLineEdit(self) # 나중에 사용할 거라 self 붙임
        ageLabel = QLabel("Age:",self)
        self.ageEdit = QLineEdit(self)
        scoreLabel = QLineEdit("Score:",self)
        self.scoreEdit = QLineEdit(self)

        # 수평
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(nameLabel)
        hbox1.addWidget(self.nameEdit)
        hbox1.addWidget(ageLabel)
        hbox1.addWidget(self.ageEdit)
        hbox1.addWidget(scoreLabel)
        hbox1.addWidget(self.scoreEdit)

        # 두 번째 줄 점수 올리기
        amountLabel = QLabel("Amount:",self)
        self.amountEdit = QLineEdit(self)

        keyLabel = QLabel("Key:",self)
        self.keyCombo = QComboBox(self)

        self.keyCombo.addItem("Name")
        self.keyCombo.addItem("Age")
        self.keyCombo.addItem("Score")
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(amountLabel)
        hbox2.addWidget(self.amountEdit)
        hbox2.addWidget(keyLabel)
        hbox2.addWidget(self.keyCombo)

        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addClicked) # 사용자 정의 함수
        delButton = QPushButton("Del")
        delButton.clicked.connect(self.delClicked)
        findButton = QPushButton("Find")
        findButton.clicked.connect(self.findClicked)
        incButton = QPushButton("Inc")
        incButton.clicked.connect(self.incClicked)
        showButton = QPushButton("Show")
        showButton.clicked.connect(self.showClicked)
        
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(addButton)
        hbox3.addWidget(delButton)
        hbox3.addWidget(findButton)
        hbox3.addWidget(incButton)
        hbox3.addWidget(showButton)

        resultLabel = QLabel("Result:", self)
        self.resultEdit = QTextEdit()

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(resultLabel)
        vbox.addWidget(self.resultEdit)

        self.setLayout(vbox) # 윈도우 창에다가 출력


        self.setGeometry(300, 300, 500, 250) 
        self.setWindowTitle('Assignment6')    
        self.show()
    
    def showClicked(self):
        sender = self.sender()
        self.showScoreDB() # showScoreDB 를 불러오기만 함

    def findClicked(self):
        sender = self.sender()
        findKey = self.nameEdit.text() # findKey 에 전달함 입력된 이름
        self.nameEdit.clear()
        self.findScoreDB(findKey)

    def delClicked(self):
        sender = self.sender()
        delKey = self.nameEdit.text() # 이름으로 찾을 거니까, 입력된 이름을 delKey 에 저장
        self.nameEdit.clear()
        self.scoredb[:] = [x for x in self.scoredb if x['Name'] != delKey] 
        self.showScoreDB()

    def incClicked(self):
        sender = self.sender()
        incKey = self.nameEdit.text()
        amount = self.amountEdit.text()
        amount = int(amount) if amount else 0 # amount 값이 0 이 아니면(값이 있다면)
        self.nameEdit.clear()
        self.amountEdit.clear()
        self.incScoreDB(incKey, amount)
        self.showScoreDB()

    def addClicked(self):
        sender = self.sender()
        name = self.nameEdit.text()
        age = int(self.ageEdit.text()) # 나이.점수는 정수로 변환 필요
        score = int(self.scoreEdit.text())
        self.nameEdit.clear()
        self.ageEdit.clear()
        self.scoreEdit.clear()

        record = {'Name':name, 'Age':age, 'Score': score}
        self.scoredb += [record]
        self.showScoreDB()



    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH) # pickle 모듈 이용
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

    def showScoreDB(self):
        keyName = str(self.keyCombo.currentText()) # 현재 어떤 항목이 선택되어 이쓴지 학목 가져와서
        msg = " " # 빈 문자열
        keyName = "Name" if not keyName else keyName # 기본값으로는 Name

        for p in sorted(self.scoredb, key = lambda person: person[keyName]):
            for attr in sorted(p):
                msg += attr + ":" + str(p[attr]) +"     \t"
            msg += "\n"
        
        self.resultEdit.setText(msg)

    def findScoreDB(self, keyName):
        msg = ""
        for p in self.scoredb :
            if p['Name'] == keyName:
                for attr in sorted(p):
                    msg += attr + ":" + str(p[attr]) + "     \t"
                    msg += "\n"
        
        self.resultEdit.setText(msg)

    def incScoreDB(self, name, amount):
        for p in self.scoredb :
            if p['Name'] == name:
                p['Score'] += amount

                


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

