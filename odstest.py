'''
Author : Ling, Cheng-Nan
Email : nan800130@gmail.com
Create Time : 17, Aug. 2018
Last Modified : 22, Aug. 2018
'''
#import module here
import pymssql
import datetime 

#===================================
##set server, username, password,and database
server   = '128.110.13.89'  
username = '011341' 
password = 'sam341' 
database = 'ODS'
#===================================

#connect with the ODS Database
conn = pymssql.connect(server, username, password, database)
cursor = conn.cursor()

#ST_Query coded here
ST_Query = """
---declare the local variables---
DECLARE @FORMER_MTH_D char(8)
DECLARE @DIFF int

---determine the former match date by the weekday today---
SET @DIFF = 1
IF( DATEPART(WEEKDAY,GETDATE()) = 1 ) SET @DIFF = 3;
SET @FORMER_MTH_D = CONVERT(char(8),GETDATE()-@DIFF,112)

---how many different S_IDNO matched in the ST_Table on the former match day---
SELECT COUNT (DISTINCT ST_CUSTOMER.S_IDNO) FROM ST_CUSTOMER 
INNER JOIN ST_MATCH_D ON (ST_MATCH_D.BROKER_NO3 = ST_CUSTOMER.BROKER_NO3) AND (ST_MATCH_D.S_ACNO = ST_CUSTOMER.S_ACNO)
WHERE MTH_DATE = @FORMER_MTH_D

"""

#WF_Query coded here (total distinct S_IDNO = 55934)
WF_Query = """
---declare the local variables---
DECLARE @FORMER_MTH_D char(8)
DECLARE @DIFF int

---determine the former match date by the weekday today---
SET @DIFF = 1
IF( DATEPART(WEEKDAY,GETDATE()) = 1 ) SET @DIFF = 3;
SET @FORMER_MTH_D = CONVERT(char(8),GETDATE()-@DIFF,112)

---how many different S_IDNO matched in the WF_Table on the former match day---
SELECT COUNT (DISTINCT WF_CUSTOMER.S_IDNO) FROM WF_CUSTOMER 
INNER JOIN WF_MATCH_D ON WF_MATCH_D.S_IDNO = WF_CUSTOMER.S_IDNO --S_IDNO is the key for both table WF_CUSTOMER & WF_MATCH_D
WHERE TDATE = @FORMER_MTH_D

"""

#FU_Query coded here
FU_Query = """
---declare the local variables---
DECLARE @FORMER_MTH_D char(8)
DECLARE @DIFF int

---determine the former match date by the weekday today---
SET @DIFF = 1
IF( DATEPART(WEEKDAY,GETDATE()) = 1 ) SET @DIFF = 3;
SET @FORMER_MTH_D = CONVERT(char(8),GETDATE()-@DIFF,112)

---how many different S_IDNO matched in the FU_Table on the former match day---
SELECT COUNT (DISTINCT FU_CUSTOMER.S_IDNO) FROM FU_CUSTOMER 
INNER JOIN FU_MATCH_D ON (FU_CUSTOMER.FU_BROKER_NO4 = FU_MATCH_D.FU_BROKER_NO4) AND (FU_CUSTOMER.FU_ACNO_1 = FU_MATCH_D.FU_ACNO_1)
WHERE MTH_DATE = @FORMER_MTH_D

"""

#SUB_Query coded here
SUB_Query = """
---declare the local variables---
DECLARE @FORMER_MTH_D char(8)
DECLARE @DIFF int

---determine the former match date by the weekday today---
SET @DIFF = 1
IF( DATEPART(WEEKDAY,GETDATE()) = 1 ) SET @DIFF = 3;
SET @FORMER_MTH_D = CONVERT(char(8),GETDATE()-@DIFF,112)

---how many different S_IDNO matched in the SUB_Table on the former match day---
SELECT COUNT (DISTINCT SUB_CUSTOMER.S_IDNO) FROM SUB_CUSTOMER 
INNER JOIN SUB_MATCH_D ON (SUB_MATCH_D.BROKER_NO4 = SUB_CUSTOMER.BROKER_NO4) AND (SUB_MATCH_D.S_ACNO = SUB_CUSTOMER.S_ACNO)
WHERE MTH_DATE = @FORMER_MTH_D

"""

##=========================== execute the SQL code below ===========================##
#execute the ST_Query code;  #fetch all fetched ST data, assign to the variable ST_data
cursor.execute(ST_Query);    ST_data = cursor.fetchone(); 

#execute the WF_Query code;  #fetch all fetched WF data, assign to the variable WF_data
cursor.execute(WF_Query);    WF_data = cursor.fetchone(); 

#execute the FU_Query code;  #fetch all fetched FU data, assign to the variable FU_data
cursor.execute(FU_Query);    FU_data = cursor.fetchone(); 

#execute the SUB_Query code; #fetch all fetched SUB data, assign to the variable SUB_data
cursor.execute(SUB_Query);   SUB_data = cursor.fetchone(); 

##=========================== print the final result on the console ===========================##
'''
print("DATE : %s"  %  datetime.date.today().strftime("%Y%m%d"))
print("  ST : %5d" %  ST_data)
print("  WF : %5d" %  WF_data)
print("  FU : %5d" %  FU_data)
print(" SUB : %5d" % SUB_data)
'''

print("DATE : %s"  %  datetime.date.today().strftime("%Y%m%d\n")+"  ST : %5d\n" % ST_data + "  WF : %5d\n" % WF_data + "  FU : %5d\n" % FU_data + " SUB : %5d\n" % SUB_data)

#commit
conn.commit()
print('======commit finished======')

#diconnect the Database
conn.close()
print('Database Closed.......')

