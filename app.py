from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret key in production!

# MySQL configuration (Railway)
db_config = {
    'host': 'mysql.railway.internal',
    'user': 'root',
    'password': 'UMuXNmnIAbQYakQHRFfiIyDtXRTuYkTF',
    'database': 'railway',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Admin Credentials
ADMIN_USERNAME = 'SNH_ASHMEET'
ADMIN_PASSWORD = '0409Ashmeet*'

@app.route('/')
def home_redirect():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] == ADMIN_USERNAME and 
            request.form['password'] == ADMIN_PASSWORD):
            session['admin'] = True
            return redirect('/home')
        else:
            flash('Invalid Credentials')
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

@app.route('/home')
def home():
    if 'admin' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if 'admin' not in session:
        return redirect('/login')
    if request.method == 'POST':
        P_id = request.form['P_id']
        P_name = request.form['P_name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']
        
        con = get_db_connection()
        cursor = con.cursor()
        sql = "INSERT INTO PATIENT_DB (P_id, P_name, age, Disease, Doc_Incharge, fee) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (P_id, P_name, age, disease, doctor, fee)
        cursor.execute(sql, val)
        con.commit()
        con.close()
        
        flash('Patient Added Successfully!')
        return redirect('/add')
    return render_template('add.html')

@app.route('/view')
def view_patients():
    if 'admin' not in session:
        return redirect('/login')
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM PATIENT_DB")
    data = cursor.fetchall()
    con.close()
    return render_template('view.html', patients=data)

@app.route('/update', methods=['GET', 'POST'])
def update_patient():
    if 'admin' not in session:
        return redirect('/login')
    if request.method == 'POST':
        P_id = request.form['P_id']
        P_name = request.form['P_name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']
        
        con = get_db_connection()
        cursor = con.cursor()
        sql = "UPDATE PATIENT_DB SET P_name=%s, age=%s, Disease=%s, Doc_Incharge=%s, fee=%s WHERE P_id=%s"
        val = (P_name, age, disease, doctor, fee, P_id)
        cursor.execute(sql, val)
        con.commit()
        con.close()
        
        flash('Patient Updated Successfully!')
        return redirect('/update')
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_patient():
    if 'admin' not in session:
        return redirect('/login')
    if request.method == 'POST':
        P_id = request.form['P_id']
        
        con = get_db_connection()
        cursor = con.cursor()
        sql = "DELETE FROM PATIENT_DB WHERE P_id=%s"
        val = (P_id,)
        cursor.execute(sql, val)
        con.commit()
        con.close()
        
        flash('Patient Deleted Successfully!')
        return redirect('/delete')
    return render_template('delete.html')

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if 'admin' not in session:
        return redirect('/login')
    result = None
    if request.method == 'POST':
        search_by = request.form['search_by']
        search_value = request.form['search_value']
        
        con = get_db_connection()
        cursor = con.cursor()
        
        if search_by == 'P_id':
            sql = "SELECT * FROM PATIENT_DB WHERE P_id=%s"
        else:
            sql = "SELECT * FROM PATIENT_DB WHERE P_name=%s"
        
        val = (search_value,)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        con.close()
    return render_template('search.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
