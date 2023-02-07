from functionalities import encrypt, putComplain, verifyLogin, addUser
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = "sessionKey"

@app.route('/')
@app.route('/mainHome')                    #homePage
def index():
    return render_template('/mainHome.html')

@app.route('/signup')                      #signup.html
def signup():
    return render_template('/signup.html')      

@app.route('/login')                       #login.html == mainHome.html
def login():
    return render_template('/mainHome.html')

@app.route('/verify', methods=['POST'])    #login verify and redirection
def verify():
    if verifyLogin(request.form['logemail'], encrypt(request.form['pswd'])):
        return render_template('/userModule.html')
    else:
        flash("Invalid Credentials!")
        return render_template('/mainHome.html')

@app.route('/newUser', methods=['POST'])        #adding user to DB
def newUser():
    if addUser(request.form['email'], encrypt(request.form['pwd1']), encrypt(request.form['pwd2'])):
        return render_template('/userModule.html')
    else:
        flash("Password is not matching!")
        return render_template('/signup.html')

@app.route('/index')
def userMod():
    return render_template('/index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()