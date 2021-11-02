from flask import Flask, render_template, request,session,redirect,url_for
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors 
from werkzeug.utils import redirect

app = Flask(__name__, template_folder = 'template', static_folder  = 'static')
app.secret_key="blood_donation"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mitika@03'
app.config['MYSQL_DB'] = 'blood_donation_dbms'

mysql = MySQL(app) 

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user_login" ,methods=['POST','GET'])
def user_login():
    msg = ""
    if request.method=='POST'and "Email_id" in request.form and "Password" in request.form :
        Email_id=request.form['Email_id']
        Password=request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Donor WHERE Email_id=%s AND Password=%s',(Email_id,Password))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['Email_id'] = Email_id
            return render_template('index.html')
        else:
            msg='Incorrect username/password!'    
    return render_template('user_login.html',msg=msg)

@app.route("/user_logout")
def user_logout():
    session.pop('loggedin',None)
    session.pop('Email_id',None)
    return redirect(url_for('user_login'))


    #     Query='''SELECT * FROM Donor WHERE Email_id =%s and password=%s''' ,(email,password)
    #     cur = myconn.cursor()
    #     cur.execute(Query)
    #     Details = cur.fetchone()
    #     if Details:
    #         return 
    #     else :
    #         msg='Incorrect username/password!'    
    # else:    
    #     return render_template('user_login.html')

@app.route("/user_signup",methods=['POST','GET'])
def user_signup():
    msg="Please fill all the elements of the form!"
    if request.method=='POST' and  'First_name' in request.form and 'Gender' in request.form and 'Email_id' in request.form and 'Last_name' in request.form and 'Age' in request.form and 'Phone_num' in request.form and  'Password' in request.form and 'c_password' in request.form and 'Address' in request.form and 'Blood_group' in request.form and 'Eligibility' in request.form and 'Frequent' in request.form and 'City' in request.form and 'District' in request.form and 'State' in request.form and 'Pincode' in request.form :
        First_name=request.form['First_name']
        Last_name=request.form['Last_name']
        Email_id=request.form['Email_id']
        Gender=request.form['Gender']
        Age=request.form['Age']
        Phone_num=request.form['Phone_num']
        Password=request.form['Password']
        c_password=request.form['c_password']
        Address=request.form['Address']
        Blood_group=request.form['Blood_group']
        Eligibility=request.form['Eligibility']
        Frequent=request.form['Frequent']
        City=request.form['City']
        District=request.form['District']
        State=request.form['State']
        Pincode=request.form['Pincode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Donor WHERE Email_id=Email_id')
        account=cursor.fetchone()
        if account :
            msg="An account had been registered with this email"
            return render_template('user_signup.html',msg=msg)
        
        elif (Password != c_password):
            msg="Password and Confirm Password are not matching! "
            return render_template('user_signup_2.html',msg=msg,First_name=First_name,Last_name=Last_name,Email_id=Email_id,Gender=Gender,Age=Age,Phone_num=Phone_num,Password=Password,Address=Address,Blood_group=Blood_group,Eligibility=Eligibility,Frequent=Frequent,City=City,District=District,State=State,Pincode=Pincode)
        
        else:

            cursor.execute('INSERT INTO Donor(First_name,Last_name,Email_id,Age,Phone_num,Password,Address,Blood_group,Eligibility,Frequent,City,District,State,Pincode,Gender) VALUES(%s,%s,%s,%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%d,%s)', (First_name,Last_name,Email_id,Age,Phone_num,Password,Address,Blood_group,Eligibility,Frequent,City,District,State,Pincode,Gender))
            mysql.connection.commit()
            return redirect(url_for('index'))
    return render_template('user_signup.html', msg = msg)

@app.route("/blood_bank_registeration",methods=['POST','GET'])
def blood_bank_registeration():
    msg="Please fill all the elements of the form!"
    if request.method=='POST' and "Blood_bank_name" in request.form and "License_number" in request.form and "Owner_name" in request.form and "Phone_number" in request.form and "Email" in request.form and "Password" in request.form and "c_password" in request.form and "Address" in request.form and "City" in request.form and "Pincode" in request.form and "District" in request.form and "State" in request.form and "Weekday" in request.form and "Opening_time" in request.form and "Closing_time" in request.form and "Website" in request.form :
        details=request.form
        if (details['Password']!=details['c_password']):
            msg="Password and Confirm Password are not matching! "
            return render_template('blood_bank_regis_2.html',msg=msg,Blood_bank_name= details['Blood_bank_name'],License_number=details['License_number'],Owner_name=details['Owner_name'],Phone_number=details['Phone_number'],Email=details['Email'],Password=details['Password'],Address=details['Address'],City=details['City'],Pincode=details['Pincode'],District=details['District'],State=details['State'],Website=details['Website'],Weekday=details['Weekday'],Opening_time=details['Opening_time'],Closing_time=details['Closing_time'],)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.exceute('INSERT INTO Blood_bank(Blood_bank_name,License_number,Owner_name,Phone_number,Email,Password,Address,City,Pincode,District,State,Website) VALUES(%s,%s,%s,%d,%s,%s,%s,%s,%d,%s,%s,%s)',(details['Blood_bank_name'],details['License_number'],details['Owner_name'],details['Phone_number'],details['Email'],details['Password'],details['Address'],details['City'],details['Pincode'],details['District'],details['State'],details['Website']))
            cursor.execute('INSERT INTO Blood_bank_timings(License_number,Weekday,Opening_time,Closing_time) VALUES(%s,%s,%s,%s)', (details['License_number'],details['Weekday'],details['Opening_time'],details['Closing_time']))
            mysql.connection.commit()

    return render_template('blood_bank_regis_me.html')

@app.route("/blood_bank_login",methods=['POST','GET'])
def blood_bank_login():
    msg=''
    if request.method=='POST'and "License_number" in request.form and "Password" in request.form :
        License_number=request.form['License_number']
        Password=request.form['Password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Blood_bank WHERE License_number=%s AND Password=%s',(License_number,Password))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['License_number']=License_number
            return render_template('')
        else:
            msg="Incorrect username/password!"
    return render_template('blood_bank_login.html',msg=msg)        

@app.route("/bank_logout")
def bank_logout():
    session.pop('loggedin',None)
    session.pop('License_number',None)
    return redirect(url_for('blood_bank_login'))


    #     Query='''SELECT * FROM Donor WHERE Email_id =%s and password=%s''' ,(email,password)
    #     cur = myconn.cursor()
    #     cur.execute(Query)
    #     Details = cur.fetchone()
    #     if Details:
    #         return 
    #     else :
    #         msg='Incorrect username/password!'    
    # else:    
    #     return render_template('user_login.html')
    # return render_template('blood_bank_login.html')

@app.route("/check_blood_availability")
def check_blood_availability():
    return render_template('check_blood_availability.html')

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

app.run(debug=True)