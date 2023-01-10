from flask import flash,Flask,redirect,render_template,url_for,request,jsonify,session
import mysql.connector
from flask_session import Session
from secretconfig import secret_key
from py_mail import mail_sender
from email.message import EmailMessage
import smtplib


'''
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD']='sravay'
app.config['MYSQL_DATABASE_DB']='LIBRARY'''
app=Flask(__name__)
app.secret_key='jgjyfjmgjhymgfnb'
app.config['SESSION_TYPE']='filesystem'

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='sravya@99Sree',
    db='website'
    )
Session(app)

'''def background_task():
    with app.app_context():
        while True:
            cursor=mydb.cursor()
            cursor.execute('select id,date from task')
            task=cursor.fetchall()
            #print(data)
            if len(task)==0:
                pass
            else:
                for i in task:
                    today=date.today()
                    current_date=datetime.strptime(f'{str(today.day)}-{str(today.month)}-{str(today.year)}','%d-%m-%Y')
                    due_date=i[1]
                    due_date1=datetime.strptime(f'{str(due_date.day)}-{str(due_date.month)}-{str(due_date.year)}','%d-%m-%Y')
                    
                    mydb.commit()
                    subject=f'remainding task '
                    body=f'you are not submited today is the last date {id1[3]}\n\n\n submit task!'
                    cursor.close()
                    try:
                        mail_sender(email_from,email,subject,body,passcode)
                    except Exception as e:
                        print(e)
                        return render_template('check2.html')'''
                        


        #print(cursor.fetchall())'''
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/adminlogin',methods=['GET','POST'])
def login():
    return render_template('adminlogin.html')
@app.route('/create99',methods=['GET','POST'])
def create():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT count(*) from admin')
    result=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        secret_key=request.form['key']
        user=request.form['user']
        password=request.form['password']
        admin_email=request.form['admin_email']
        passcode=request.form['p_key']
        secret_key=cursor.fetchall()
        cursor.close()
        if (secret_key,) in secret_key:
            flash('This Security code is alredy taken by Faculty')
            return render_template('adminlogin.html')
        else:
            cursor=mydb.cursor()
            cursor.execute('insert into admin values(%s,%s,%s,%s)',[user,password,admin_email,passcode])
            mydb.commit()
            return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/validation',methods=['POST'])
def validation():
    
    if request.method=="POST":
        print(request.form)
        user=request.form['user']
        user=session['id']
        cursor=mydb.cursor()
        cursor.execute('SELECT username from admin')
        users=cursor.fetchall()            
        password=request.form['password']
        cursor.execute('select password from admin where username=%s',[user])
        task=cursor.fetchone()
        cursor.close()
        print(user)
        print(task[0])
        print(task)
        if (user,) in users:
            if password==task[0]:
                session['id']=request.form['user']
                print(session['id'])
                return redirect(url_for('adminpanel'))
            else:
                flash('Invalid Password')
                return redirect(url_for('login'))
        else:
            flash('Invalid user id')
            return redirect(url_for('login'))
@app.route('/adminlogout')
def logoutadmin():
    session.pop('id',None)
    return redirect(url_for('home'))
@app.route('/adminpanel')
def adminpanel():
    cursor=mydb.cursor()
    cursor.execute('SELECT id from task')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('adminpanel.html',tasks=tasks)
@app.route('/create1',methods=['GET','POST'])
def create1():
    cursor=mydb.cursor()
    cursor.execute('SELECT count(*) from empolyee')
    re=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        cursor=mydb.cursor()
        empid=request.form['employeeid']
        cursor.execute('SELECT employeeid from empolyee')
        task=cursor.fetchall()
        cursor.execute('SELECT email from empolyee')
        emails=cursor.fetchall()
        if (empid,) in task:
            flash('Employee id already exists')
            return render_template('signin.html')
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        if (email,) in emails:
            flash('Email is  already exists')
            return render_template('signin.html')
        password=request.form['password']
        phone=request.form['phonenumber']
        cursor.close()
        cursor=mydb.cursor()
        cursor.execute('insert into empolyee values(%s,%s,%s,%s,%s,%s)',[empid,firstname,lastname,email,password,phone])
        mydb.commit()
        return redirect(url_for('home'))
    return render_template('signin.html')

        
