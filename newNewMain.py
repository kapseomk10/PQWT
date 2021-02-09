import mysql.connector as conn
from datetime import datetime
from urllib.request import Request, urlopen
import certifi
import ssl

mydb = conn.connect(host="192.168.1.108",user="hello1",passwd="hello1", database="hms", auth_plugin='mysql_native_password')

def liveTime():
    now = datetime.now()
    current_time = now.strftime("%H.%M")
    return current_time

def waitTime(task1):
    return sum(waitT[task1])

def serviceTime(pid1,task1):
    sqlx = "select `"+task1+"` from patient where patientID='"+pid1+"'"
    mycursor.execute(sqlx)
    myresult = mycursor.fetchone()
    waitT[task1].append(int(myresult[0]))
    return int(myresult[0])

def diffTime(current_time,arrivalTime):
    currenth,currentm = tuple([int(i) for i in current_time.split(".")])
    arrivalh,arrivalm = tuple([int(j) for j in arrivalTime.split(".")])
    if (currentm>=arrivalm):
        timemin = currentm - arrivalm
        timehr = currenth - arrivalh 
        return str(timehr)+"."+str(timemin) 
    else:
        timemin = 60+currentm - arrivalm 
        currenth-=1 
        timehr = currenth - arrivalh
        return str(timehr)+"."+str(timemin) 

def addTime(current,arrival):
    currenth,currentm = tuple([int(i) for i in current.split(".")])
    arrivalh,arrivalm = tuple([int(j) for j in arrival.split(".")])
    timemin = currentm + arrivalm
    if(timemin>60):
        addh = timemin // 60
        timehr = currenth + arrivalh
        timehr+=addh 
        return str(timehr)+"."+str(timemin) 
    else:
        timehr = currenth + arrivalh
        return str(timehr)+"."+str(timemin) 

while True:
    pid,task=tuple(input().split(" "))

    waitT = { 'Registration':[0],'Check Up':[0],'XRay':[0],'Injection':[0],'CT Scan':[0],'MRI Scan':[0],'Medicine':[0],'Payment':[0] }
    taski = {0:'Registration',1:'Check Up',2:'XRay',3:'Injection',4:'CT Scan',5:'MRI Scan',6:'Medicine',7:'Payment'}

    task=taski[int(task)]

    mycursor = mydb.cursor()
    sql = "select * from patient where patientID='"+pid+"'"
    mycursor.execute(sql)
    myres = mycursor.fetchone()
    print(myres)
    if myres!=None:
        sql1 = "select * from livetasks where patientID='"+pid+"' and task='"+task+"'"
        mycursor.execute(sql1)
        myresult = mycursor.fetchone()
        print(myresult)
        if myresult!=None:
            if(myresult[10]=='waiting'):
                live = liveTime()
                wai = diffTime(live,myresult[9])
                sql3 = "update livetasks set status='inservice',wt='"+wai+"',sat='"+live+"' where patientID='"+pid+"'"
                print(sql3)
                mycursor.execute(sql3)
                mydb.commit()
                stat = 'inservice'
                print("https://hmsprojectdatabase.000webhostapp.com/updateData.php?pid="+pid)
                urlopen("https://hmsprojectdatabase.000webhostapp.com/updateData.php?pid="+pid, context=ssl.create_default_context(cafile=certifi.where()))
            elif(myresult[10]=="inservice"):
                sql4 = "Delete from livetasks where patientID='"+pid+"'"
                print(sql4)
                mycursor.execute(sql4)
                mydb.commit()
                print("https://hmsprojectdatabase.000webhostapp.com/removeData.php?pid="+pid)
                urlopen("https://hmsprojectdatabase.000webhostapp.com/removeData.php?pid="+pid, context=ssl.create_default_context(cafile=certifi.where()))
                #for completedtasks
                arrivalTime = myresult[9]
                endTime = liveTime()
                wto1 = myresult[11]
                sto1 = diffTime(endTime,myresult[12])
                sqlform = "insert into completedtasks(patientID,name,age,gender,task,doctorID,wt,st,tts,at,et) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                patientinfo = [(myres[0],myres[1],myres[2],myres[3],task,'1',wto1,sto1,addTime(wto1,sto1),arrivalTime,endTime)]
                mycursor.executemany(sqlform,patientinfo)
                mydb.commit()
                sql5 = "Delete from patient where patientID='"+pid+"'"
                print(sql5)
                mycursor.execute(sql4)
                mydb.commit()
        else:
            arrivalTime = liveTime()
            wto = waitTime(task)
            sto = serviceTime(pid,task)
            sqlform = "insert into livetasks(patientID,name,age,gender,task,doctorID,pwt,pst,tts,at,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            patientinfo = [(myres[0],myres[1],myres[2],myres[3],task,'1',wto,sto,wto+sto,arrivalTime,'waiting')]
            mycursor.executemany(sqlform,patientinfo)
            mydb.commit()
            stat = 'waiting'
            print("https://hmsprojectdatabase.000webhostapp.com/add_data.php?pid="+pid+"&task="+task.replace(' ','')+"&status="+stat+"&wt="+str(wto)+"&st="+str(sto))
            urlopen("https://hmsprojectdatabase.000webhostapp.com/add_data.php?pid="+pid+"&task="+task.replace(' ','')+"&status="+stat+"&wt="+str(wto)+"&st="+str(sto), context=ssl.create_default_context(cafile=certifi.where()))
    else: 
        print('invalid input')
        #https://hmsprojectdatabase.000webhostapp.com/add_data.php?pid=1&task=Injection&status=waiting&wt=0&st=14