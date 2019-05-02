# -*- encoding: utf-8 -*-
"""
Author: Tao-Chun Cheng
Date: 2018-01-01
Usage: Masterlink Securities, daily flow for FINI, ITC and Prop desks.
Decriptions:
1. Stocks are first sorted by traded values according to investors
2. Top ranked stocks are then calculated for days net bought and sold
3. The final output are then pasted to the Bloomberg chats

"""
import requests
import sqlite3
import time
import os
#from openpyxl import Workbook
from datetime import timedelta, date
from urllib import request, parse
from bs4 import BeautifulSoup as bss

#header information of websites
goodinfoHead = {
        "host": "goodinfo.tw",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br"
        }

twseHead = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"}

gretaiHead = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "en,en-US;q=0.7,zh-TW;q=0.3",
        "Host" : "www.tpex.org.tw",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0 "        
        }

#Global Variables
twse = "http://www.twse.com.tw/"
gretai = "http://www.tpex.org.tw/"
tableName = "三大法人"
holidays = ['20180213','20180214','20180215',
            '20180216','20180219','20180220',
            '20180101','20171010',
            '20170928','20180616','20180617',
            '20180404','20180405','20180406',
            '20180618','20180922','20180923',
            '20180924','20181231', '20180228',
            "20171009", "20171004", "20171228"]


if date.today() == '2018-12-22':
    print("Working Saturday")
    holiNum = 5
else:
    holiNum = 4

etf = [
       '0050'  ,'00677U', '00632R', '00639' , '00687B',
       '00687B','00723B','00637L' ,'00633L' ,'00725B' ,
       '00655L','00636' ,'00694B' ,'0056'   , '00694B',
       '00727B','00673R', '00710B', '00713' , '00712' ,
       '006205','00653L', '00683L','00665L' ,'00679B' ,
       '006206','00676R', '00663L','00664R' ,'00669R' ,
       '00671R','00648R', '00718B', '006207', '2891B' ,
       '00640L','00672L', '00657' , '00640L'
       ]

userName = os.getlogin()
database_directory = "C:/Users/" + userName + "/Documents/證交所櫃買爬蟲資料/stocks.db"
html_directory = "C:/Users/" + userName + "/Documents/證交所櫃買爬蟲資料/HTML檔案/"

'''
users = ['aaronlian', 'lilan', 'tao']

if "compaq" in os.getcwd():
    database_directory = "/home/compaq/Documents/stocks.db"
    html_directory = "/home/compaq/Documents/HTML檔案/"
elif "taocheng" in os.getcwd():
    database_directory = "/home/taocheng/Documents/stocks.db"
    html_directory = "/home/taocheng/Documents/HTML檔案/"
elif "aaron" in os.getcwd():
    database_directory = "C:/Users/blptw/Documents/證交所櫃買爬蟲資料/stocks.db"
    html_directory = "C:/Users/blptw/Documents/證交所櫃買爬蟲資料/HTML檔案/"
else:
    database_directory = "C:/Users/blptw/Documents/證交所櫃買爬蟲資料/stocks.db"
    html_directory = "C:/Users/blptw/Documents/證交所櫃買爬蟲資料/HTML檔案/"
'''

def pathcheckers():
    if os.path.exists(html_directory) is not True:
        os.mkdir(html_directory)
        print(html_directory + " created!")
    else:
        pass

pathcheckers()

