import hashlib
from flask import Flask, render_template, request
from pymongo import MongoClient
client = MongoClient('localhost', 27017)


app = Flask(__name__)


db=client.users

@app.route("/")
def home():    
    return render_template("index.html") 

	
@app.route('/cabinet',methods=['POST'])
def login():
	check=0
	user_name=request.form['user_name']
	user_password=request.form['user_password']
	user_password=hashlib.md5(user_password.encode()).hexdigest()
	for user in db.info.find({"login":user_name,"password":user_password}):
		if user.get("password")==user_password:
			check=1
		else:
			check=0
	if check==1:
			return render_template('cabinet.html',user_name=user_name)
	else:
			return render_template('index.html',error="Invalid login or password")
@app.route('/logout',methods=['POST'])
def logout():
	return render_template('index.html')

@app.route('/register')
def reg():
	return render_template('registration.html')

@app.route('/newuser',methods=['POST'])
def newuser():
	user_name=request.form['user_name']
	user_password=request.form['user_password']
	user_password=hashlib.md5(user_password.encode()).hexdigest()
	user_email=request.form['user_email']
	db.info.insert({"login": user_name, "password": user_password, "e-mail":user_email})
	return render_template('cabinet.html',user_name=user_name)
	
@app.errorhandler(405)
def page_not_found(e):
  return render_template('405.html')
	
if __name__ == "__main__":    
    app.run()
	