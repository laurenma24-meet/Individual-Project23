from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




config = {
  "apiKey": "AIzaSyD2BQXXECRmnPLSmJ2T39q14isfE4WlN-U",
  "authDomain": "example-9d1d1.firebaseapp.com",
  "projectId": "example-9d1d1",
  "storageBucket": "example-9d1d1.appspot.com",
  "messagingSenderId": "304177667159",
  "appId": "1:304177667159:web:a4f1f95719955ed77d5712",
  "measurementId": "G-KETR296LV3",
  "databaseURL":"https://new3-b23b0-default-rtdb.europe-west1.firebasedatabase.app/"
}




firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



#home
@app.route('/')
def home():
    return render_template('index.html')



#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
    return render_template("signup.html", error=error)





 # signin  
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_task'))
        except:
            error = "Authentication failed"
    return render_template("signin.html", error=error)




#task page
@app.route('/task')
def task():
    return render_template('task.html')





@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form.get('task_name')  
        if task_name:
            db.child("tasks").push({"name": task_name})
    
    tasks = db.child("tasks").get().val()
    if tasks is None:
        tasks = {}  
    return render_template('task.html', tasks=tasks)




@app.route('/remove_task/<task_id>')
def remove_task(task_id):
    db.child("tasks").child(task_id).remove()
    tasks = db.child("tasks").get().val()
    if tasks is None:
        tasks = {}  
    
    return render_template('task.html', tasks=tasks)


@app.route('/profile')
def profile():
    return render_template("profile.html")



if __name__ == '__main__':
    app.run(debug=True)