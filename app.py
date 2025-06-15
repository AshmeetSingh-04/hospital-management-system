from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Fetch database credentials from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '!@#$%ashmeet12345'),
    'database': os.getenv('DB_NAME', 'SNH_DATABASE')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname == 'SNH_ASHMEET' and pwd == '0409Ashmeet*':
            session['username'] = uname
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if 'username' in session:
        if request.method == 'POST':
            pid = request.form['P_id']
            name = request.form['P_name']
            age = request.form['age']
            disease = request.form['Disease']
            doctor = request.form['Doc_Incharge']
            fee = request.form['fee']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO PATIENT_DB (P_id, P_name, age, Disease, Doc_Incharge, fee) VALUES (%s, %s, %s, %s, %s, %s)",
                        (pid, name, age, disease, doctor, fee))
            con.commit()
            con.close()
            return redirect(url_for('home'))
        return render_template('add.html')
    return redirect(url_for('login'))

@app.route('/view')
def view_patient():
    if 'username' in session:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM PATIENT_DB")
        data = cur.fetchall()
        con.close()
        return render_template('view.html', patients=data)
    return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update_patient():
    if 'username' in session:
        if request.method == 'POST':
            pid = request.form['P_id']
            name = request.form['P_name']
            age = request.form['age']
            disease = request.form['Disease']
            doctor = request.form['Doc_Incharge']
            fee = request.form['fee']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE PATIENT_DB SET P_name=%s, age=%s, Disease=%s, Doc_Incharge=%s, fee=%s WHERE P_id=%s",
                        (name, age, disease, doctor, fee, pid))
            con.commit()
            con.close()
            return redirect(url_for('home'))
        return render_template('update.html')
    return redirect(url_for('login'))

@app.route('/delete', methods=['GET', 'POST'])
def delete_patient():
    if 'username' in session:
        if request.method == 'POST':
            pid = request.form['P_id']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM PATIENT_DB WHERE P_id=%s", (pid,))
            con.commit()
            con.close()
            return redirect(url_for('home'))
        return render_template('delete.html')
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if 'username' in session:
        if request.method == 'POST':
            search_by = request.form['search_by']
            search_value = request.form['search_value']

            con = get_db_connection()
            cur = con.cursor()
            if search_by == 'P_id':
                cur.execute("SELECT * FROM PATIENT_DB WHERE P_id=%s", (search_value,))
            else:
                cur.execute("SELECT * FROM PATIENT_DB WHERE P_name LIKE %s", ('%' + search_value + '%',))
            data = cur.fetchall()
            con.close()
            return render_template('search.html', patients=data)
        return render_template('search.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
