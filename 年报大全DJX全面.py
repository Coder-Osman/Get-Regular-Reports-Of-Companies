# 作者丁敬轩
import requests, time, os
from bs4 import BeautifulSoup as soup
import json
year = time.strftime("%Y", time.localtime())
month = time.strftime("%m", time.localtime())
day = time.strftime("%d", time.localtime())
print (year + "-" + month + "-" + day)
company = open ("company.txt", "r")
comNames = company.read ().split ()
company.close ()
exp = []
bug = []
same = []
for comName in comNames :
    cor1 = True
    # A股
    for j in comName :
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
    cwd = os.getcwd() + '\\A股 ' + comName
    sameName = os.path.exists (cwd)
    cnt = 0
    if sameName == False :
        try :
            cnt = 0
            sum = 100
            page = 1
            while cnt < sum :
                data = {
                    "pageNum" : page,
                    "pageSize" : 30,
                    "column" : "szse",
                    "tabName" : "fulltext",
                    "searchkey" : comName,
                    "category" : "category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh",
                    "seDate" : "1000-01-01~%s-%s-%s" % (year, month, day),
                    "isHLtitle" : "true"
                }
                res = requests.post ("http://www.cninfo.com.cn/new/hisAnnouncement/query?", data = data).json ()
                sum = res ["totalAnnouncement"]
                res = res ["announcements"]
                for i in res :
                    cnt += 1
                    secName = i ["secName"]
                    announcementTitle = i ["announcementTitle"]
                    secName += announcementTitle
                    title = ""
                    run = True
                    for j in secName :
                        if j == "<" :
                            run = False
                        elif j == ">" :
                            run = True
                        elif run and j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                                 and j != "\"" and j != "<" and j != ">" and j != "|":
                            title += j
                    adjunctUrl = i ["adjunctUrl"]
                    if "PDF" in adjunctUrl :
                        res2 = requests.get ("http://static.cninfo.com.cn/%s" % adjunctUrl).content
                        pdfs.append (res2)
                        ptitle.append (title)
                        print ("A股" + title + "okay")
                    elif ".html" in adjunctUrl :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup (res2, "html.parser")
                        bs = bs.find_all ("table", align = "center")
                        bj = []
                        max = 0
                        bbb = 0
                        count = 0
                        for k in bs :
                            bj.append (len (k.text))
                        for k in bj :
                            if k > max :
                                max = k
                                bbb = bs [count]
                            count += 1
                        bs = bbb.find_all ("span", class_ = "da") [1]
                        bs = str (bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
                        for i in range(len(list)):
                            bs = bs.replace(list[i], list2[i])
                        bs = bs.replace ("<br>", "\n")
                        bs = bs.replace ("<br/>", "\n")
                        b = ""
                        for j in bs :
                            if j == "<":
                                run = False
                            elif j == ">":
                                run = True
                            elif run:
                                b += j
                        docxs.append (b.strip ())
                        dtitle.append (title)
                        print("A股" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs)[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("A股" + title + "javascript")
                page += 1
        except:
            error = True
            bug.append(comName)
    if error :
        print ("A股" + comName + "爬取时出错")
    elif sameName:
        print("A股" + comName + "已经爬取过")
        same.append(comName)
    elif cnt == 0 :
        try :
            data2 = {
                "keyWord" : comName.swapcase (),
                "maxSecNum" : 10,
                "maxListNum" : 5
            }
            res3 = requests.post ("http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery", data = data2).json ()
            code = res3 ["keyBoardList"]
            code = code [0]
            code = code ["code"]
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
                        print("A股" + title + "okay")
                    elif ".html" in adjunctUrl :
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
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("A股" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("A股" + title + "javascript")
                page += 1
            if cnt == 0 :
                cor1 = False
            else :
                print("A股" + comName + "over")
                ct = 0
                os.mkdir(cwd)
                for docx in docxs:
                    file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="utf-8")
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
                    file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
                    file1.write(javascript)
                    file1.close()
                    ct += 1
        except :
            cor1 = False
    else :
        print ("A股" + comName + "over")
        ct = 0
        os.mkdir (cwd)
        for docx in docxs :
            file1 = open(cwd + "\\%s.docx" % dtitle [ct], "w", encoding = "utf-8")
            file1.write(docx)
            file1.close()
            ct += 1
        ct = 0
        for pdf in pdfs :
            file1 = open(cwd + "\\%s.PDF" % ptitle [ct], "wb")
            file1.write(pdf)
            file1.close()
            ct += 1
        ct = 0
        for javascript in js:
            file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
            file1.write(javascript)
            file1.close()
            ct += 1












    cnt = 0
    cor2 = True
    # Hong Kong
    for j in comName :
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
    cwd = os.getcwd() + '\\港股 ' + comName
    sameName = os.path.exists (cwd)
    if sameName == False :
        try :
            cnt = 0
            sum = 100
            page = 1
            while cnt < sum :
                data = {
                    "pageNum" : page,
                    "pageSize" : 30,
                    "column" : "hke",
                    "tabName" : "fulltext",
                    "searchkey" : comName,
                    "seDate" : "1000-01-01~%s-%s-%s" % (year, month, day),
                    "isHLtitle" : "true"
                }
                res = requests.post ("http://www.cninfo.com.cn/new/hisAnnouncement/query?", data = data).json ()
                sum = res ["totalAnnouncement"]
                res = res ["announcements"]
                for i in res :
                    secName = i ["secName"]
                    announcementTitle = i ["announcementTitle"]
                    if "中期报告" not in announcementTitle and "年度报告" not in announcementTitle or "通知" in announcementTitle or "债券" in announcementTitle :
                        sum -= 1
                        continue
                    cnt += 1
                    if secName is None :
                        secName = comName
                    secName += announcementTitle
                    title = ""
                    run = True
                    for j in secName :
                        if j == "<" :
                            run = False
                        elif j == ">" :
                            run = True
                        elif run and j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                                 and j != "\"" and j != "<" and j != ">" and j != "|":
                            title += j
                    adjunctUrl = i ["adjunctUrl"]
                    if "PDF" in adjunctUrl :
                        res2 = requests.get ("http://static.cninfo.com.cn/%s" % adjunctUrl).content
                        pdfs.append (res2)
                        ptitle.append (title)
                        print ("港股" + title + "okay")
                    elif ".html" in adjunctUrl :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "windows-1252"
                        res2 = res2.text
                        bs = soup (res2, "html.parser")
                        bs = bs.find_all ("table", align = "center")
                        bj = []
                        max = 0
                        bbb = 0
                        count = 0
                        for k in bs :
                            bj.append (len (k.text))
                        for k in bj :
                            if k > max :
                                max = k
                                bbb = bs [count]
                            count += 1
                        bs = bbb.find_all ("span", class_ = "da") [1]
                        bs = str (bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
                        for i in range(len(list)):
                            bs = bs.replace(list[i], list2[i])
                        bs = bs.replace ("<br>", "\n")
                        bs = bs.replace ("<br/>", "\n")
                        b = ""
                        for j in bs :
                            if j == "<":
                                run = False
                            elif j == ">":
                                run = True
                            elif run:
                                b += j
                        docxs.append (b.strip ())
                        dtitle.append (title)
                        print("港股" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("港股" + title + "javascript")
                page += 1
        except:
            error = True
            bug.append(comName)
    if error :
        print ("港股" + comName + "爬取时出错")
    elif sameName:
        print("港股" + comName + "已经爬取过")
        same.append(comName)
    elif cnt == 0 :
        try :
            data2 = {
                "keyWord" : comName.swapcase (),
                "maxSecNum" : 10,
                "maxListNum" : 5
            }
            res3 = requests.post ("http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery", data = data2).json ()
            code = res3 ["keyBoardList"]
            code = code [0]
            plate = code ["plate"]
            if plate != "hke" :
                raise ()
            code = code ["code"]
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
                    if "中期报告" not in announcementTitle and "年度报告" not in announcementTitle or "通知" in announcementTitle or "债券" in announcementTitle :
                        continue
                    if secName is None:
                        secName = comName
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
                        print("港股" + title + "okay")
                    elif ".html" in adjunctUrl :
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
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("港股" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("港股" + title + "javascript")
                page += 1
            if cnt == 0 :
                cor2 = False
            else :
                print("港股" + comName + "over")
                ct = 0
                os.mkdir(cwd)
                for docx in docxs:
                    file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="utf-8")
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
                    file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
                    file1.write(javascript)
                    file1.close()
                    ct += 1
        except :
            cor2 = False
    else :
        print ("港股" + comName + "over")
        ct = 0
        os.mkdir (cwd)
        for docx in docxs:
            file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="utf-8")
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
            file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
            file1.write(javascript)
            file1.close()
            ct += 1













    cnt = 0
    cor3 = True
    # trird
    for j in comName :
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
    cwd = os.getcwd() + '\\三板 ' + comName
    sameName = os.path.exists (cwd)
    if sameName == False :
        try :
            cnt = 0
            sum = 100
            page = 1
            while cnt < sum :
                data = {
                    "pageNum" : page,
                    "pageSize" : 30,
                    "column" : "third",
                    "tabName" : "fulltext",
                    "searchkey" : comName,
                    "category" : "category_dqgg",
                    "seDate" : "1000-01-01~%s-%s-%s" % (year, month, day),
                    "isHLtitle" : "true"
                }
                res = requests.post ("http://www.cninfo.com.cn/new/hisAnnouncement/query?", data = data).json ()
                sum = res ["totalAnnouncement"]
                res = res ["announcements"]
                for i in res :
                    cnt += 1
                    secName = i ["secName"]
                    announcementTitle = i ["announcementTitle"]
                    secName += announcementTitle
                    title = ""
                    run = True
                    for j in secName :
                        if j == "<" :
                            run = False
                        elif j == ">" :
                            run = True
                        elif run and j != "/" and j != "\\" and j != ":" and j != "*" and j != "?" \
                                 and j != "\"" and j != "<" and j != ">" and j != "|":
                            title += j
                    adjunctUrl = i ["adjunctUrl"]
                    if "PDF" in adjunctUrl :
                        res2 = requests.get ("http://static.cninfo.com.cn/%s" % adjunctUrl).content
                        pdfs.append (res2)
                        ptitle.append (title)
                        print ("三板" + title + "okay")
                    elif ".html" in adjunctUrl :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "windows-1252"
                        res2 = res2.text
                        bs = soup (res2, "html.parser")
                        bs = bs.find_all ("table", align = "center")
                        bj = []
                        max = 0
                        bbb = 0
                        count = 0
                        for k in bs :
                            bj.append (len (k.text))
                        for k in bj :
                            if k > max :
                                max = k
                                bbb = bs [count]
                            count += 1
                        bs = bbb.find_all ("span", class_ = "da") [1]
                        bs = str (bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
                        for i in range(len(list)):
                            bs = bs.replace(list[i], list2[i])
                        bs = bs.replace ("<br>", "\n")
                        bs = bs.replace ("<br/>", "\n")
                        b = ""
                        for j in bs :
                            if j == "<":
                                run = False
                            elif j == ">":
                                run = True
                            elif run:
                                b += j
                        docxs.append (b.strip ())
                        dtitle.append (title)
                        print("三板" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("三板" + title + "javascript")
                page += 1
        except:
            error = True
            bug.append(comName)
    if error :
        print ("三板" + comName + "爬取时出错")
    elif sameName:
        print("三板" + comName + "已经爬取过")
        same.append(comName)
    elif cnt == 0 :
        try :
            data2 = {
                "keyWord" : comName.swapcase (),
                "maxSecNum" : 10,
                "maxListNum" : 5
            }
            res3 = requests.post ("http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery", data = data2).json ()
            code = res3 ["keyBoardList"]
            code = code [0]
            plate = code ["plate"]
            if plate != "neeq" :
                raise ()
            code = code ["code"]
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
                        print("三板" + title + "okay")
                    elif ".html" in adjunctUrl :
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
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("三板" + title + "text")
                    else :
                        res2 = requests.get("http://static.cninfo.com.cn/%s" % adjunctUrl)
                        res2.encoding = "gbk"
                        res2 = res2.text
                        bs = soup(res2, "html.parser").text
                        bs = str(bs)
                        bs = bs.replace("var affiches=", "")
                        bs = bs.strip()[: - 1]
                        bs = json.loads(bs, encoding="gbk")[0]["Zw"]
                        bs = str(bs)
                        list = ["&nbsp", "&gt", "&amp", "&lt", "&quot", "&apos", "&cent", "&pound", "&yen", "&euro",
                                "&sect", "&copy", "&reg", "&trade", "&times", "&divide"]
                        list2 = [" ", ">", "&", "<", "\"", "'", "￠", "£", "¥", "€", "§", "©", "®", "™", "×", "÷"]
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
                        print("三板" + title + "javascript")
                page += 1
            if cnt == 0 :
                cor3 = False
            else :
                print("三板" + comName + "over")
                ct = 0
                os.mkdir(cwd)
                for docx in docxs:
                    file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="utf-8")
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
                    file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
                    file1.write(javascript)
                    file1.close()
                    ct += 1
        except :
            cor3 = False
    else :
        print ("三板" + comName + "over")
        ct = 0
        os.mkdir (cwd)
        for docx in docxs:
            file1 = open(cwd + "\\%s.docx" % dtitle[ct], "w", encoding="utf-8")
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
            file1 = open(cwd + "\\%s.docx" % jtitle[ct], "w", encoding="utf-8")
            file1.write(javascript)
            file1.close()
            ct += 1
    if not (cor1 or cor2 or cor3) :
        exp.append (comName)
        print (comName + "名称错误")

problem = open ("problem.txt", "w")
problem.write ("共有%d个名称有问题，分别是：" % len (exp))
for i in exp :
    problem.write (i + " ")
problem.write ("\n")
problem.write ("共有%d个公司爬取时出错，分别是：" % len (bug))
for i in bug :
    problem.write (i + " ")
problem.write ("\n")
problem.write ("共有%d个公司已经被爬取过，分别是：" % len (same))
for i in same :
    problem.write (i + " ")
problem.close ()