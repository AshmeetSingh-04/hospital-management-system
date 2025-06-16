from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Railway MySQL Database configuration
db_config = {
    'host': 'mysql.railway.internal',
    'user': 'root',
    'password': 'UMuXNmnIAbQYakQHRFfiIyDtXRTuYkTF',
    'database': 'railway',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'SNH_ASHMEET' and password == '0409Ashmeet*':
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('home.html')
    return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        pid = request.form['pid']
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PATIENT_DB (P_id, P_name, age, Disease, Doc_Incharge, fee) VALUES (%s, %s, %s, %s, %s, %s)",
                       (pid, name, age, disease, doctor, fee))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/display')
    return render_template('add.html')

@app.route('/display')
def display():
    if 'username' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PATIENT_DB")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view.html', rows=rows)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        pid = request.form['pid']
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE PATIENT_DB SET P_name=%s, age=%s, Disease=%s, Doc_Incharge=%s, fee=%s WHERE P_id=%s",
                       (name, age, disease, doctor, fee, pid))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/display')
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        pid = request.form['pid']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PATIENT_DB WHERE P_id=%s", (pid,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/display')
    return render_template('delete.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect('/login')
    rows = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PATIENT_DB WHERE P_id=%s OR P_name=%s", (keyword, keyword))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('search.html', rows=rows)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
