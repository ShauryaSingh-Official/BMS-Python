from asyncio.windows_events import NULL
from distutils.util import execute
import mysql.connector
from time import sleep

try:
    conn= mysql.connector.connect(user='root', password='Sour@1508', host='localhost',database ='BMSDatabase', port=3306 )
    if(conn.is_connected()):
        print("Connected")   
except:
    print('Unable to connect database')


def inputEmpFields():
    dept = input(" Enter Department Name : ")
    emp = input(" Enter Employee Name   : ")
    if dept=="CHITAYI" :
        item = input(" Enter Product Id      : ")
    else :
        item = "COMMON"
    rs = int(input("Enter production Rs. (per kg or hrs or pc) : "))
    params = (dept, emp, item, rs)
    return params 


def newEmployee():
    params = inputEmpFields()
    sql = "INSERT INTO EMPLOYEE(DEPT_NAME, E_NAME, ITEM_ID, RS_PRODUCTION) VALUES(?,?,?,?) "
    myc= conn.cursor(prepared=True)
    myc.execute(sql, params)
    conn.commit()
    myc.close()
    print("1 Row inserted ! ")


def showEmployee():
    sql= "SELECT * FROM EMPLOYEE"
    myc= conn.cursor()
    myc.execute(sql)
    row = myc.fetchone()
    print("______________________________________________________________________")
    print("                    ALL EMPLOYEES LIST                    ")
    print("----------------------------------------------------------------------")
    print( "E_ID \tDEPT_NAME\tE_NAME\t\tPRODUCT_ID\tRS_PRODUCTION" )
    print("----------------------------------------------------------------------")
    while row is not None :
        if len(row[1]) <= 6 :
            print( str(row[0]) + "\t" + row[1] +"\t\t" + str(row[2]) + "\t" + row[3] + "\t\t" + str(row[4]) )
        else :
            print( str(row[0]) + "\t" + row[1] +"\t\t" + str(row[2]) + "\t\t" + row[3] + "\t\t" + str(row[4]) )
        row = myc.fetchone()
    print("______________________________________________________________________")
    myc.close()


def inputWorkFields():
    emp = input(" Enter Employee Name                           : ")
    wtorhrsorNo = float(input(" Enter Work weight/hours/no.of pcs             : "))
    item = input(" Enter Product Id                              : ")
    query = " SELECT DEPT_NAME FROM EMPLOYEE WHERE E_NAME = %s "
    myc1 = conn.cursor()
    param = (emp,)
    myc1.execute(query,param)
    dept = myc1.fetchone()
    if dept=="CHITAYI" :
        sql = ' SELECT RS_PRODUCTION FROM EMPLOYEE WHERE E_NAME = %s AND ITEM_ID= %s '
        params = (emp,item)
    else :
        sql = ' SELECT RS_PRODUCTION FROM EMPLOYEE WHERE E_NAME = %s AND ITEM_ID= "COMMON" '
        params = (emp,)
    myc = conn.cursor()
    myc.execute(sql,params)
    row = myc.fetchone()
    rs = row[0]
    total_amt = float(rs*wtorhrsorNo)
    myc.close()
    pay = float(input(" Enter Pay Amount to Worker                    : "))
    date = input(" Enter Current Date [Use Format : yyyy-mm-dd ] : ")
    paramS = (emp, item, wtorhrsorNo, total_amt, pay, date)
    return paramS


def exeSql(params) :
    sql= "INSERT INTO WORK( E_NAME, ITEM_ID, WEIGHTo_HOURS_NO_OF_PCS, TOTAL_AMT, PAID_AMT, DATE_ ) VALUES(?,?,?,?,?,?) "
    myc= conn.cursor(prepared=True)
    myc.execute(sql, params)
    conn.commit()
    myc.close()

def newWork():
    print("")
    params = inputWorkFields()
    exeSql(params)
    print("1 Row inserted ! ")


def empPay() :
    emp = input(" Employee Name                            : ")
    amt = float(input(" Pay Amount                               : "))
    date = input(" Current Date [ Use Format : yyyy-mm-dd ] : ")
    params = ( emp, "----", 0, 0, amt, date )
    exeSql(params)


