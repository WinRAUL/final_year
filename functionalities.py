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
        myCursor.execute("select Complains,User from dataset ORDER BY Complains DESC LIMIT 20 ")
        res = myCursor.fetchall()
        myCursor.reset()
        return res
    except Error as e:
        flash(e,"error")
        return ()

# def putComplain(complainString,email):        #old
#     if(complainString==''):
#         flash("Empty response not acceptable","error")
#         return
#     try:
#         myCursor = conn.cursor()
#         myCursor.execute("insert into complaints(`Complains`, `Department`, `User`) values(%s,%s,%s)",(complainString,'dept',email))  #2nd param is a tuple
#         flash("Submitted succesfully","success")
#         conn.commit()
#     except Error as e:
#         flash("Submition Failed","error")
#         conn.rollback()

        
def putComplain(complainString, result, email):          #new
    if(complainString==''):
        flash("Empty response not acceptable","error")
        return
    try:
        myCursor = conn.cursor()
        # cols = ("Complains", "Road Department", "Sewage Maintenance", "Electric Department", "Water Department", "Waste Management", "Urban Amenities", "Public Toilets", "Disposal of Dead Animals", "Pest Control", "User")
        val = (complainString,) + tuple(result) + (email,)
        myCursor.execute("insert into dataset values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",val)
        # conn.commit()
        # flash("Submitted Succesfully","success")
        print("Submitted Succesfully")
        print(val)
    except Error as e:
        print(e)
        conn.rollback()
        flash("Submition Failed","error")
    finally:
        conn.close()

# putComplain("the roads are in bad shape",[1,0,1,0,1,0,1,0,1],"mymail@mail.com")