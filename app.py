from flask import Flask,render_template,url_for,request,session,redirect
from flask_pymongo import PyMongo
import bcrypt

app=Flask(__name__)

app.config['MONGO_DBNAME']='login-pymongo'
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds223738.mlab.com:23738/login-pymongo'

mongo=PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as'    +  session['username']

    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    users=mongo.db.Login
    login_user=users.find_one({'name':request.form['username']})
    
        
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['Password'])== login_user['Password']:
            session['username']=request.form['username']
            return redirect(url_for('index'))


    return'invalid username/password combination'
                
@app.route('/register',methods=['POST','GET'])

def register():
    if request.method=='POST':
        users=mongo.db.Login
        existing_user=users.find_one({'name':request.form['username']})
        
        if existing_user is None:
            hashpass=bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
            users.insert({'name':request.form['username'],'Password':hashpass})
            session['username']=request.form['username']
            return redirect(url_for('index'))


        return'That Username already exists!'
    
    
    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key='MySecret'
    app.run(debug=True)