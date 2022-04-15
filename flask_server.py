from flask import Flask, render_template, request, session, jsonify, flash
# import firebase
from firebase import firebase
# import pyrebase
from pyrebase import pyrebase

import hashlib
import os
import time
import cv2
import numpy as np
import pandas as pd

def read_data(filename):
    data = pd.read_csv(filename)
    return data

review_data = read_data('res_data.csv')
user_data = read_data('user_message.csv')

app = Flask(__name__,static_folder='./static')
#configuration for firebase
CONFIG = {
    "apiKey": "AIzaSyD_TrxwgdFuIZCyYcOwsdeUa6sVtvxreAE",
    "authDomain": "foodreview-a9558.firebaseapp.com",
    "projectId": "foodreview-a9558",
    "databaseURL": "https://foodreview-a9558.firebaseio.com",
    "storageBucket": "foodreview-a9558.appspot.com",
    "messagingSenderId": "1054185588914",
    "appId": "1:1054185588914:web:00d0164a221328916ee1ab",
    "measurementId": "G-1M2XFT74V6"
    # "apiKey": "AIzaSyCs1J_PXXG3HEs1B19YVN7Z-d3JESrui3E",
    # "authDomain": "firebird-7ef02.firebaseapp.com",
    # "databaseURL": "https://firebird-7ef02.firebaseio.com",
    # "projectId": "firebird-7ef02",
    # "storageBucket": "firebird-7ef02.appspot.com",
    # "messagingSenderId": "574864460908",
    # "appId": "1:574864460908:web:c317c3217ae1fcd4899c49",
    # "measurementId": "G-15LBYQ506Y"
}



##------------------------------------------------------------------------------##
##__________________________utility functions______________________




def get_data(pro):
    global review_data
    hotels = []
    data_subset = review_data[review_data['Category'] == pro]
    for name in list(set(data_subset['Restaurant Name'])):
        hdict = {}
        hotel_subset = data_subset[data_subset['Restaurant Name'] == name]
        hdict['Restaurant Name'] = name
        hdict['Address'] = list(hotel_subset['Address'])[0]
        hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
        hdict['image_name'] = os.path.join('res_images', name + '.png')
        # print(hdict['image_name'])
        hotels.append(hdict)
    return hotels


def get_data_single(res):
    global review_data
    hdict = {}
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant Name'] = res
    hdict['Reviews'] = list(hotel_subset['Reviews'])
    hdict['User_email'] = list(hotel_subset['User_email'])
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    # hdict['image'] = cv2.imread(os.path.join('static','res_images', name + '.png'))
    hdict['image_name'] = os.path.join('res_images', res + '.png')
    return hdict



def logincheck(u_email, u_pass):
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    try:
        signin = auth.sign_in_with_email_and_password(u_email, u_pass)
    except Exception as e:
        return False
    return True

def signupcheck(u_dict):
    fb = firebase.FirebaseApplication('https://foodreview-a9558.firebaseio.com/')
    email = u_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    result = None
    # result = fb.get('/{}'.format(sha_email), None)
    if result != None:
        valid = False
        msg = 'Email already exists'
        return valid, msg
    else:
        valid = True
        msg = 'Succesfully created profile'
        return valid, msg

def update_db(user_dict):
    fb = firebase.FirebaseApplication('https://foodreview-a9558.firebaseio.com/')
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    email = user_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    print(sha_email,user_dict,"------------------------------==")
    result = None
    # result = fb.post('/{}'.format(sha_email), user_dict)
    flag = auth.create_user_with_email_and_password(email, user_dict['password'])
    if result != None and flag != None:
        status = True
        return status


##------------------------------------------------------------------------------##
##__________________pages_____________________________
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')

@app.route('/index_page')
def index_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')




@app.route('/login_page')
def login_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('login.html')

@app.route('/about')
def about_page():
    if 'username' in session:
        return render_template('about_loggedin.html', username = session['username'])
    else:
        return render_template('about.html')

@app.route('/contact')
def contact_page():
    if 'username' in session:
        return render_template('contact_loggedin.html', username = session['username'])
    else:
        return render_template('contact.html')



@app.route('/signup_page')
def accounts_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('signup.html')






##________________functional API________________________

@app.route("/bestofmumbai")
def review_MN():
    if 'username' in session:
        data = get_data(1)
        return render_template('bestofmumbai.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/alldaycafe")
def review_NC():
    if 'username' in session:
        data = get_data(2)
        return render_template('alldaycafe.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/kebabs")
def review_WI():
    if 'username' in session:
        data = get_data(3)
        return render_template('kebabs.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/oldisgold")
def review_CT():
    if 'username' in session:
        data = get_data(4)
        return render_template('oldisgold.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/corporate")
def review_VA():
    if 'username' in session:
        data = get_data(5)
        return render_template('corporate.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/streetsavy")
def review_NY():
    if 'username' in session:
        data = get_data(6)
        return render_template('streetsavy.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')


@app.route("/show_info",methods=["POST"])
def show_info():
    if 'username' in session:
        res = request.form['res_name']
        print(res)
        data = get_data_single(res)
        return render_template('show_info.html', data = data, username = session['username'])
    else:
        return render_template('login.html')



@app.route("/logout")
def logout():
    if 'username' in session:
        session['logged_in'] = False
        session.pop('username')
    print(session)
    return render_template('index.html')




@app.route("/login", methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']
    valid = logincheck(email, password)
    if valid:
        session['logged_in'] = True
        session['username'] = email
        print(session)
        return render_template('index_loggedin.html', username = session['username'])
    else:
        flash('Incorrect Username or Password')
        print('Incorrect Username or Password')
        return render_template('login.html')


@app.route("/comment", methods = ['POST'])
def comment():
    global review_data
    hdict = {}
    res = request.form['Restaurant Name']
    hdict['Reviews'] = request.form['Reviews']
    print(res)
    print(hdict['Reviews'])
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant ID'] = list(hotel_subset['Restaurant ID'])[0]
    hdict['Restaurant Name'] = res
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['User_email'] = session['username']
    review_data = review_data.append(hdict, ignore_index = True)
    review_data.to_csv('res_data.csv', index = False)
    data = get_data_single(res)
    print(data)
    return render_template('show_info.html', data = data, username = session['username'])





@app.route("/signup", methods = ['POST'])
def signup():
    user = {}
    user['name'] = request.form['name']
    user['email'] = request.form['email']
    user['password'] = request.form['pass']
    valid, msg = signupcheck(user)
    # valid = True
    # msg = "Success"
    print(valid, msg,'====================================')
    if valid:
        status = update_db(user)
        if status:
            flash(msg)
            print(msg)
            return render_template('login.html')
        else:
            flash('Error in creating profile')
            print('Error in creating profile')
            return render_template('signup.html')
    else:
        flash(msg)
        print(msg)
        return render_template('signup.html')

@app.route("/contactmsg", methods = ['POST'])
def contact():
    global user_data
    user = {}
    user['Name'] = request.form['fname']
    user['Email'] = request.form['email']
    user['Phone'] = request.form['pno']
    user['Message'] = request.form['msg']
    print(user)
    user_data = user_data.append(user, ignore_index = True)
    user_data.to_csv('user_message.csv', index = False)
    return render_template('contact.html')



if __name__ == "__main__":
    app.secret_key = os.urandom(100)
    app.run(host='127.0.0.1', port=5000, debug = True )
