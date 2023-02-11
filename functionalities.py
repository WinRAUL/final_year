import mysql.connector, hashlib
from mysql.connector import Error
from flask import flash
def connection():
    return mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "ProjectDB"
)
conn = connection()
myCursor = conn.cursor()

def putComplain(complainString,user):
    if(complainString==''):
        flash("Empty response not acceptable","error")
        return
    try:
        myCursor = conn.cursor()
        myCursor.execute("insert into complaints(`Complains`, `Department`, `User`) values(%s,%s,%s)",(complainString,'dept',user))  #2nd param is a tuple
        flash("Submitted succesfully","success")
        conn.commit()
    except Error as e:
        flash("Submition Failed",'error')
        conn.rollback()
    
def encrypt(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

def verifyLogin(email, password):
    try:
        myCursor.execute("select * from users where Email=%s AND Pass=%s",(email,password))
        res = myCursor.fetchall()
        if(bool(res)):
            return True
        else:
            return False
    except Error as e:
        flash("e","error")
        return False

def addUser(email, pwd1, pwd2):
    if pwd1!=pwd2:
        flash("Password is not matching!")
        return False
    else:
        try:
            myCursor.execute("insert into users(email,pass) values(%s,%s)",(email,pwd1))
            conn.commit()
            return True
        except:
            flash("Email alrerady in use")
            return False

# def getComplaints():