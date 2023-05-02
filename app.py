from functionalities import encrypt, putComplain, verifyLogin, addUser, getComplaints
from flask import Flask, render_template, request, redirect, flash
from classifier import classify
app = Flask(__name__)
app.secret_key = "sessionKey"

@app.route('/')                     #homePage
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
        return redirect('/',302)

@app.route('/newUser', methods=['POST'])   #adding user to DB
def newUser():
    if addUser(request.form['email'], encrypt(request.form['pwd1']), encrypt(request.form['pwd2'])):
        return render_template('/userModule.html', email=request.form['email'])
    else:
        return render_template('/signup.html')

@app.route('/userModule', methods=['POST'])   #user page
def newComplain():
    email=request.form['email']
    complain = (request.form['complain']).strip()
    if (complain==''):
        flash("Empty response not acceptable","error")
        return render_template('/userModule.html', email=email)
    else:
        result = classify(request.form['complain'])
        putComplain(request.form['complain'], result, email)
        return render_template('/userModule.html', email=email)

@app.route('/admin')
def admin():
    # return render_template('/adminModule.html')
    return render_template('/adminModule.html', tuples=getComplaints())

@app.route('/logout')
def logout():
    flash("Logged Out","success")
    return redirect('/')

@app.errorhandler(404)      #to handle any non-specified endpoint
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':                  #app entrypoint
    app.run()