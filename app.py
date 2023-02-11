from functionalities import encrypt, putComplain, verifyLogin, addUser
from flask import Flask, render_template, request, flash, session
app = Flask(__name__)
app.secret_key = "sessionKey"

@app.route('/')
@app.route('/mainHome')                    #homePage
def mainHome():
    return render_template('/mainHome.html')

@app.route('/signup')                      #signup.html
def signup():
    return render_template('/signup.html')      

@app.route('/verify', methods=['POST'])    #login verify and redirection
def verify():
    if verifyLogin(request.form['logemail'], encrypt(request.form['pswd'])):
        return render_template('/userModule.html',email=request.form['logemail'])
    else:
        flash("Invalid Credentials!","error")
        return render_template('/mainHome.html')

@app.route('/newUser', methods=['POST'])   #adding user to DB
def newUser():
    if addUser(request.form['email'], encrypt(request.form['pwd1']), encrypt(request.form['pwd2'])):
        return render_template('/userModule.html',email=request.form['email'])
    else:
        return render_template('/signup.html')

@app.route('/userModule', methods=['POST'])   #adding complaint
def newComplain():
    mail=request.form['email']
    putComplain(request.form['complain'] ,mail)
    return render_template('/userModule.html',email=mail)

@app.route('/admin')
def admin():
    return render_template('/adminModule.html')

@app.route('/logout')
def logout():
    flash("Logged Out","success")
    return render_template('/mainHome.html')

@app.errorhandler(404)      #to handle any non-specified endpoint
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()