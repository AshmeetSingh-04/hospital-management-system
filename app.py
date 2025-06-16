import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ✅ Final InfinityFree MySQL Database Config:
db = mysql.connector.connect(
    host="sql301.infinityfree.com",
    user="if0_39243875",
    password="0409Ashmeet",
    database="if0_39243875_snhHospital"
)

cursor = db.cursor()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'SNH_ASHMEET' and request.form['password'] == '0409Ashmeet*':
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            age = request.form['age']
            disease = request.form['disease']
            doctor = request.form['doctor']
            fee = request.form['fee']

            sql = "INSERT INTO PATIENT_DB (P_id, P_name, age, Disease, Doc_Incharge, fee) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id, name, age, disease, doctor, fee)
            cursor.execute(sql, val)
            db.commit()
            flash('Patient added successfully.')
            return redirect(url_for('dashboard'))
        return render_template('add.html')
    else:
        return redirect(url_for('login'))

@app.route('/view')
def view():
    if 'username' in session:
        cursor.execute("SELECT * FROM PATIENT_DB")
        data = cursor.fetchall()
        return render_template('view.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            age = request.form['age']
            disease = request.form['disease']
            doctor = request.form['doctor']
            fee = request.form['fee']

            sql = "UPDATE PATIENT_DB SET P_name=%s, age=%s, Disease=%s, Doc_Incharge=%s, fee=%s WHERE P_id=%s"
            val = (name, age, disease, doctor, fee, id)
            cursor.execute(sql, val)
            db.commit()
            flash('Patient updated successfully.')
            return redirect(url_for('dashboard'))
        return render_template('update.html')
    else:
        return redirect(url_for('login'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            sql = "DELETE FROM PATIENT_DB WHERE P_id=%s"
            val = (id,)
            cursor.execute(sql, val)
            db.commit()
            flash('Patient deleted successfully.')
            return redirect(url_for('dashboard'))
        return render_template('delete.html')
    else:
        return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        if request.method == 'POST':
            search_by = request.form['search_by']
            search_value = request.form['search_value']
            if search_by == "id":
                sql = "SELECT * FROM PATIENT_DB WHERE P_id=%s"
            else:
                sql = "SELECT * FROM PATIENT_DB WHERE P_name=%s"
            val = (search_value,)
            cursor.execute(sql, val)
            data = cursor.fetchall()
            return render_template('search.html', data=data)
        return render_template('search.html', data=None)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
