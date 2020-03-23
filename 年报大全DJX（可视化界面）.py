# 作者丁敬轩
import requests, time, os, json, sys
from bs4 import BeautifulSoup as soup
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 50, 640, 100))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 20, 640, 20))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(560, 160, 75, 25))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 300, 320, 150))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 270, 100, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 220, 100, 20))
        self.label_3.setObjectName("label_3")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(330, 250, 310, 200))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 210, 100, 20))
        self.label_4.setObjectName("label_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(300, 175, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 175, 100, 20))
        self.label_5.setObjectName("label_5")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(90, 205, 100, 30))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(90, 170, 100, 30))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(0, 175, 100, 20))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.run)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请在下方输入要爬取的全部公司名称（每两个公司中间要空格或者回车）："))
        self.pushButton.setText(_translate("MainWindow", "输入完毕"))
        self.label_2.setText(_translate("MainWindow", "爬取过程栏"))
        self.label_3.setText(_translate("MainWindow", "爬取结果栏"))
        self.label_4.setText(_translate("MainWindow", "已爬取公司数： "))
        self.label_5.setText(_translate("MainWindow", "爬取进度："))
        self.label_6.setText(_translate("MainWindow", "总公司数："))

    def run (self) :
        text2 = self.textEdit.toPlainText()
        comNames = text2.split()
        self.progressBar.setValue(0)
        self.lcdNumber.display(0)
        self.lcdNumber_2.display(len(comNames))
        self.textBrowser_2.clear()
        self.textBrowser.clear()
        self.textBrowser.append("爬取开始")
        year = time.strftime("%Y", time.localtime())
        month = time.strftime("%m", time.localtime())
        day = time.strftime("%d", time.localtime())
        self.textBrowser.append(year + "-" + month + "-" + day)
        QtWidgets.QApplication.processEvents()
        exp = []
        bug = []
        same = []
        tot = 0
        for comName in comNames:
            for j in comName:
                if j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                        and j != "\"" and j != "<" and j != ">" and j != "|":
                    pass
                else:
                    comName = comName.replace(j, "")
            error = False
            docxs = []
            pdfs = []
            js = []
            dtitle = []
            ptitle = []
            jtitle = []
            cwd = os.getcwd() + '\\' + comName
            sameName = os.path.exists(cwd)
            if sameName == False:
                try:
                    cnt = 0
                    sum = 100
                    page = 1
                    while cnt < sum:
                        data = {
                            "pageNum": page,
                            "pageSize": 30,
                            "column": "szse",
                            "tabName": "fulltext",
                            "searchkey": comName,
                            "category": "category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh",
                            "seDate": "1000-01-01~%s-%s-%s" % (year, month, day),
                            "isHLtitle": "true"
                        }
                        res = requests.post("http://www.cninfo.com.cn/new/hisAnnouncement/query?", data=data).json()
                        sum = res["totalAnnouncement"]
                        res = res["announcements"]
                        for i in res:
                            cnt += 1
                            secName = i["secName"]
                            announcementTitle = i["announcementTitle"]
                            secName += announcementTitle
                            title = ""
                            run = True
                            for j in secName:
                                if j == "<":
                                    run = False
                                elif j == ">":
                                    run = True
                                elif run and j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                                        and j != "\"" and j != "<" and j != ">" and j != "|":
                                    title += j
                            adjunctUrl = i["adjunctUrl"]
                            if "PDF" in adjunctUrl:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl).content
                                pdfs.append(res2)
                                ptitle.append(title)
                                self.textBrowser.append(title + "okay")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                            elif ".html" in adjunctUrl:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                                res2.encoding = "windows-1252"
                                res2 = res2.text
                                bs = soup(res2, "html.parser")
                                bs = bs.find_all("table", align="center")
                                bj = []
                                max = 0
                                bbb = 0
                                count = 0
                                for k in bs:
                                    bj.append(len(k.text))
                                for k in bj:
                                    if k > max:
                                        max = k
                                        bbb = bs[count]
                                    count += 1
                                bs = bbb.find_all("span", class_="da")[1]
                                bs = str(bs)
                                list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen",
                                        "&euro",
                                        "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                                list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×",
                                         "÷"]
                                for i in range(len(list)):
                                    bs = bs.replace(list[i], list2[i])
                                bs = bs.replace("<br>", "\n")
                                bs = bs.replace("<br/>", "\n")
                                b = ""
                                for j in bs:
                                    if j == "<":
                                        run = False
                                    elif j == ">":
                                        run = True
                                    elif run:
                                        b += j
                                docxs.append(b.strip())
                                dtitle.append(title)
                                self.textBrowser.append(title + "text")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                            else:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                                res2.encoding = "gbk"
                                res2 = res2.text
                                bs = soup(res2, "html.parser").text
                                bs = str(bs)
                                bs = bs.replace("var affiches=", "")
                                bs = bs.strip()[: - 1]
                                bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                                bs = str(bs)
                                list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen",
                                        "&euro",
                                        "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                                list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×",
                                         "÷"]
                                for i in range(len(list)):
                                    bs = bs.replace(list[i], list2[i])
                                bs = bs.replace("<br>", "\n")
                                bs = bs.replace("<br/>", "\n")
                                b = ""
                                for j in bs:
                                    if j == "<":
                                        run = False
                                    elif j == ">":
                                        run = True
                                    elif run:
                                        b += j
                                js.append(b.strip())
                                jtitle.append(title)
                                self.textBrowser.append(title + "javascript")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                        page += 1
                except:
                    error = True
                    bug.append(comName)
            if error:
                self.textBrowser.append(comName + "爬取时出错")
                QtWidgets.QApplication.processEvents()
            elif sameName:
                self.textBrowser.append(comName + "已经爬取过")
                QtWidgets.QApplication.processEvents()
                same.append(comName)
            elif cnt == 0:
                try:
                    data2 = {
                        "keyWord": comName.swapcase(),
                        "maxSecNum": 10,
                        "maxListNum": 5
                    }
                    res3 = requests.post("http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery",
                                         data=data2).json()
                    code = res3["keyBoardList"]
                    code = code[0]
                    code = code["code"]
                    docxs = []
                    pdfs = []
                    js = []
                    dtitle = []
                    ptitle = []
                    jtitle = []
                    cnt = 0
                    sum = 100
                    page = 1
                    while cnt < sum:
                        data3 = {
                            "pageNum": page,
                            "pageSize": 30,
                            "column": "szse",
                            "tabName": "fulltext",
                            "stock": code,
                            "category": "category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh",
                            "seDate": "1000-01-01~%s-%s-%s" % (year, month, day),
                            "isHLtitle": "true"
                        }
                        res = requests.post("http://www.cninfo.com.cn/new/hisAnnouncement/query?", data=data3).json()
                        sum = res["totalAnnouncement"]
                        res = res["announcements"]
                        for i in res:
                            cnt += 1
                            secName = i["secName"]
                            announcementTitle = i["announcementTitle"]
                            secName += announcementTitle
                            title = ""
                            run = True
                            for j in secName:
                                if j == "<":
                                    run = False
                                elif j == ">":
                                    run = True
                                elif run and j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                                        and j != "\"" and j != "<" and j != ">" and j != "|":
                                    title += j
                            adjunctUrl = i["adjunctUrl"]
                            if "PDF" in adjunctUrl:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl).content
                                pdfs.append(res2)
                                ptitle.append(title)
                                self.textBrowser.append(title + "okay")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                            elif ".html" in adjunctUrl:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                                res2.encoding = "windows-1252"
                                res2 = res2.text
                                bs = soup(res2, "html.parser")
                                bs = bs.find_all("table", align="center")
                                bj = []
                                max = 0
                                bbb = 0
                                count = 0
                                for k in bs:
                                    bj.append(len(k.text))
                                for k in bj:
                                    if k > max:
                                        max = k
                                        bbb = bs[count]
                                    count += 1
                                bs = bbb.find_all("span", class_="da")[1]
                                bs = str(bs)
                                list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen",
                                        "&euro",
                                        "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                                list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×",
                                         "÷"]
                                for i in range(len(list)):
                                    bs = bs.replace(list[i], list2[i])
                                bs = bs.replace("<br>", "\n")
                                bs = bs.replace("<br/>", "\n")
                                b = ""
                                for j in bs:
                                    if j == "<":
                                        run = False
                                    elif j == ">":
                                        run = True
                                    elif run:
                                        b += j
                                docxs.append(b.strip())
                                dtitle.append(title)
                                self.textBrowser.append(title + "text")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                            else:
                                res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                                res2.encoding = "gbk"
                                res2 = res2.text
                                bs = soup(res2, "html.parser").text
                                bs = str(bs)
                                bs = bs.replace("var affiches=", "")
                                bs = bs.strip()[: - 1]
                                bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                                bs = str(bs)
                                list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen",
                                        "&euro",
                                        "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                                list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×",
                                         "÷"]
                                for i in range(len(list)):
                                    bs = bs.replace(list[i], list2[i])
                                bs = bs.replace("<br>", "\n")
                                bs = bs.replace("<br/>", "\n")
                                b = ""
                                for j in bs:
                                    if j == "<":
                                        run = False
                                    elif j == ">":
                                        run = True
                                    elif run:
                                        b += j
                                js.append(b.strip())
                                jtitle.append(title)
                                self.textBrowser.append(title + "javascript")
                                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                                QtWidgets.QApplication.processEvents()
                        page += 1
                    if cnt == 0:
                        self.textBrowser.append(comName + "名称错误")
                        QtWidgets.QApplication.processEvents()
                        exp.append(comName)
                    else:
                        self.textBrowser.append(comName + "over")
                        QtWidgets.QApplication.processEvents()
                        ct = 0
                        os.mkdir(cwd)
                        for docx in docxs:
                            file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="windows-1252")
                            file1.write(docx)
                            file1.close()
                            ct += 1
                        ct = 0
                        for pdf in pdfs:
                            file1 = open(cwd + "\\%s.PDF" % ptitle[ct], "wb")
                            file1.write(pdf)
                            file1.close()
                            ct += 1
                        ct = 0
                        for javascript in js:
                            file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="gbk")
                            file1.write(javascript)
                            file1.close()
                            ct += 1
                except:
                    self.textBrowser.append(comName + "名称错误")
                    QtWidgets.QApplication.processEvents()
                    exp.append(comName)
            else:
                self.textBrowser.append(comName + "over")
                QtWidgets.QApplication.processEvents()
                ct = 0
                os.mkdir(cwd)
                for docx in docxs:
                    file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="windows-1252")
                    file1.write(docx)
                    file1.close()
                    ct += 1
                ct = 0
                for pdf in pdfs:
                    file1 = open(cwd + "\\%s.PDF" % ptitle[ct], "wb")
                    file1.write(pdf)
                    file1.close()
                    ct += 1
                ct = 0
                for javascript in js:
                    file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="gbk")
                    file1.write(javascript)
                    file1.close()
                    ct += 1
            tot += 1
            self.progressBar.setValue(int (tot / len(comNames) * 100))
            self.lcdNumber.display(int (tot))
            QtWidgets.QApplication.processEvents()
        self.textBrowser.append("爬取结束")
        self.textBrowser_2.append("共有%d个名称有问题，分别是：" % len (exp))
        for i in exp:
            self.textBrowser_2.append(i + " ")
        self.textBrowser_2.append("\n")
        self.textBrowser_2.append("共有%d个公司爬取时出错，分别是：" % len (bug))
        for i in bug:
            self.textBrowser_2.append(i + " ")
        self.textBrowser_2.append("\n")
        self.textBrowser_2.append("共有%d个公司已经被爬取过，分别是：" % len (same))
        for i in same:
            self.textBrowser_2.append(i + " ")
        self.textBrowser_2.moveCursor(self.textBrowser.textCursor().End)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
