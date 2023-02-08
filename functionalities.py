import mysql.connector, hashlib
from mysql.connector import Error
from flask import flash
conn = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "ProjectDB"
)
myCursor = conn.cursor()


def putComplain(complainString,dept,user):
    if(complainString==''):
        flash("Empty request not acceptable")
        return
    myCursor = conn.cursor()
    try:
        myCursor.execute("insert into complaints(`Complains`, `Department`, `User`) values(%s,%s,%s)",(complainString,dept,user))  #2nd param is a tuple
        flash("Submitted succesfully","success")
        conn.commit()
    except Error as e:
        flash("Submition Failed",'error')
        conn.rollback()
    
def encrypt(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

def verifyLogin(email, password):
    myCursor.execute("select * from users where Email=%s AND Pass=%s",(email,password))
    res = myCursor.fetchall()
    if(bool(res)):
        return True
    else:
        return False

def addUser(email, pwd1, pwd2):
        if pwd1!=pwd2:
            flash("Password is not matching!")
            return False
        else:
            # if 1==2:
            if (myCursor.execute("insert into users(email,pass) values(%s,%s)",(email,pwd1))):
                conn.commit()
                print("user added")
                return True
            else:
                flash("Email alrerady in use")
                return False

# def getComplaints():