def showWork():
    sql= "SELECT * FROM WORK"
    myc= conn.cursor()
    myc.execute(sql)
    row = myc.fetchone()
    print("___________________________________________________________________________________________________________________")
    print("                                             ALL EMPLOYEE'S WORK RECORD                                             ")
    print("-------------------------------------------------------------------------------------------------------------------")
    print( "S_NO\t\tE_NAME\t\tITEM_ID\t\tWEIGHTo_HOURS_NO_OF_PCS\tTOTAL_AMT\tPAID_AMT\tDATE_ " )
    print("-------------------------------------------------------------------------------------------------------------------")
    while row is not None :
        if len(row[1])>6:
            print( str(row[0]) + "\t" + str(row[1]) +"\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t\t\t" + str(row[4]) + "\t\t" + str(row[5]) + "\t\t" + str(row[6]) )
        else :
             print( str(row[0]) + "\t" + str(row[1]) +"\t\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t\t\t" + str(row[4]) + "\t\t" + str(row[5]) + "\t\t" + str(row[6]) )
        row = myc.fetchone()
    print("___________________________________________________________________________________________________________________")
    myc.close()


def generateEmpBill() :
    print("_____________________________________________________________________________________")
    print("                                   EMPLOYEE BILL                                     ")
    print("\t\t\t।। 🙏  राधे राधे ।। जय श्री महाकाल  🙏 ।।")
    print("_____________________________________________________________________________________")
    emp = input(" Employee Name : ")
    sql = " SELECT * FROM WORK WHERE E_NAME = %s "
    param = (emp,)
    myc = conn.cursor()
    myc.execute(sql,param)
    row = myc.fetchone()
    print(" From Date     : " + str(row[6]))
    print("_____________________________________________________________________________________")
    print("PRODUCT_ID\tWEIGHTorHOURSorNO_OF_PCS\tWORK_AMOUNT\tPAID\t DATE ")
    print("-------------------------------------------------------------------------------------")
    total_wtorhrs = 0
    total_work_amt = 0
    total_pay = 0
    while row is not None :
        if len(row[2]) > 7 :
            print( str(row[2]) + "\t" + str(row[3]) + "\t\t\t\t" + str(row[4]) + "\t\t" + str(row[5]) + "\t " + str(row[6]) )
        else :
            print( str(row[2]) + "\t\t" + str(row[3]) + "\t\t\t\t" + str(row[4]) + "\t\t" + str(row[5]) + "\t " + str(row[6]) )
        total_wtorhrs = total_wtorhrs + row[3]
        total_work_amt = total_work_amt + row[4]
        total_pay = total_pay + row[5]
        row = myc.fetchone()
    print("_____________________________________________________________________________________")
    print("\t\tTOTAL : WEIGHT/HOURS/PCS \tWORK_AMOUNT \tPAY \t|  BALANCE  |")
    print("------------------------------------------------------------------------|___________|")
    balance = total_work_amt - total_pay
    print( "\t\t\t" + str(total_wtorhrs) + "\t\t\t"  + str(total_work_amt) + "\t\t" + str(total_pay) + "\t|  " + str(balance)+"  |" )
    print("\t\t\t\t\t\t\t\t\t|___________|")
    print("\t\t\t\t\t\t\t AUTHORISED BY:- Sourav Kumar")
    print("\t\t\t\t\t\t\t\t\t( Shauraya )")
    print("_____________________________________________________________________________________")
    myc.close()

# newEmployee()
# showEmployee()

# newEmployee()
# showEmployee()

# newEmployee()
# showEmployee()

# newEmployee()
# showEmployee()

# newWork()
# showWork()

# generateEmpBill()


###################################################################################################################################################


def inputFields(fn_id) :
    if fn_id=="saleRecord" :
        party      =       input(" Enter Party Name                         : ")
        product_id =       input(" Enter Product Id                         : ")
        p_brass    = float(input(" Enter Party Brass ( Provided Us )\n [ NOTE : If not provided then use '0' ]  : "))
        rs         = float(input(" Enter Production Price ( per kg )        : "))
        wt         = float(input(" Enter Weight ( Product )                 : "))
        payable = rs*wt
        paid       = float(input(" Enter Paid Amount                        : "))
        date       =       input(" Current Date [ Use Format : yyyy-mm-dd ] : ")
        params = (party, product_id, p_brass, rs, wt, payable, paid, date) 
        return params
    
    if fn_id == "salepayorbrass" :
        typ = str(input(" Enter Pay Type (Press : ' 1 ' or ' AMOUNT PAID ' ,  ' 2 ' or ' BRASS ' ) : "))
        party = input(" Enter Party Name                         : ")
        if typ ==  "1"  or typ == "AMOUNT PAID" :
          paid = float(input(" Enter Paid Amount                        : "))
          l = [party, "----\t ", 0, 0, 0, 0, paid ]  
        elif typ ==  "2"  or typ == "BRASS" :
            p_brass = float(input(" Enter Party Brass ( Provided Us )        : "))
            l = [party,'----\t ' , p_brass, 0, 0, 0, 0 ]
        else :
            print(" PLEASE ENTER VALID OPTION !! ")
            inputFields(fn_id)
        date = input(" Current Date [ Use Format : yyyy-mm-dd ] : ")
        params = ( l[0] , l[1], l[2], l[3], l[4], l[5], l[6],  date )
        return params


