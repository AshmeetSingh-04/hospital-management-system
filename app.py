from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration for FreeSQLDatabase.com
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12785004",
    password="qPXgYMu5h6",  # Your actual DB password
    database="sql12785004",
    port=3306
)

cursor = db.cursor()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "SNH_ASHMEET" and password == "0409Ashmeet*":
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        pid = request.form['pid']
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']
        
        query = "INSERT INTO PATIENT_DB (P_id, P_name, age, Disease, Doc_Incharge, fee) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (pid, name, age, disease, doctor, fee)
        
        cursor.execute(query, values)
        db.commit()
        
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/view')
def view_patients():
    cursor.execute("SELECT * FROM PATIENT_DB")
    data = cursor.fetchall()
    return render_template('view.html', patients=data)

@app.route('/update', methods=['GET', 'POST'])
def update_patient():
    if request.method == 'POST':
        pid = request.form['pid']
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        doctor = request.form['doctor']
        fee = request.form['fee']

        query = "UPDATE PATIENT_DB SET P_name=%s, age=%s, Disease=%s, Doc_Incharge=%s, fee=%s WHERE P_id=%s"
        values = (name, age, disease, doctor, fee, pid)
        
        cursor.execute(query, values)
        db.commit()
        
        return redirect(url_for('home'))
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_patient():
    if request.method == 'POST':
        pid = request.form['pid']
        
        query = "DELETE FROM PATIENT_DB WHERE P_id=%s"
        values = (pid,)
        
        cursor.execute(query, values)
        db.commit()
        
        return redirect(url_for('home'))
    return render_template('delete.html')

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        search_by = request.form['search_by']
        search_value = request.form['search_value']

        if search_by == 'id':
            query = "SELECT * FROM PATIENT_DB WHERE P_id=%s"
        elif search_by == 'name':
            query = "SELECT * FROM PATIENT_DB WHERE P_name=%s"
        else:
            return render_template('search.html', error="Invalid search criteria")
        
        values = (search_value,)
        cursor.execute(query, values)
        data = cursor.fetchall()
        
        return render_template('search.html', patients=data)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