@app.route('/taskemployee',methods=['GET','POST'])
def taskemployee():
    if session.get('email'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT employeeid  from empolyee where email=%s',[session['email']])
        data=cursor.fetchone()
        id1=data[0]
        cursor.execute('SELECT * from task where assign_to=%s',[id1])
        tasks=cursor.fetchall()
        print(tasks)
        cursor.close()
        
        return render_template('taskemployee.html',id1=id1,task=tasks)
    return redirect(url_for('employeelogin'))
@app.route('/employeelogin',methods=['GET','POST'])
def employeelogin():
    
    if request.method=="POST":
        email=request.form['email']
        cursor=mydb.cursor()
        cursor.execute('SELECT email from empolyee')
        emails=cursor.fetchall()
        password=request.form['password']
        cursor.execute('select password from empolyee where email=%s',[email])
        task=cursor.fetchone()
        cursor.close()
        if (email,) in emails:
            if password==task[0]:
                session["email"]=request.form['email']
                return redirect(url_for('taskemployee'))
            else:
                flash('Invalid Password')
                return render_template('employeelogin.html')
        else:
            flash('Invalid employee id')
            return render_template('employeelogin.html')
    
    return render_template('employeelogin.html')
@app.route('/logoutemp')
def logout():
    session.pop('email',None)
    return redirect(url_for('home'))

@app.route('/addsuggestion',methods=['GET','POST'])         
def suggestions():
    cursor=mydb.cursor()
    cursor.execute('SELECT * from announcements')
    suggestions=cursor.fetchall()
    if request.method=="POST":
        emp_id=request.form['id']
        name=request.form['name']
        field=request.form['field']
        announcement=request.form['text']
        cursor=mydb.cursor()
        cursor.execute('INSERT INTO announcements values(%s,%s,%s,%s)',[emp_id,name,field, announcement])
        mydb.commit()
        return render_template('announcements.html',suggestions=suggestions)
    return render_template('announcements.html')

@app.route('/delete',methods=['POST'])
def delete():
    if request.method=='POST':
        print(request.form)
        s=request.form['option'].split()
        cursor=mydb.cursor()
        cursor.execute('delete from task where id=%s',[s[0]])
        mydb.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))
@app.route('/addtask',methods=['GET','POST'])
def addtask():
    if request.method=='POST':
        id1=request.form['id']
        name=request.form['name']        
        assign_to=request.form['assign_to']
        duedate=request.form['date']        

        cursor=mydb.cursor()
        id2=session.get('id')
        print(id2)
        
        cursor.execute('insert into task(id,name,assigning_task,task_status ,assign_to,date) values(%s,%s,%s,%s,%s,%s)',[id1,name,id2,'NOT STARTED',assign_to,duedate])
        mydb.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))
    return render_template('addtask.html')
@app.route('/viewtask')
def view():
    cursor=mydb.cursor()
    cursor.execute('SELECT * from task order by date')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('alltasktable.html',tasks=tasks)
@app.route('/viewtask1')
def view1():
    cursor=mydbcursor()
    cursor.execute('SELECT * from task order by date')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('table1.html',tasks=tasks)
        
@app.route('/forgetpassword',methods=['GET','POST'])
def password():
    if request.method=='POST':
        print(request.form)
        key=request.form['key']
        password=request.form['password']
        email=request.form['email']
        passcode=request.form['p_key']
        if key==secret_key:
            cursor=mydb.cursor()
            cursor.execute('update admin set password=%s,email=%s,passcode=%s',[password,email,passcode])
            mydb.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('password'))
    return render_template('secret.html')
@app.route('/password1',methods=['GET','POST'])
def password1():
    if request.method=='POST':
        print(request.form)
        email=request.form['email']
        password=request.form['password']
        if key==secret_key:
            cursor=mydb.cursor()
            cursor.execute('update empolyee set password=%s,email=%s',[password,email])
            mydb.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('password1'))
    return render_template('empforgetpass.html')



@app.route('/update',methods=['POST'])
def update1():
    option1=request.form['id1'].split()[0]
    return redirect(url_for('update',id1=option1))
@app.route('/update/<id1>',methods=['GET','POST'])
def update(id1):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT * FROM task where id=%s',[id1])
    option=cursor.fetchall()
    id1=option[0][0]
    name=option[0][1]
    print(option)
    assign_to=option[0][5]
    print(assign_to)
    date=option[0][3]
    cursor.close()
    if request.method=='POST':
        name2=request.form['name']
        assign_to2=request.form['assign_to']
        date2=request.form['date']
        
        cursor=mydb.cursor()
        cursor.execute('SELECT assigning_task,assign_to from task where id=%s',[id1])
        task=cursor.fetchone()
    
        cursor=mydb.cursor(buffered=True)
        
        cursor.execute('SELECT PASSCODE from admin')
        passcode=cursor.fetchone()[0]
        cursor.execute('SELECT admin_email from admin')
        email=cursor.fetchone()[0]
        
        cursor.execute('update task set name=%s,date=%s,assign_to=%s where id=%s',[name2,date2,assign_to2,id1])
        mydb.commit()
        
        
        subject=f'Task is updated'
        body=f'\nYou completed the task with in time'
        
        try:
            mail_sender(email,subject,body,passcode)
        except Exception as e:
            print(e)
            return render_template('check.html')
        return redirect(url_for('adminpanel'))
    
    return render_template('update.html',name=name,assign_to=assign_to,date=date,id1=id1)

app.run(debug=True)


