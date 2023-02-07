import mysql.connector, hashlib
conn = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "ProjectDB"
)

def putComplain(complainString):
    myCursor = conn.cursor()
    myCursor.execute("insert into complaints values(%s)",(complainString,))  #2nd param is a tuple
    conn.commit()
    
def encrypt(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

def verifyLogin(email, password):
    myCursor = conn.cursor()
    myCursor.execute("select * from users where Email=%s AND Pass=%s",(email,password))
    res = myCursor.fetchall()
    if(bool(res)):
        return True
    else:
        return False

def addUser(email, pwd1, pwd2):
        if pwd1!=pwd2:
            return False
        else:
            myCursor = conn.cursor()
            myCursor.execute("insert into users(email,pass) values(%s,%s)",(email,pwd1))
            conn.commit()
            print("user added")
            return True

########################
# def putComplain(complainString):
#     myCursor = conn.cursor()
#     myCursor.execute("select * from complaints")
#     res = myCursor.fetchall()
#     for x in res:
#         print(x[0])

#     conn.close()

#to retrieve & print complains from database