def saleRecord() :
    fn_id = "saleRecord"
    params = inputFields(fn_id)
    sql = "INSERT INTO PARTY_RECORD(PARTY, PRODUCT_ID, P_BRASS, RS, WEIGHT, PAYABLE_AMT , PAID, DATE_) VALUES(?,?,?,?,?,?,?,?) "
    myc = conn.cursor(prepared = True)
    myc.execute(sql, params)
    conn.commit()
    myc.close()
    print("1 Row inserted to Work Record ! ")


def printRecord(row) :
    if len(row[0]) >= 15 :
        if row[1] == "----\t ":
            print( row[0] + "\t" + row[1] +"\t\t\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t\t" + str(row[6]) + "\t " + str(row[7]) )
        elif len(row[1]) <= 10 :
            print( row[0] + "\t" + row[1] +"\t\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t" + str(row[6]) + "\t " + str(row[7]) )
        else :
            print( row[0] + "\t" + row[1] +"\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t" + str(row[6]) + "\t " + str(row[7]) )
    else :
        if row[1] == "----\t ":
            print( row[0] + "\t\t" + row[1] +"\t\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t\t" + str(row[6]) + "\t " + str(row[7]) )
        elif len(row[1]) <= 10 :
            print( row[0] + "\t\t" + row[1] +"\t\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t" + str(row[6]) + "\t " + str(row[7]) )
        else :
            print( row[0] + "\t\t" + row[1] +"\t" + str(row[2]) + " \t  " + str(row[3]) + "\t  " + str(row[4]) + "\t " + str(row[5]) + "\t" + str(row[6]) + "\t " + str(row[7]) )


def showPartyRecords() :
    sql= "SELECT * FROM PARTY_RECORD"
    myc= conn.cursor()
    myc.execute(sql)
    row = myc.fetchone()
    print("___________________________________________________________________________________________________________")
    print("                                             ALL PARTY RECORDS                                             ")
    print("-----------------------------------------------------------------------------------------------------------")
    print( "PARTY\t\t\tPRODUCT_ID\t\tP_BRASS\t  RS\t WEIGHT\t PAYABLE_AMT\tPAID\t DATE " )
    print("-----------------------------------------------------------------------------------------------------------")
    while row is not None :
        printRecord(row)
        row = myc.fetchone()
    print("___________________________________________________________________________________________________________")
    myc.close()



def showPartyRecord() :
    name = input(" Party Name  : ")
    sql= "SELECT * FROM PARTY_RECORD WHERE PARTY = %s "
    param = (name,)
    myc= conn.cursor()
    myc.execute( sql, param )
    row = myc.fetchone()
    print(" From Date   : ALL ")
    print("____________________________________________________________________________________________________________")
    # print("                                                PARTY RECORD                                                ")
    # print("------------------------------------------------------------------------------------------------------------")
    print( "PARTY\t\t\tPRODUCT_ID\t\tP_BRASS\t  RS\t WEIGHT\t PAYABLE_AMT\tPAID\t DATE " )
    print("------------------------------------------------------------------------------------------------------------")
    t_pb = 0
    t_wt = 0
    t_pa = 0
    t_p = 0
    while row is not None :
        printRecord(row)
        t_pb = t_pb + row[2]
        t_wt = t_wt + row[4]
        t_pa = t_pa + row[5]
        t_p = t_p + row[6]
        row = myc.fetchone()
    print("____________________________________________________________________________________________________________")
    myc.close()
    total_data = (t_pb, t_wt, t_pa, t_p)
    return total_data


