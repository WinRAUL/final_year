from putComplain import putComplain, verifyLogin
from flask import Flask, render_template, request
app = Flask(__name__)

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

@app.route('/verify', methods=['POST'])                       #login verify and redirection
def verify():
    if verifyLogin(request.form['logemail'], request.form['pswd']):
        return render_template('/userModule.html')
    else:
        return render_template('/mainHome.html')

@app.route('/newUSer', methods=['POST'])        #to make
def newUser():
    return addUser()


@app.route('/',methods=['POST'] )               #will be mdified later
def sendVal():
    complain = request.form['complain']
    putComplain(complain)
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()