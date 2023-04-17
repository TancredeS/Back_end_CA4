import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, url_for, redirect, session
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"

client = pymongo.MongoClient(
    "mongodb+srv://cafe:yYCEj4BSsl0zgifW@cluster0.lz9tjnm.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
todos = db.todos
records = db.register

# :)
@app.route('/hello_word')
def hello_world():
    return 'Hello, World!'


#this is the function for the home page
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template('index.html')

#this is the function for the register page
@app.route("/register/", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)
    return render_template('register.html')

@app.route('/about/')
def about():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))

    return render_template('about.html')

#this is the function for the login page
@app.route("/login/", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

#if the user is logged in, he will be redirected to this page
@app.route('/logged_in/')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))

#this is the function for the logout page
@app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("sign_out.html")
    else:
        return render_template('index.html')

#this is the function for the todolist page
@app.route('/todolist/', methods=('GET', 'POST'))
def todolist():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('todolist'))

    all_todos = todos.find()
    return render_template('todolist.html', todos=all_todos)

#this is the function to delete an item from the todolist
@app.post('/<id>/delete')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

#this is the function to update an item from the todolist
@app.route('/<id>/update', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"content": content, "degree": degree}})
        return redirect(url_for('index'))
    todo = todos.find_one({"_id": ObjectId(id)})
    return render_template('update.html', todo=todo)

#this runs the app
if __name__ == '__main__':
    app.run()