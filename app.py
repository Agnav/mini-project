from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL


#cursor = connection.cursor()
app = Flask(__name__)
app.secret_key = "your_super_key"

#mysql configuration
app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'parkin'



mysql=MySQL(app)



@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html",username=session['username'])
    else:
        return render_template("index.html")




@app.route('/login', methods=['GET','POST'])
def login():
    book = None  # Define book with a default value of None
    
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            cur = mysql.connection.cursor()
            cur.execute(f"select username,password from user where username = '{username}'")
            user = cur.fetchone()
            cur.close()
            if user and password == user[1]:
                session['username']= user[0]
                return redirect(url_for('index'))
            if username == "admin" and password == "admin@123":
                cur = mysql.connection.cursor()
                cur.execute(f"select username,slot,start,end,id,mail from user")
                data = cur.fetchall()
                cur.execute(f"SELECT COUNT(*) FROM user")
                count = cur.fetchone()
                result = count[0]
                return render_template("admindashboard.html", data=data, count=result, book=book)
            else:
                return render_template('login.html', error='Invalid username or password')

        if 'book' in request.form:
            id = request.form['book']
            cur = mysql.connection.cursor()
            cur.execute(f"select username,slot,start,end,id,mail from user")
            data = cur.fetchall()
            cur.execute(f"SELECT COUNT(*) FROM user")
            count = cur.fetchone()
            result = count[0]
            cur.execute(f"select slot,start,end from user where id = '{id}'")
            check = cur.fetchone()
            cur.execute(f"SELECT COUNT(*) FROM user WHERE id = '{id}'")
            count1 = cur.fetchone()[0]
            cur.close()
            if count1 == 0:
                return render_template("admindashboard.html", error="invalid booking id", book=book, data=data)
            else:
                msg = 'Valid'
                return render_template("admindashboard.html", book=check, data=data ,msg = msg)

    return render_template("login.html", book=book)





@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
         username = request.form['username']
         mail = request.form['mail']
         password = request.form['password']
         dob = request.form['dob']
         cur = mysql.connection.cursor()
         cur.execute(f"SELECT COUNT(*) FROM user WHERE username = '{username}'")
         count = cur.fetchone()[0]
         if count == 0:
            cur.execute(f"insert into user (username, mail, password, date) values ('{username}', '{mail}', '{password}', '{dob}')")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
         else:
             return render_template("signup.html",error="Username already taken")
              
    return render_template("signup.html")




@app.route('/parkmap')
def parkmap():
    return render_template("parkmap.html")




@app.route('/payment', methods=['GET','POST'])
def payment():
    if request.method == 'POST':
         username = session['username']
         slot = request.form['slot']
         start = request.form['start']
         end = request.form['end']
         cur = mysql.connection.cursor()
         cur.execute(f"SELECT COUNT(*) FROM user WHERE slot = '{slot}'")
         count = cur.fetchone()[0]
         if count == 0:
            cur.execute(f"update user set slot = '{slot}', start = '{start}', end = '{end}', id = '{username}{slot}' WHERE username = '{username}'")
            mysql.connection.commit()
            cur.close()
            username = session['username']
            cur = mysql.connection.cursor()
            cur.execute(f"select username,slot,start,end,id from user where username = '{username}'")
            user = cur.fetchone()
            cur.close()
            session['id'] = user[4]
            return render_template("ticket.html",username=session['username'],slot = user[1],start = user[2],end = user[3],id=user[4])
         else:
            return render_template("parkmap.html",error="Slot already Booked")
    username=session['username']
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(id) FROM user where username = '{username}'")
    count = cur.fetchone()[0]
    if count == 0:
             return render_template("ticket.html",error="No bookings")
    else:
             username = session['username']
             cur = mysql.connection.cursor()
             cur.execute(f"select username,slot,start,end,id from user where username = '{username}'")
             user = cur.fetchone()
             cur.close()
             return render_template("ticket.html",username=session['username'],slot = user[1],start = user[2],end = user[3],id=user[4])
    
        
@app.route("/drop" ,methods=['GET','POST'])
def drop():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username=session['username']
        cur.execute(f"UPDATE user SET slot = NULL, start = NULL, end = NULL, id = NULL WHERE username = '{username}'")
        mysql.connection.commit()
        cur.close()
        return render_template("ticket.html",error="No booking")
    return render_template("ticket.html")




@app.route('/logout')
def logout():
     session.pop('username',None)
     return redirect(url_for('index'))

'''@app.route('/loggedin')
def logged():
    return render_template('loggedin.html')'''

if __name__== '__main__':
    app.run(use_reloader=True, debug=True)
