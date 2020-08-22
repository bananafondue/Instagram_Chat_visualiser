
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from PyQt5.QtWidgets import QMessageBox


timesrun = 0
timesrun2 = 0

class Ui_MainWindow(object):
    def Search_String(self, tofind):
        with open(self.path, encoding="utf8") as f:
            data = json.load(f)

        counttofindname1 = 0
        counttofindname2 = 0
        Name1 = self.Name1.text()
        Name2 = self.Name2.text()
        req = [Name1, Name2]
        for item in data:
            if item['participants'] == req:
                for conv in item['conversation']:
                    if 'text' in conv.keys():
                        search = conv['text']
                        if search == None:
                            continue
                        numberfound = search.lower().count(tofind.lower())
                        if conv['sender'] == Name1:
                            counttofindname1 += numberfound
                        elif conv['sender'] == Name2:
                            counttofindname2 += numberfound

        return counttofindname1, counttofindname2

    def count_messages(self):
        with open(self.path, encoding="utf8") as f:
            data = json.load(f)

        countmsgsname1 = 0
        countmsgsname2 = 0
        Name1 = self.Name1.text()
        Name2 = self.Name2.text()
        req = [Name1, Name2]
        for item in data:
            if item['participants'] == req:
                for conv in item['conversation']:
                    if conv['sender'] == Name1:
                        countmsgsname1 += 1
                    elif conv['sender'] == Name2:
                        countmsgsname2 += 1

        return countmsgsname1, countmsgsname2

    def wordcount(self):
        with open(self.path, encoding="utf8") as f:
            data = json.load(f)

        totalwordcount = 0
        wordcount1 = 0
        wordcount2 = 0
        Name1 = self.Name1.text()
        Name2 = self.Name2.text()
        req = [Name1, Name2]

        for item in data:
            if item['participants'] == req:
                for conv in item['conversation']:
                    if 'text' in conv.keys():
                        search = conv['text']
                        if search == None:
                            continue
                        wc = len(search.split())
                        totalwordcount += wc
                        if conv['sender'] == Name1:
                            wordcount1 += wc
                        elif conv['sender'] == Name2:
                            wordcount2 += wc
        return wordcount1, wordcount2, totalwordcount

    def errorboi(self):
        self.msgbox = QMessageBox()
        self.msgbox.setText("Error, The given username doesnt exist, Check it and try again")
        self.msgbox.exec()

    def addmpl2(self, fig):
        self.canvas2 = FigureCanvas(fig)
        self.mplvl2.addWidget(self.canvas2)
        self.canvas2.draw()

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def rmmpl(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()

    def rmmpl2(self):
        self.mplvl.removeWidget(self.canvas2)
        self.canvas2.close()

    def check(self):
        with open(self.path, encoding="utf8") as f:
            data = json.load(f)
        Name1 = self.Name1.text()
        Name2 = self.Name2.text()
        req = [Name1, Name2]
        lists = []
        returnval = ""
        for item in data:
            if item['participants'] == req:
                lists.append("yes")

        if len(lists) != 0:
            returnval = True
        else:
            returnval = False

        return returnval

    def gen_search_clicked(self):

        Name1 = self.Name1.text()
        Name2 = self.Name2.text()

        if self.check():
            countmsgsname1, countmsgsname2 = self.count_messages()
            totalcountmsgs = countmsgsname1 + countmsgsname2
            self.disp_msgs_total.setText(str(totalcountmsgs))

            wordcount1, wordcount2, totalwordcount = self.wordcount()
            self.disp_words_total.setText(str(totalwordcount))

            emptystring = ""
            numberofletters1, numberofletters2 = self.Search_String(emptystring)
            self.disp_chars_total.setText(str(numberofletters1 + numberofletters2))

            self.disp_avgwords.setText(str(totalwordcount / totalcountmsgs))
            self.disp_avgchars.setText(str((numberofletters1 + numberofletters2)/totalcountmsgs))

            global timesrun
            if timesrun > 0:
                ui.rmmpl()
            # TOTAL MESSAGES

            fig1 = Figure()
            onef1 = fig1.add_subplot(131)
            fig1.set_facecolor('#172144')
            labels = [Name1, Name2]
            sizes1 = [countmsgsname1, countmsgsname2]
            onef1.set_title("Number of Messages", color='white', fontsize='13')
            patches, texts, autotexts = onef1.pie(sizes1, labels=labels, autopct='%1.1f%%', colors=('#25a1ff', '#0eebff'),
                                                  explode=(0.05, 0))

            for text in texts:
                text.set_color('#ff8419')
            for autotext in autotexts:
                autotext.set_color('black')

            # TOTAL WORDS

            twof1 = fig1.add_subplot(132)
            sizes2 = [wordcount1, wordcount2]
            twof1.set_title("Number of Words", color='white', fontsize='13')
            patches2, texts2, autotexts2 = twof1.pie(sizes2, labels=labels, autopct='%1.1f%%', colors=('#25a1ff', '#0eebff'),
                                                     explode=(0.05, 0))
            for text in texts2:
                text.set_color('#ff8419')
            for autotext in autotexts2:
                autotext.set_color('black')

            # TOTAL CHARACTERS

            threef1 = fig1.add_subplot(133)
            sizes3 = [numberofletters1, numberofletters2]
            threef1.set_title("Number of Characters", color='white', fontsize='13')
            patches3, texts3, autotexts3 = threef1.pie(sizes3, labels=labels, autopct='%1.1f%%', colors=('#25a1ff', '#0eebff'),
                                                       explode=(0.05, 0))
            for text in texts3:
                text.set_color('#ff8419')
            for autotext in autotexts3:
                autotext.set_color('black')

            timesrun += 1
            ui.addmpl(fig1)
        else:
            self.errorboi()


    def search_clicked(self):
        Name1 = self.Name1.text()
        Name2 = self.Name2.text()
        Inputword = self.Inputword.text()
        req = [Name1, Name2]
        numberofwords1, numberofwords2 = self.Search_String(Inputword)

        self.display1.setText(Name1 + " said " + Inputword + " " + str(numberofwords1) + " times")
        self.display2.setText(Name2 + " said " + Inputword + " " + str(numberofwords2) + " times")

        global timesrun2
        if timesrun2 > 0:
            ui.rmmpl2()


        fig2 = Figure()
        onef2 = fig2.add_subplot(111)
        labels = [Name1, Name2]
        height = [numberofwords1, numberofwords2]
        fig2.set_facecolor('#172144')
        onef2.set_facecolor('#172144')
        onef2.spines['bottom'].set_color('white')
        onef2.spines['left'].set_color('white')
        onef2.spines['top'].set_color('#172144')
        onef2.spines['right'].set_color('#172144')
        onef2.xaxis.label.set_color('white')
        onef2.yaxis.label.set_color('white')
        onef2.tick_params(axis='x', colors='white')
        onef2.tick_params(axis='y', colors='white')

        onef2.bar(labels, height, width=0.4, align='center', color=('#25a1ff', '#0eebff'))
        ui.addmpl2(fig2)

        timesrun2 += 1

    def Nextpage_button_clicked(self):
        self.stackedWidget.setCurrentWidget(self.homepage)

    def Browse_button_clicked(self):
        filter = "json Files (*.json)"
        fileName = QFileDialog.getOpenFileName(None, 'Search image Path', os.getcwd(), filter)
        self.path = fileName[0]
        self.file_path.setText(self.path)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1578, 964)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(16, 23, 39)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(-10, -50, 1602, 1031))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.homepage = QtWidgets.QWidget()
        self.homepage.setObjectName("homepage")
        self.label_2 = QtWidgets.QLabel(self.homepage)
        self.label_2.setGeometry(QtCore.QRect(30, 370, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(23, 33, 68);")
        self.label_2.setObjectName("label_2")
        self.disp_avgchars = QtWidgets.QLabel(self.homepage)
        self.disp_avgchars.setGeometry(QtCore.QRect(250, 640, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.disp_avgchars.setFont(font)
        self.disp_avgchars.setStyleSheet("color: rgb(248, 29, 244);\n"
                                         "background-color: rgb(23, 33, 68);")
        self.disp_avgchars.setText("")
        self.disp_avgchars.setObjectName("disp_avgchars")
        self.disp_words_total = QtWidgets.QLabel(self.homepage)
        self.disp_words_total.setGeometry(QtCore.QRect(130, 400, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.disp_words_total.setFont(font)
        self.disp_words_total.setStyleSheet("color: rgb(248, 29, 244);\n"
                                            "background-color: rgb(23, 33, 68);")
        self.disp_words_total.setText("")
        self.disp_words_total.setObjectName("disp_words_total")
        self.label_12 = QtWidgets.QLabel(self.homepage)
        self.label_12.setGeometry(QtCore.QRect(30, 730, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(23, 33, 68);")
        self.label_12.setObjectName("label_12")
        self.layoutWidget = QtWidgets.QWidget(self.homepage)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 850, 1081, 160))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.display1 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display1.sizePolicy().hasHeightForWidth())
        self.display1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.display1.setFont(font)
        self.display1.setStyleSheet("color: rgb(37, 161, 255);\n"
                                    "")
        self.display1.setLineWidth(1)
        self.display1.setText("")
        self.display1.setScaledContents(False)
        self.display1.setObjectName("display1")
        self.verticalLayout.addWidget(self.display1)
        self.display2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display2.sizePolicy().hasHeightForWidth())
        self.display2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.display2.setFont(font)
        self.display2.setStyleSheet("color : rgb(14, 235, 255);\n"
                                    "")
        self.display2.setText("")
        self.display2.setObjectName("display2")
        self.verticalLayout.addWidget(self.display2)
        self.label_4 = QtWidgets.QLabel(self.homepage)
        self.label_4.setGeometry(QtCore.QRect(30, 530, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(23, 33, 68);")
        self.label_4.setObjectName("label_4")
        self.Search = QtWidgets.QPushButton(self.homepage)
        self.Search.setGeometry(QtCore.QRect(190, 780, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.Search.setFont(font)
        self.Search.setStyleSheet("background-color: rgb(248, 29, 244);\n"
                                  "color: rgb(255, 255, 255);")
        self.Search.setObjectName("Search")
        self.mplwindow2 = QtWidgets.QWidget(self.homepage)
        self.mplwindow2.setGeometry(QtCore.QRect(1120, 560, 381, 441))
        self.mplwindow2.setObjectName("mplwindow2")
        self.mplvl2 = QtWidgets.QVBoxLayout(self.mplwindow2)
        self.mplvl2.setContentsMargins(0, 0, 0, 0)
        self.mplvl2.setObjectName("mplvl2")
        self.label_6 = QtWidgets.QLabel(self.mplwindow2)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.mplvl2.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.homepage)
        self.label_5.setGeometry(QtCore.QRect(30, 610, 341, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(23, 33, 68);")
        self.label_5.setObjectName("label_5")
        self.Inputword = QtWidgets.QLineEdit(self.homepage)
        self.Inputword.setGeometry(QtCore.QRect(190, 730, 261, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Inputword.setFont(font)
        self.Inputword.setStyleSheet("color: rgb(255, 132, 25);\n"
                                     "background-color: rgb(23, 33, 68);\n"
                                     "border-radius: 20px\n"
                                     "")
        self.Inputword.setText("")
        self.Inputword.setFrame(False)
        self.Inputword.setObjectName("Inputword")
        self.label_11 = QtWidgets.QLabel(self.homepage)
        self.label_11.setGeometry(QtCore.QRect(20, 280, 441, 411))
        self.label_11.setStyleSheet("background-color: rgb(23, 33, 68);\n"
                                    "border-radius: 20px")
        self.label_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_11.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.label_7 = QtWidgets.QLabel(self.homepage)
        self.label_7.setGeometry(QtCore.QRect(30, 50, 1531, 71))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(234, 187, 13);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.homepage)
        self.label_3.setGeometry(QtCore.QRect(30, 450, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color : rgb(23, 33, 68)")
        self.label_3.setObjectName("label_3")
        self.disp_avgwords = QtWidgets.QLabel(self.homepage)
        self.disp_avgwords.setGeometry(QtCore.QRect(250, 560, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.disp_avgwords.setFont(font)
        self.disp_avgwords.setStyleSheet("color: rgb(248, 29, 244);\n"
                                         "background-color: rgb(23, 33, 68);")
        self.disp_avgwords.setText("")
        self.disp_avgwords.setObjectName("disp_avgwords")
        self.label_13 = QtWidgets.QLabel(self.homepage)
        self.label_13.setGeometry(QtCore.QRect(20, 720, 441, 111))
        self.label_13.setStyleSheet("background-color: rgb(23, 33, 68);\n"
                                    "border-radius: 20px")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.disp_msgs_total = QtWidgets.QLabel(self.homepage)
        self.disp_msgs_total.setGeometry(QtCore.QRect(130, 320, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.disp_msgs_total.setFont(font)
        self.disp_msgs_total.setStyleSheet("color: rgb(248, 29, 244);\n"
                                           "background-color: rgb(23, 33, 68);")
        self.disp_msgs_total.setText("")
        self.disp_msgs_total.setObjectName("disp_msgs_total")
        self.layoutWidget1 = QtWidgets.QWidget(self.homepage)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 140, 671, 128))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Name1 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Name1.setFont(font)
        self.Name1.setAccessibleName("")
        self.Name1.setAutoFillBackground(False)
        self.Name1.setStyleSheet("background-color: rgb(16, 23, 39);\n"
                                 "color: rgb(255, 132, 25);")
        self.Name1.setInputMask("")
        self.Name1.setText("")
        self.Name1.setFrame(False)
        self.Name1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Name1.setObjectName("Name1")
        self.verticalLayout_2.addWidget(self.Name1)
        self.Name2 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Name2.setFont(font)
        self.Name2.setMouseTracking(True)
        self.Name2.setStyleSheet("background-color: rgb(16, 23, 39);\n"
                                 "color: rgb(255, 132, 25);")
        self.Name2.setFrame(False)
        self.Name2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Name2.setObjectName("Name2")
        self.verticalLayout_2.addWidget(self.Name2)
        self.Name2.raise_()
        self.Name1.raise_()
        self.label = QtWidgets.QLabel(self.homepage)
        self.label.setGeometry(QtCore.QRect(30, 290, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(23, 33, 68);")
        self.label.setObjectName("label")
        self.mplwindow = QtWidgets.QWidget(self.homepage)
        self.mplwindow.setGeometry(QtCore.QRect(490, 280, 1071, 241))
        self.mplwindow.setStyleSheet("border-radius: 20px")
        self.mplwindow.setObjectName("mplwindow")
        self.mplvl = QtWidgets.QVBoxLayout(self.mplwindow)
        self.mplvl.setContentsMargins(0, 0, 0, 0)
        self.mplvl.setObjectName("mplvl")
        self.disp_chars_total = QtWidgets.QLabel(self.homepage)
        self.disp_chars_total.setGeometry(QtCore.QRect(130, 480, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.disp_chars_total.setFont(font)
        self.disp_chars_total.setStyleSheet("color: rgb(248, 29, 244);\n"
                                            "background-color: rgb(23, 33, 68);")
        self.disp_chars_total.setText("")
        self.disp_chars_total.setObjectName("disp_chars_total")
        self.gen_search = QtWidgets.QPushButton(self.homepage)
        self.gen_search.setGeometry(QtCore.QRect(710, 190, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.gen_search.setFont(font)
        self.gen_search.setStatusTip("")
        self.gen_search.setStyleSheet("background-color: rgb(248, 29, 244);\n"
                                      "color: rgb(255, 255, 255);")
        self.gen_search.setIconSize(QtCore.QSize(120, 60))
        self.gen_search.setFlat(False)
        self.gen_search.setObjectName("gen_search")
        self.label_13.raise_()
        self.label_11.raise_()
        self.label_2.raise_()
        self.disp_avgchars.raise_()
        self.disp_words_total.raise_()
        self.label_12.raise_()
        self.layoutWidget.raise_()
        self.label_4.raise_()
        self.Search.raise_()
        self.mplwindow2.raise_()
        self.label_5.raise_()
        self.Inputword.raise_()
        self.label_7.raise_()
        self.label_3.raise_()
        self.disp_avgwords.raise_()
        self.disp_msgs_total.raise_()
        self.layoutWidget.raise_()
        self.label.raise_()
        self.disp_chars_total.raise_()
        self.gen_search.raise_()
        self.mplwindow.raise_()
        self.stackedWidget.addWidget(self.homepage)
        self.pathpage = QtWidgets.QWidget()
        self.pathpage.setObjectName("pathpage")
        self.label_9 = QtWidgets.QLabel(self.pathpage)
        self.label_9.setGeometry(QtCore.QRect(360, 820, 901, 61))
        self.label_9.setStyleSheet("background-color: rgb(23, 33, 68);\n"
                                   "border-radius: 20px")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.Nextpage = QtWidgets.QPushButton(self.pathpage)
        self.Nextpage.setGeometry(QtCore.QRect(750, 930, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.Nextpage.setFont(font)
        self.Nextpage.setStyleSheet("background-color: rgb(248, 29, 244);\n"
                                    "color: rgb(255, 255, 255);")
        self.Nextpage.setObjectName("Nextpage")
        self.label_10 = QtWidgets.QLabel(self.pathpage)
        self.label_10.setGeometry(QtCore.QRect(240, 70, 1091, 111))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(234, 187, 13);")
        self.label_10.setObjectName("label_10")
        self.label_14 = QtWidgets.QLabel(self.pathpage)
        self.label_14.setGeometry(QtCore.QRect(690, 230, 871, 561))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(23, 33, 68);\n"
                                    "border-radius: 20px")
        self.label_14.setTextFormat(QtCore.Qt.RichText)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.pathpage)
        self.label_15.setGeometry(QtCore.QRect(30, 230, 631, 351))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: rgb(23, 33, 68);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-radius : 20px\n"
                                    "")
        self.label_15.setTextFormat(QtCore.Qt.RichText)
        self.label_15.setObjectName("label_15")
        self.label_17 = QtWidgets.QLabel(self.pathpage)
        self.label_17.setGeometry(QtCore.QRect(1230, 190, 251, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_17.setObjectName("label_17")
        self.label_16 = QtWidgets.QLabel(self.pathpage)
        self.label_16.setGeometry(QtCore.QRect(1330, 150, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(234, 187, 13);")
        self.label_16.setObjectName("label_16")
        self.label_8 = QtWidgets.QLabel(self.pathpage)
        self.label_8.setGeometry(QtCore.QRect(370, 830, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(23, 33, 68)")
        self.label_8.setObjectName("label_8")
        self.file_path = QtWidgets.QLineEdit(self.pathpage)
        self.file_path.setGeometry(QtCore.QRect(495, 830, 641, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_path.sizePolicy().hasHeightForWidth())
        self.file_path.setSizePolicy(sizePolicy)
        self.file_path.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(23, 33, 68)")
        self.file_path.setFrame(False)
        self.file_path.setObjectName("file_path")
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.file_path.setFont(font)
        self.Browse_button = QtWidgets.QPushButton(self.pathpage)
        self.Browse_button.setGeometry(QtCore.QRect(1150, 830, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.Browse_button.setFont(font)
        self.Browse_button.setStyleSheet("background-color: rgb(248, 29, 244);\n"
                                         "color: rgb(255, 255, 255);")
        self.Browse_button.setObjectName("Browse_button")
        self.label_9.raise_()
        self.Nextpage.raise_()
        self.label_10.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_17.raise_()
        self.label_16.raise_()
        self.label_8.raise_()
        self.file_path.raise_()
        self.Browse_button.raise_()
        self.stackedWidget.addWidget(self.pathpage)
        MainWindow.setCentralWidget(self.centralwidget)
        #
        self.stackedWidget.setCurrentWidget(self.pathpage)
        self.Nextpage.clicked.connect(self.Nextpage_button_clicked)
        self.Browse_button.clicked.connect(self.Browse_button_clicked)
        self.Search.clicked.connect(self.search_clicked)
        self.gen_search.clicked.connect(self.gen_search_clicked)
        #
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "InstaChat Analyser--beta"))
        self.label_2.setText(_translate("MainWindow", "Words Total"))
        self.label_12.setText(_translate("MainWindow", "Custom Search:"))
        self.label_4.setText(_translate("MainWindow", "Average words per message"))
        self.Search.setText(_translate("MainWindow", "Find!"))
        self.label_5.setText(_translate("MainWindow", "Average Characters per message"))
        self.Inputword.setPlaceholderText(_translate("MainWindow", "Enter Word here"))
        self.label_7.setText(_translate("MainWindow", "Your Insta Banter"))
        self.label_3.setText(_translate("MainWindow", "Characters Total"))
        self.Name1.setToolTip(_translate("MainWindow", "Enter name here:"))
        self.Name1.setPlaceholderText(_translate("MainWindow", "Enter your insta username here:"))
        self.Name2.setPlaceholderText(_translate("MainWindow", "Enter the other person\'s username:"))
        self.label.setText(_translate("MainWindow", "Messages Total"))
        self.gen_search.setToolTip(_translate("MainWindow", "click to proceed"))
        self.gen_search.setText(_translate("MainWindow", "GO!"))
        self.Nextpage.setText(_translate("MainWindow", "Next >>"))
        self.label_10.setText(_translate("MainWindow", "Instagram Conversation Analyser"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p>Following are the steps to get "
                                                       "started:</p><p>1) Download the Data:</p><p>On the instagam "
                                                       "app, go to Settings &gt;&gt; Security &gt;&gt; Download "
                                                       "Data.</p><p>Enter your email address and request download. "
                                                       "You will receive</p><p>the link to download the data on "
                                                       "</p><p>your email within 48 hours. (Generally it takes less "
                                                       "than 20 mins)</p><p><br/>2) Once u get the link, download the "
                                                       "<span style=\" color:#eabb0d;\">&quot;Part 1&quot;</span> "
                                                       "data.</p><p><br/>3) Unzip the data :</p><p>Do this using any "
                                                       "Unzipping tool like RAR, 7zip, WinZip etc.<br/></p><p>4) "
                                                       "Voila! </p><p>You will get a file named <span style=\" "
                                                       "color:#eabb0d;\">&quot;messages&quot;</span> with a .json "
                                                       "extension. </p><p>Now select that file through the Browse "
                                                       "Button and Click Next to proceed.</p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p>Hi there!</p><p>This is the Instagram "
                                                       "Conversation Analyser, </p><p>You can visualise your "
                                                       "conversation with</p><p>someone in terms of ratio of "
                                                       "messages, words</p><p>and more.<br/></p><p>You can search how "
                                                       "many emotes you used and </p><p>visualise it with a graph as "
                                                       "well!</p></body></html>"))
        self.label_17.setText(_translate("MainWindow", "Developed by: Soham Kulkarni"))
        self.label_16.setText(_translate("MainWindow", "beta"))
        self.label_8.setText(_translate("MainWindow", "Select File :"))
        self.Browse_button.setText(_translate("MainWindow", "Browse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