def getPartyBill():
    print("____________________________________________________________________________________________________________")
    print("                                                    BILL                                                    ")
    print("                                    ।। 🙏  राधे राधे ।। जय श्री महाकाल  🙏 ।।                                    ")
    print("------------------------------------------------------------------------------------------------------------")
    results = showPartyRecord()
    print( "\t\t\t\t\tTOTAL :\tP_BRASS\t\t WEIGHT\t PAYABLE_AMT\tPAID " )
    print("------------------------------------------------------------------------------------------------------------")
    print( "\t\t\t\t\t\t" + str(results[0]) + "\t\t " + str( round((results[1]),2) ) + "\t " + str(results[2]) + "\t" + str(results[3]) + "\n\n" )
    if results[0]==0 :
        print(" REMAINING PARTY BRSSS : 0 ( NIL )")
    else :    
        print(" REMAINING PARTY BRSSS : " + str( round((results[0] - results[1]),2) ) )
    print(" REMAINING PAY         : " + str( round((results[2] - results[3]),2) ) )
    print("\t\t\t\t\t\t\t\t\t\tAUTHORISED BY:- Sourav Kumar")
    print("\t\t\t\t\t\t\t\t\t\t\t\t( Shauraya )")
    print("____________________________________________________________________________________________________________")


def partyBrassOrPaid() :
    fn_id = "salepayorbrass"
    p  = inputFields(fn_id)
    params =( p[0],p[1], p[2], p[3] , p[4], p[5], p[6], p[7] )
    sql = " INSERT INTO PARTY_RECORD(PARTY, PRODUCT_ID, P_BRASS, RS, WEIGHT, PAYABLE_AMT , PAID, DATE_) VALUES(?,?,?,?,?,?,?,?) "
    myc = conn.cursor(prepared = True)
    myc.execute(sql, params)
    conn.commit()
    myc.close()
    print("1 Row inserted to Work Record ! ")   


# saleRecord()
# saleRecord()
# saleRecord()
# saleRecord()
# showPartyRecords()
# partyBrassOrPaid()
# showPartyRecords()
# showPartyRecord()
# getPartyBill()

####################################################################################################################################################


# MAIN FUNCTION

def showEmpOP() :
    i = 1
    while i !=0 :
        print("____________________________________________________________________________________________________________________________________________________\n\n")
        print(" PRESS FOLLOWING DIGIT TO PERFORM AN OPERATION ")
        print(" 1 : Add New Employee to Record \t 3 : Input Work Details \t 5 : Show Work Details      \t 0 : Main Menu ")
        print(" 2 : Show Employee List         \t 4 : Input Employee Pay \t 6 : Generate Employee Bill \t  ")
        selected = int(input(" Enter Here ==> "))
        if selected == 0   :
            i = 0
            return  
        elif selected == 1 : newEmployee() 
        elif selected == 2 : showEmployee()
        elif selected == 3 : newWork()
        elif selected == 4 : empPay()
        elif selected == 5 : showWork()
        elif selected == 6 : generateEmpBill()

def showPartyOP() :
    i = 1
    while i !=0 :
        print("____________________________________________________________________________________________________________________________________________________\n\n")
        print(" PRESS FOLLOWING DIGIT TO PERFORM AN OPERATION ")
        print(" 1 : Add Sale Details                      \t 3 : Show All Sale Records\t\t 5 : Generate Party Bill ")
        print(" 2 : Input Brass/Paymant ( GIVEN BY PARTY )\t 4 : Show Sale Record of a Party\t 0 : Main Menu ")
        selected = int(input(" Enter Here ==> "))
        if selected == 0 :   
            i = 0
            return
        elif selected == 1 : saleRecord() 
        elif selected == 2 : partyBrassOrPaid()
        elif selected == 3 : showPartyRecords()
        elif selected == 4 : showPartyRecord()
        elif selected == 5 : getPartyBill()
        else               : print(" Please provide a valid input !!! ")

flag = 1
while flag != 0 :
    print(" \t\t\t\t\t\t\t\t MAIN MENU ")
    print("____________________________________________________________________________________________________________________________________________________\n\n")
    print(" PRESS FOLLOWING DIGIT TO PERFORM AN OPERATION ")
    print(" 1 : Visit Employee ")                   
    print(" 2 : Visit Parties ")                   
    print(" 0 : Exit")
    selected = int(input(" Enter Here ==> "))
    if selected == 0 :
        print(" Great Job !! Thank you for using me. ")
        sleep(2)
        print("** Bye ** ")
        print("____________________________________________________________________________________________________________________________________________________")
        sleep(1)
        flag = 0
    elif selected == 1 : showEmpOP()
    elif selected == 2 : showPartyOP()
    else               : print(" Please provide a valid input !!! ")

conn.close()