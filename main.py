import pymongo
from flask import Flask, request, render_template, url_for, redirect
# from decouple import config
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        action = request.form["action"]
        if action == "signup":
            return render_template("signup.html")
        else:
            return render_template("login.html")

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form["emailId"]
    password = request.form["password"]
    # user = config('user',default='')
    # passwd = config('passwd',default='')
    # DB_CON_URL = f"mongodb+srv://{user}:{passwd}@cluster0.nnfqq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    DB_CON_URL = os.environ.get("MONGO_UAI", None)
    try:
        database = pymongo.MongoClient(DB_CON_URL)
        print("Database connection successful!")

        my_db = database["authentication"]
        coll_name = my_db["signup"]

        cur = coll_name.find({"email": email})

        if cur.count() == 0:
            coll_name.insert_one({"email": email, "password": password})
            print("record inserted successfully")
            return redirect(url_for('success'))
        else:
            print("email already exists!")
            return redirect(url_for('failure'))

    except Exception as e:
        print(str(e))
@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/failure')
def failure():
    return render_template("failure.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form["emailId"]
        password = request.form["password"]
        # user = config('user', default='')
        # passwd = config('passwd', default='')
        # DB_CON_URL = f"mongodb+srv://{user}:{passwd}@cluster0.nnfqq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        DB_CON_URL = os.environ.get("MONGO_UAI", None)
        try:
            database = pymongo.MongoClient(DB_CON_URL)
            print("Database connection successful!")

            my_db = database["authentication"]
            coll_name = my_db["signup"]

            cur = coll_name.find({"email": email, "password": password})

            if cur.count() == 1:
                print("record exists")
                return "<h1>login successful</h1>"
            else:
                print("incorrect credentials!")
                return "<h1>Incorrect credentials</h1>"

        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    app.run(debug=True)
