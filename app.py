from putComplain import putComplain
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'] )
def sendVal():
    complain = request.form['complain']
    putComplain(complain)
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()