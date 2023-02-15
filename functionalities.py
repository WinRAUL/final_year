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
            flash("Invalid Credentials!","error")
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

def getComplaints():
    try:
        myCursor.execute("select * from dataset ORDER BY Complains DESC LIMIT 20 ")
        res = myCursor.fetchall()
        myCursor.reset()
        return res
    except Error as e:
        flash(e,"error")
        return ()
        
def putComplain(complainString, result, email):
    if(complainString==''):
        flash("Empty response not acceptable","error")
        return
    try:
        myCursor = conn.cursor()
        val = (complainString,) + tuple(result) + (email,)
        myCursor.execute("insert into dataset values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",val)
        conn.commit()
        flash("Submitted Succesfully","success")
    except Error as e:
        conn.rollback()
        flash(e,"error")