def sqlTableCreate():
    '''Creates a basic database'''
    if os.path.exists(database_directory) is not True:
        tableHeader = """日期 text,代號 text,名稱 text,
            外資及陸資買賣超 real,投信買賣超 real,自營商買賣超 real,
            三大法人買賣超合計 real, 均價 real"""
        conn = sqlite3.connect(database_directory)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS {!s} ({!s})'''.format(tableName, tableHeader))
        conn.commit()
        c.close()
        conn.close()
        print("Database " + tableName +" created")
    else:
        print("Table : {!s} loaded. ".format(tableName))

sqlTableCreate()

def getData(ticker):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    rank = 1
    print("Date           Ticker\tFINI  \tITC \tProp")
    for row in c.execute("SELECT 日期, 代號, 均價, 外資及陸資買賣超,投信買賣超,自營商買賣超 FROM 三大法人 WHERE 代號='{!s}' ORDER BY 日期 DESC LIMIT 20".format(ticker)):
        print("{}: {}  {}\t{:>12,}   {:>12,}   {:>12,}".format(rank, row[0], row[1], int(row[3]), int(row[4]), int(row[5])))
        rank += 1
    c.close()
    conn.close()

def updateData(myTime, ticker, heading, change):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    c.execute("UPDATE 三大法人 SET {!s} = {!s} WHERE 代號='{!s}' AND 日期='{!s}' ".format(heading, change, ticker, myTime ))
    conn.commit()
    c.close()
    conn.close() 

def insertData( tableName, header, data):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    c.execute("INSERT INTO {!s} (!s) VALUES {!s}".format(tableName, header, data))
    conn.commit()
    c.close()
    conn.close() 

def deleteData(myTime):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    c.execute("DELETE FROM 三大法人 WHERE 日期='{!s}' ".format(myTime ))
    conn.commit()
    c.close()
    conn.close() 

def deleteDatabyTicker(ticker):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    c.execute("DELETE FROM 三大法人 WHERE 代號='{!s}' ".format(ticker ))
    conn.commit()
    c.close()
    conn.close() 

'''Main functions start from below'''

def downloadWebpage(url, fileName):
    if "twse" in url:
        req = request.Request(url, data=None, headers=twseHead)
    else:
        req = request.Request(url, data=None, headers=gretaiHead)
    a = request.urlopen(req)
    b = open(html_directory + fileName, "wb+")
    b.write(a.read())
    b.close()
    print("下載完成 : {!s} ...".format(fileName))

def checkFile(sourceWebsite, daysBack):
    '''
    Check if file exists then download if not. 
    '''
    dayBase = date.today()-timedelta(days=daysBack)
    fileDate_TWSEOTC = dayBase.strftime("%Y%m%d")
    dateTWSE = dayBase.strftime("%Y%m%d")
    dateOTC = "{!s}{!s}".format(int(dayBase.strftime("%Y"))-1911, dayBase.strftime("/%m/%d"))
    if date.weekday(dayBase) <= holiNum and dateTWSE not in holidays:
        print("\n檢查檔案中")
        if "twse" in sourceWebsite:
            html_tail = "_TWSE.html"
            html_tailPrice = "_TWSEPrice.html"
            twseH = "http://www.twse.com.tw/fund/T86?response=html&date="
            twseL = "&selectType=ALLBUT0999"
            twsePriceH = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date="
            twsePriceT = "&type=ALLBUT0999"
            xLink = twseH + dateTWSE + twseL
            yLink = twsePriceH + dateTWSE + twsePriceT
            if os.path.exists(html_directory + fileDate_TWSEOTC + html_tail) is not True:
                downloadWebpage(xLink, fileDate_TWSEOTC + html_tail)
                downloadWebpage(yLink, fileDate_TWSEOTC + html_tailPrice)
            else:
                print( fileDate_TWSEOTC + html_tail + "\t" + " alredy exists")
                print( fileDate_TWSEOTC + html_tailPrice + "\t" +" alredy exists")
        else:
            html_tail = "_Gretai.html"
            html_tailPrice = "_GretaiPrice.html"
            gretaiH = "http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_print.php?l=zh-tw&se=EW&t=D&d="
            gretaiL = "&s=0,asc"
            gretaiPriceH = "http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php?l=zh-tw&d="
            gretaiPriceT = "&se=EW&s=0,asc,0"
            xLink = gretaiH + dateOTC + gretaiL
            yLink = gretaiPriceH + dateOTC + gretaiPriceT
            if os.path.exists(html_directory + fileDate_TWSEOTC + html_tail) is not True:
                downloadWebpage(xLink, fileDate_TWSEOTC + html_tail)
                downloadWebpage(yLink, fileDate_TWSEOTC + html_tailPrice)
            else:
                print(fileDate_TWSEOTC + html_tail + "\t" + " alredy exists")
                print(fileDate_TWSEOTC + html_tailPrice + "\t" + " alredy exists")
        time.sleep(2)
   
def stockAvgPrice(market, daysBack):
    '''
    Similar to the database data prepare function, but this time for average price calculations!
    Only roll back 10 days because this is not relaly the point to make this 
    '''
    x = date.today()-timedelta(days=daysBack)
    myDate = x.strftime("%Y%m%d")
    sqlDate = x.strftime("%Y-%m-%d")
    if os.path.exists(html_directory + myDate + "_" + market + "Price.html") and date.weekday(x) <= holiNum:
        soup = bss(open(html_directory + myDate + "_" + market + "Price.html", encoding='UTF-8'), 'html.parser')
        if len(soup.find_all("td")) > 50:
            output = []
            if market == "TWSE":
                full_list = [tds.text.replace(" ","").replace(",","") for tds in soup.find_all("table")[4].find_all("td")]
                for list_point in range(full_list.index("本益比")+1, len(full_list),16):
                    try:
                        output.append([sqlDate, full_list[list_point],full_list[list_point +1], full_list[list_point +2 ], full_list[list_point +4], float(full_list[list_point+4]) / float(full_list[list_point+2])])
                    except ZeroDivisionError:
                        output.append([sqlDate, full_list[list_point],full_list[list_point +1], full_list[list_point +2 ], full_list[list_point +4], 0 ])
            elif market == "Gretai":
                full_list = [tds.text.replace(" ","").replace(",","") for tds in soup.find_all("td")[1:-1]]
                for list_point in range(0, len(full_list),15):
                    try:
                        output.append([sqlDate, full_list[list_point],full_list[list_point+1],full_list[list_point+7],full_list[list_point+8], float(full_list[list_point+8]) / float(full_list[list_point+7])])
                    except ZeroDivisionError:
                        output.append([sqlDate, full_list[list_point],full_list[list_point+1],full_list[list_point+7],full_list[list_point+8], 0])
            return output
            
def listPrep(src, startpoint, columns, sqlTime):
    instList = []
    for list_point in range(startpoint, len(src),columns):
        try:
            instList.append([ sqlTime, src[list_point], src[list_point+1], src[list_point+4], src[list_point+7], src[list_point+8], src[list_point+15] ])
        except ZeroDivisionError:
            instList.append([ sqlTime, src[list_point], src[list_point+1], src[list_point+4], src[list_point+7], src[list_point+8], src[list_point+15] ])
    return instList

def listPrepTWSE(src, startpoint, columns, sqlTime):
    instList = []
    for list_point in range(startpoint, len(src),columns):
        try:
            instList.append([ sqlTime, src[list_point], src[list_point+1], int(src[list_point+4]) + int(src[list_point+7]), src[list_point+10], src[list_point+11], src[list_point+18] ])
        except ZeroDivisionError:
            instList.append([ sqlTime, src[list_point], src[list_point+1], int(src[list_point+4]) + int(src[list_point+7]), src[list_point+10], src[list_point+11], src[list_point+18] ])
    return instList

def listPrepOTC(src, startpoint, columns, sqlTime):
    instList = []
    for list_point in range(startpoint, len(src),columns):
        try:
            instList.append([ sqlTime, src[list_point], src[list_point+1], src[list_point+10], src[list_point+13], src[list_point+22], src[list_point+23] ])
        except ZeroDivisionError:
            instList.append([ sqlTime, src[list_point], src[list_point+1], src[list_point+10], src[list_point+13], src[list_point+22], src[list_point+23] ])
    return instList

def institutionalData(market, daysBack):
    dToday = date.today()
    dTWSE = dToday - date(2017, 12, 15)
    dOTC = dToday - date(2018, 1, 12)
    dayBase = date.today()-timedelta(days=daysBack)
    fileDate_TWSEOTC = dayBase.strftime("%Y%m%d")
    sqlDate = "{!s}".format(dayBase)
    if fileDate_TWSEOTC not in holidays:
        if os.path.exists(html_directory + fileDate_TWSEOTC + "_" + market + "Price.html") and date.weekday(dayBase) <= holiNum:
            soup = bss(open(html_directory + fileDate_TWSEOTC + "_" + market + ".html", encoding='UTF-8'), 'html.parser')
            if len(soup.find_all("td")) > 50:
                full_list = [tds.text.replace(" ","").replace(",","") for tds in soup.find_all("td")]
                if market == "TWSE" and daysBack < dTWSE.days:
                    sp, col = 19, 19
                    return listPrepTWSE(full_list, sp, col, sqlDate)
                elif market == "Gretai" and daysBack < dOTC.days:
                    sp, col = 1, 24
                    return listPrepOTC(full_list[:-1], sp, col, sqlDate)
                else:
                    if market == "TWSE":
                        sp, col = 16, 16
                        return listPrep(full_list, sp, col, sqlDate)
                    elif market == "Gretai":
                        sp, col = 1, 16
                        return listPrep(full_list[:-1], sp, col, sqlDate)
            else:
                print("{!s} {!s} has no data. Download again?".format(market, fileDate_TWSEOTC))
                dAgain = str(input("yes/no?")).lower()
                if dAgain == 'y' or dAgain == "yes":
                    os.remove(html_directory + fileDate_TWSEOTC + "_" + market + ".html")
                    os.remove(html_directory + fileDate_TWSEOTC + "_" + market + "Price.html")
                    checkFile(twse, daysBack)
                    checkFile(gretai, daysBack)

def combine(list1, list2):
    for inst in list1:
        for avg in list2:
            if inst[1] == avg[1]:
                inst.append(avg[5])
            else:
                pass
    return list1

def getForex():
    link = "http://rate.bot.com.tw/xrt?Lang=zh-TW"
    fx_soup = bss(requests.get(link).content, "html.parser")
    fx_data = [ a.text for a in fx_soup.find_all("td")[1:6]]
    fx_result = round((float(fx_data[2]) + float(fx_data[3]))/2, 4)
    print("Forex Rate: {!s}".format(fx_result))
    return fx_result

#forex = float(input("Please enter the USD/TWD forex: "))
forex = getForex()

investorTYpe = {"自營商買賣超" : "Domestic PROP", 
                "投信買賣超":"Domestic ITC", 
                "外資及陸資買賣超":"FINI",
                "DESC":" top net buys", 
                "ASC":" top net sells"}

def countDays(market, ticker):
    cur = sqlite3.connect(database_directory).cursor()
    ind, d = 0 ,  '2017-09-30'
    count2 = []
    if "外資" in market:
        col = 1
    elif "投信" in market:
        col = 2
    else:
        col = 3
    for row in cur.execute("SELECT 日期, {!s} FROM 三大法人 WHERE (日期 BETWEEN '{!s}' AND '{!s}') AND 代號='{!s}'".format(market, d, date.today(), ticker)):
        count2.append([row[0], row[1]])
        print(row)
    while ind < len(count2)-1:
        if count2[ind][col] * count2[ind + 1][col] > 0:
            pass
        else:
            #print(count2[ind], ind+1)
            break
        ind +=1
        return ind

def StockNameAdd(ticker, name):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    c.execute("INSERT INTO 股票名稱 (代號, 名稱) VALUES ('{!s}' , '{!s}')".format(ticker, name))
    conn.commit()
    conn.close()

conn = sqlite3.connect(database_directory)
c = conn.cursor()
tickerDictionary = {}
for row in c.execute("SELECT * FROM 股票名稱"):
    tickerDictionary[row[0]] = row[1]
c.close()
conn.close()

def point72(investor, myTime, direction):
    buys, sells = [], []
    count = []
    ind, d = 0 ,  '2017-10-30'
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    print("\n{!s}{!s}".format(investorTYpe[investor], investorTYpe[direction]))
    print("{!s} {!s} {!s} {!s}".format("Ticker","Name","(USD$M)", "+/-"))
    for row in c.execute("SELECT 日期, 代號, {!s}*均價 FROM 三大法人 WHERE 日期='{!s}' ORDER BY {!s}*均價 {!s} LIMIT 10".format(investor, myTime, investor, direction)):
        if direction  == "DESC":
            buys.append(row)
        else:
            sells.append(row)
        count.append([row[1], round(row[2]/forex/1000000, 1)])
    for stock in count:
        count2 = []
        for row in c.execute("SELECT 日期, {!s} FROM 三大法人 WHERE (日期 BETWEEN '{!s}' AND '{!s}') AND 代號='{!s}' ORDER BY 日期 DESC".format(investor, d, date.today(), stock[0])):
            count2.append([row[0], row[1]])
        for ind in range( len(count2)):
            if count2[ind][1] * count2[ind + 1][1] > 0:
                pass
            else:
                #print(count2[ind], ind+1)
                break
            #ind +=1
            #print(ind)
        stock.append(ind+1)
    c.close()
    conn.close()
    for each in count:
        print("{!s:7}\t{:25}{!s}\t{!s}".format(each[0], tickerDictionary[each[0]], each[1], each[2]))
    print(buys)
    print(sells)

def dailyFlows(investor, myTime, direction):
    count = []
    ind, d = 0 ,  '2018-01-01'
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    print("\n{!s}{!s}".format(investorTYpe[investor], investorTYpe[direction]))
    print("{!s} {!s} {!s} {!s}".format("Ticker","Name","(USD$M)", "+/-"))
    for row in c.execute("SELECT 日期, 代號, {!s}*均價 FROM 三大法人 WHERE 日期='{!s}' ORDER BY {!s}*均價 {!s} LIMIT 10".format(investor, myTime, investor, direction)):
        count.append([row[1], round(row[2]/forex/1000000, 1)])
    for stock in count:
        count2 = []
        for row in c.execute("SELECT 日期, {!s} FROM 三大法人 WHERE (日期 BETWEEN '{!s}' AND '{!s}') AND 代號='{!s}' ORDER BY 日期 DESC".format(investor, d, date.today(), stock[0])):
            count2.append([row[0], row[1]])
            #print(count2)
        if len(count2) > 1:
            for ind in range( len(count2)-1):
                if count2[ind][1] * count2[ind + 1][1] > 0:
                    pass
                else:
                    break
            stock.append(ind+1)
    c.close()
    conn.close()
    for each in count:
        #print(tickerDictionary[each[0]])
        print("{!s:7}\t{:25}{!s}\t{!s}".format(each[0], tickerDictionary[each[0]], each[1], each[2]))

#change the 26 you see above to change the padding. The dictionary is also in there. 

def dailyFlowsDebug(investor, myTime, direction):
    count = []
    ind, d = 0 ,  '2018-01-01'
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    print("\n{!s}{!s}".format(investorTYpe[investor], investorTYpe[direction]))
    print("{!s} {!s} {!s} {!s}".format("Ticker","Name","(USD$M)", "+/-"))
    for row in c.execute("SELECT 日期, 代號, {!s}*均價 FROM 三大法人 WHERE 日期='{!s}' ORDER BY {!s}*均價 {!s} LIMIT 10".format(investor, myTime, investor, direction)):
        count.append([row[1], round(row[2]/forex/1000000, 1)])
    for stock in count:
        count2 = []
        for row in c.execute("SELECT 日期, {!s} FROM 三大法人 WHERE (日期 BETWEEN '{!s}' AND '{!s}') AND 代號='{!s}' ORDER BY 日期 DESC".format(investor, d, date.today(), stock[0])):
            count2.append([row[0], row[1]])
        #print(count2)
        if len(count2) > 1:
            for ind in range( len(count2)-1):
                if count2[ind][1] * count2[ind + 1][1] > 0:
                    pass
                else:
                    break
            stock.append(ind+1)
    c.close()
    conn.close()
    for each in count:
        print("{!s:7}\t{:25}{!s}\t{!s}".format(each[0], tickerDictionary[each[0]], each[1], each[2]))

def showDay(oneDay):
    dailyFlows("外資及陸資買賣超", oneDay, "DESC")
    dailyFlows("外資及陸資買賣超", oneDay, "ASC")
    dailyFlows("投信買賣超", oneDay, "DESC")
    dailyFlows("投信買賣超", oneDay, "ASC")
    dailyFlows("自營商買賣超", oneDay, "DESC")
    dailyFlows("自營商買賣超", oneDay, "ASC")

def FiveDayFlows(investor, myTime, direction):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    print("\n{!s} 5-day{!s}".format(investorTYpe[investor], investorTYpe[direction]))
    print("{!s} {!s} {!s}".format("Ticker","Name","(USD$M)"))
    for row in c.execute("SELECT 日期, 代號, sum({!s}*均價) FROM 三大法人 WHERE (日期 BETWEEN '{!s}' AND '{!s}') GROUP BY 代號 ORDER BY sum({!s}*均價) {!s} LIMIT 30".format(investor, myTime, date.today(), investor, direction)):
        if row[1] not in etf:
            print("{!s} {!s} \t{!s}".format(row[1], tickerDictionary[row[1]], round(row[2]/forex/1000000, 1)))
    c.close()
    conn.close()

def function1():
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    for days in range(0,1,1):
        checkFile(twse, days)
        checkFile(gretai, days)
        if institutionalData("TWSE", days) != None:
            c.executemany("INSERT OR IGNORE INTO 三大法人 (日期,代號,名稱,外資及陸資買賣超,投信買賣超,自營商買賣超,三大法人買賣超合計, 均價) VALUES (?,?,?,?,?,?,?,?)",combine(institutionalData("TWSE", days), stockAvgPrice("TWSE", days)))
            c.executemany("INSERT OR IGNORE INTO 三大法人 (日期,代號,名稱,外資及陸資買賣超,投信買賣超,自營商買賣超,三大法人買賣超合計, 均價) VALUES (?,?,?,?,?,?,?,?)",combine(institutionalData("Gretai", days), stockAvgPrice("Gretai", days)))
    c.close()
    conn.commit()
    conn.close()
    print("資料輸入完成！")

def function2():
    查詢日 = input("請輸入往前第五日查詢日期. 格式: 'yyyy-mm-dd'：")
    showDay(date.today())
    print("\n***TW Institutional 5-Day Fund Flows {!s}***".format(date.today().strftime("%Y%m%d")))
    FiveDayFlows("外資及陸資買賣超", 查詢日, "DESC")
    FiveDayFlows("外資及陸資買賣超", 查詢日, "ASC")
    FiveDayFlows("投信買賣超", 查詢日, "DESC")
    FiveDayFlows("投信買賣超", 查詢日, "ASC")
    FiveDayFlows("自營商買賣超", 查詢日, "DESC")
    FiveDayFlows("自營商買賣超", 查詢日, "ASC")

def function72():
    dailyFlows("外資及陸資買賣超", date.today(), "DESC")
    dailyFlows("外資及陸資買賣超", date.today(), "ASC")
    dailyFlows("投信買賣超", date.today(), "DESC")
    dailyFlows("投信買賣超", date.today(), "ASC")
    dailyFlows("自營商買賣超", date.today(), "DESC")
    dailyFlows("自營商買賣超", date.today(), "ASC")

def functionDays(days):
    conn = sqlite3.connect(database_directory)
    c = conn.cursor()
    for days in range(1,days,1):
        checkFile(twse, days)
        checkFile(gretai, days)
        if institutionalData("TWSE", days) != None:
            c.executemany("INSERT OR IGNORE INTO 三大法人 (日期,代號,名稱,外資及陸資買賣超,投信買賣超,自營商買賣超,三大法人買賣超合計, 均價) VALUES (?,?,?,?,?,?,?,?)",combine(institutionalData("TWSE", days), stockAvgPrice("TWSE", days)))
            c.executemany("INSERT OR IGNORE INTO 三大法人 (日期,代號,名稱,外資及陸資買賣超,投信買賣超,自營商買賣超,三大法人買賣超合計, 均價) VALUES (?,?,?,?,?,?,?,?)",combine(institutionalData("Gretai", days), stockAvgPrice("Gretai", days)))
    c.close()
    conn.commit()
    conn.close()
    print("{!s}筆資料輸入完成！".format(days))

def webpageToList(url, begin, delimit):
    #This is hard coded for TAIFEX website only
    soup = bss(requests.get(url).content, "html.parser")
    data = []
    for tag in soup.find_all("td")[begin:-1:delimit]:
        data.append(tag.text.replace(" ",""))
    return data

while True:
    if __name__ == "__main__":    
        print("********{!s}********".format("Database TWSE/OTC"))
        userChoice = int(input("請選擇功能:\n1. 更新今日資料. \n2. 製作今日資料. \n3. 指定單日資料\n"))
        if userChoice == 1:
            function1()
            deleteDatabyTicker('2881B')
            deleteDatabyTicker('2838A')
            deleteDatabyTicker('2882B')
            userChoice = int(input("請選擇功能:\n1. 更新今日資料. \n2. 製作今日資料. \n3. 指定單日資料\n輸入其他數字鍵跳出程式"))
            if userChoice == 1:
                function1()
            elif userChoice == 2:
                function2()
            elif userChoice == 3:
                userDate = input("請選定查詢日期. 格式: 'yyyy-mm-dd'：")
                showDay(userDate)
        elif userChoice == 2:
            function2()
        elif userChoice == 3:
            userDate = input("請選定查詢日期. 格式: 'yyyy-mm-dd'：")
            showDay(userDate)
        elif userChoice == 5:
            print("重新下載資料, 往回150天")
            functionDays(170)
        elif userChoice == 72:
            function72()
        else:
            print("You have entered an option not listed in the menu. \nPlease re-run the program")
            break
