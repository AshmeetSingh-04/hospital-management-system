# 🏥 Hospital Management System - Flask Web Application

A simple and professional Hospital (Patient) Management System built using **Python Flask** and **MySQL**, with a clean Bootstrap-styled frontend.

---

## 🚀 Features

✔️ **Admin Login**  
✔️ Add Patient Records  
✔️ View (Display) Records  
✔️ Update Records  
✔️ Delete Records  
✔️ Search Patient (by ID or Name)  
✔️ Fully Responsive Design (using Bootstrap 5)

---

## 🛠️ Tech Stack Used

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Backend**: Python 3, Flask
- **Database**: MySQL
- **Other Tools**: Git, GitHub

---

## 📂 Folder Structure

/Hospital_Management_Web
│
├── app.py
├── templates/
│ ├── add.html
│ ├── delete.html
│ ├── display.html
│ ├── home.html
│ ├── login.html
│ ├── search.html
│ └── update.html
├── static/
│ └── style.css
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

1. **Clone this repo**:
git clone https://github.com/Ashmeet-Singh0409/hospital-management-system.git
cd hospital-management-system


2. **Virtual Environment (optional)**:
python -m venv venv
venv\Scripts\activate # Windows


3. **Install dependencies**:
pip install -r requirements.txt


4. **MySQL Setup**:
CREATE DATABASE SNH_DATABASE;

CREATE TABLE PATIENT_DB (
P_id INT PRIMARY KEY,
P_name VARCHAR(50),
age INT,
Disease VARCHAR(50),
Doc_Incharge VARCHAR(50),
fee INT
);


5. **Run Flask**:
python app.py


6. **View in Browser**:  
http://127.0.0.1:5000/

---

## 🔑 Admin Login:

- **Username**: SNH_ASHMEET  
- **Password**: 0409Ashmeet*

---

## 📄 License

This project is licensed under the MIT License.

---

## 🌐 Author

Made with ❤️ by **Ashmeet Singh**  
[GitHub](https://github.com/Ashmeet-Singh0409) | [LinkedIn](https://www.linkedin.com/in/ashmeet-singh0409/)
