# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# import os
# import pytesseract
# from pdf2image import convert_from_path

# # Initialize app and config
# app = Flask(__name__)
# app.secret_key = 'secretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['UPLOAD_FOLDER'] = 'uploads'

# # Ensure upload folder exists
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# # Tesseract path – update this to your installation path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Database setup
# db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # 'lower' or 'higher'

# # Home route
# @app.route('/')
# def home():
#     return '''
#         <h1>Welcome to Certificate System</h1>
#         <p><a href="/login">Login</a> | <a href="/register">Register</a></p>
#     '''

# # Register route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])
#         role = request.form['role']

#         user = User(username=username, password=password, role=role)
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     return render_template('register.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = user.username
#             session['role'] = user.role
#             if user.role == 'lower':
#                 return redirect('/lower_dashboard')
#             else:
#                 return redirect('/higher_dashboard')
#         else:
#             return "Invalid credentials"
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/login')

# @app.route('/lower_dashboard')
# def lower_dashboard():
#     if session.get('role') == 'lower':
#         return render_template('dashboard_lower.html', username=session['username'])
#     return "Unauthorized", 403

# @app.route('/higher_dashboard')
# def higher_dashboard():
#     if session.get('role') == 'higher':
#         return render_template('dashboard_higher.html', username=session['username'])
#     return "Unauthorized", 403

# # Upload or Manual Entry Route
# @app.route('/upload_pdf', methods=['GET', 'POST'])
# def upload_pdf():
#     if session.get('role') != 'lower':
#         return "Unauthorized", 403

#     name, emp_id = "", ""

#     if request.method == 'POST':
#         submit_type = request.form['submit_type']

#         if submit_type == 'Upload PDF':
#             file = request.files['pdf']
#             if file:
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(filepath)

#                 images = convert_from_path(filepath)
#                 text = ""
#                 for image in images:
#                     text += pytesseract.image_to_string(image)

#                 name, emp_id = extract_name_and_id(text)

#         elif submit_type == 'Submit Manually':
#             name = request.form['manual_name']
#             emp_id = request.form['manual_id']

#         return f'''
#             <h2>Data Extracted/Entered</h2>
#             <b>Name:</b> {name}<br>
#             <b>Employee ID:</b> {emp_id}<br><br>
#             <a href="/upload_pdf">⬅ Back</a>
#         '''

#     return render_template('upload_pdf.html')

# # Helper function to extract from OCR text
# def extract_name_and_id(text):
#     lines = text.split('\n')
#     name, emp_id = "Not Found", "Not Found"
#     for line in lines:
#         if 'Name' in line:
#             name = line.split(':')[-1].strip()
#         elif 'ID' in line or 'Employee ID' in line:
#             emp_id = line.split(':')[-1].strip()
#     return name, emp_id

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)









# from flask import Flask, render_template, request, redirect, url_for, session
# import pytesseract
# from pdf2image import convert_from_path
# import os
# from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'secretkey'

# # Upload and OCR settings
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # 🧠 Set Tesseract and Poppler Paths
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # ✅ Your Tesseract path
# POPPLER_PATH = r'C:\Users\Poshank Markam\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'  # ✅ Your Poppler path

# # Create upload folder if not exists
# try:
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
# except Exception as e:
#     print(f"Error creating upload folder: {e}")

# # ❗🔁 TEMP: Using SQLite now, will switch to MySQL in next phase
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_root_password@localhost/nmdc'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # User model 
# class User(db.Model):
#     __tablename__ = 'user'
#     __table_args__ = {'extend_existing': True}

#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50), nullable=False)
#     role = db.Column(db.Enum('reviewer_one', 'reviewer_two', 'admin'), nullable=False)

# class Department(db.Model):
#     __tablename__ = 'department'
#     dept_id = db.Column(db.Integer, primary_key=True)
#     dept_name = db.Column(db.String(100), unique=True, nullable=False)

# class Employee(db.Model):
#     __tablename__ = 'employee'
#     emp_id = db.Column(db.String(20), primary_key=True)
#     emp_name = db.Column(db.String(50))
#     father_name = db.Column(db.String(50))
#     mother_name = db.Column(db.String(50))
#     sap_id = db.Column(db.String(50), nullable=False)
#     designation = db.Column(db.String(100))
#     dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

# class Training(db.Model):
#     __tablename__ = 'training'
#     training_id = db.Column(db.Integer, primary_key=True)
#     emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'))
#     scheduled_date = db.Column(db.Date)
#     joining_date = db.Column(db.Date)
#     completion_date = db.Column(db.Date)
#     training_name = db.Column(db.String(100))
 
# class VerificationStatus(db.Model):
#     __tablename__ = 'verification_status'
#     certificate_id = db.Column(db.Integer, primary_key=True)
#     emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'))
#     verification_status = db.Column(db.Integer, default=0)
#     training_id = db.Column(db.Integer, db.ForeignKey('training.training_id'))



# @app.route('/')
# def home():
#     return '''<h1>Welcome to Certificate System.</h1> Go to <a href="/login">/login </a>or <a href="/register">/register</a>'''

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])
#         role = request.form['role']

#         user = User(username=username, password=password, role=role)
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = user.username
#             session['role'] = user.role
#             if user.role == 'reviewer_one':
#                 return redirect('/reviewer_one_dashboard')
#             elif user.role == 'reviewer_two':
#                 return redirect('/reviewer_two_dashboard')
#             elif user.role == 'admin':
#                 return redirect('/admin_dashboard')
#             else:
#                 return "Unauthorized role", 403
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/login')

# @app.route('/reviewer_one_dashboard')
# def reviewer_one_dashboard():
#     if session.get('role') == 'reviewer_one':
#         return render_template('dashboard_reviewer_one.html', username=session['username'])
#     return "Unauthorized", 403

# @app.route('/reviewer_two_dashboard')
# def reviewer_two_dashboard():
#     if session.get('role') == 'reviewer_two':
#         return render_template('dashboard_reviewer_two.html', username=session['username'])
#     return "Unauthorized", 403

# @app.route('/admin_dashboard')
# def admin_dashboard():
#     if session.get('role') == 'admin':
#         return render_template('dashboard_admin.html', username=session['username'])
#     return "Unauthorized", 403

# # @app.route('/upload_pdf', methods=['GET', 'POST'])
# # def upload_pdf():
# #     if session.get('role') != 'lower':
# #         return "Unauthorized", 403

# #     name, emp_id, training_status = "", "", ""

# #     if request.method == 'POST':
# #         submit_type = request.form['submit_type']

# #         if submit_type == 'Upload PDF':
# #             file = request.files['pdf']
# #             if file:
# #                 filename = secure_filename(file.filename)
# #                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #                 file.save(filepath)

# #                 # ✅ Use Poppler path to convert PDF to images
# #                 # images = convert_from_path(filepath, poppler_path=POPPLER_PATH)
# #                 images = convert_from_path(
# #                     filepath,
# #                     poppler_path=r'C:\Users\Poshank Markam\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'
# #                 )

# #                 text = ""
# #                 for image in images:
# #                     text += pytesseract.image_to_string(image)


# #                 name, emp_id, training_status = extract_name_id_status(text)

                 
# #         elif submit_type == 'Submit Manually':
# #             name = request.form['manual_name']
# #             emp_id = request.form['manual_id']
# #             training_status = request.form['training_status']

# #         return f'''
# #             <h2>Extracted or Entered Data:</h2>
# #             <b>Name:</b> {name}<br>
# #             <b>Employee ID:</b> {emp_id}<br>
# #             <b>Training Status:</b> {training_status}<br><br>
# #             <a href="/upload_pdf">⬅ Back</a>
# #         '''

# #     return render_template('upload_pdf.html')


# @app.route('/upload_pdf', methods=['GET', 'POST'])
# def upload_pdf():
#     if session.get('role') != 'reviewer_one':
#         return "Unauthorized", 403

#     name, emp_id, training_status, match_result = "", "", "", ""

#     if request.method == 'POST':
#         submit_type = request.form['submit_type']

#         if submit_type == 'Upload PDF':
#             file = request.files['pdf']
#             if file:
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(filepath)

#                 images = convert_from_path(
#                     filepath,
#                     poppler_path=r'C:\Users\Poshank Markam\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'
#                 )
               
#                 text = ""
#                 for image in images:
#                     text += pytesseract.image_to_string(image)


#                 name, emp_id, training_status = extract_name_id_status(text)

#         elif submit_type == 'Submit Manually':
#             name = request.form['manual_name']
#             emp_id = request.form['manual_id']
#             training_status = request.form['training_status']

#         # 🔍 Check MySQL `employee` table for match
#         employee = Employee.query.filter_by(emp_id=emp_id, emp_name=name).first()
#         if employee:
#             match_result = f"""
#                 <h3>✅ Match Found in Database</h3>
#                 <b>Name:</b> {employee.emp_name}<br>
#                 <b>Emp ID:</b> {employee.emp_id}<br>
#                 <b>Designation:</b> {employee.designation}<br>
#             """
#         else:
#             match_result = "<h3>❌ No matching employee found in the system.</h3>"

#         return f'''
#             <h2>Data:</h2>
#             <b>Name:</b> {name}<br>
#             <b>Employee ID:</b> {emp_id}<br>
#             <b>Training Status:</b> {training_status}<br><br>
#             {match_result}<br><br>
#             <a href="/upload_pdf">⬅ Back</a>
#         '''

#     return render_template('upload_pdf.html')


# # def extract_name_and_id(text):
# #     lines = text.split('\n')
# #     name, emp_id = "Not Found", "Not Found"
# #     for line in lines:
# #         if 'Name' in line:
# #             name = line.split(':')[-1].strip()
# #         elif 'ID' in line or 'Employee ID' in line:
# #             emp_id = line.split(':')[-1].strip()
# #     return name, emp_id

# # if __name__ == '__main__':
# #     with app.app_context():
# #         db.create_all()
# #     app.run(debug=True, use_reloader=False)


# def extract_name_id_status(text):
#     lines = text.split('\n')
#     name, emp_id, training_status = "Not Found", "Not Found", "Not Found"

#     for line in lines:
#         line = line.strip()
#         if 'Name' in line:
#             parts = line.split(':')
#             if len(parts) > 1:
#                 name = parts[1].strip()
#         elif 'Employee ID' in line or 'ID' in line:
#             parts = line.split(':')
#             if len(parts) > 1:
#                 emp_id = parts[1].strip()
#         elif 'Training Status' in line:
#             parts = line.split(':')
#             if len(parts) > 1:
#                 training_status = parts[1].strip()

#     return name, emp_id, training_status


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, use_reloader=False)




# from flask import flash, Flask, render_template, request, redirect, url_for, session
# import pytesseract
# from pdf2image import convert_from_path
# import os
# from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'secretkey'

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:poshank%4014database@localhost/nmdc'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# if not os.path.exists('certificates'):
#     os.makedirs('certificates')

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# db = SQLAlchemy(app)

# class User(db.Model):
#     __tablename__ = 'user'
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(512), nullable=False)
#     role = db.Column(db.Enum('reviewer_one', 'reviewer_two', 'admin'))

# class Department(db.Model):
#     __tablename__ = 'department'
#     dept_id = db.Column(db.Integer, primary_key=True)
#     dept_name = db.Column(db.String(100), unique=True, nullable=False)

# class Employee(db.Model):
#     __tablename__ = 'employee'
#     emp_id = db.Column(db.String(20), primary_key=True)
#     emp_name = db.Column(db.String(50))
#     father_name = db.Column(db.String(50))
#     mother_name = db.Column(db.String(50))
#     sap_id = db.Column(db.String(50), nullable=False)
#     designation = db.Column(db.String(100))
#     dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

# class Training(db.Model):
#     __tablename__ = 'training'
#     training_id = db.Column(db.Integer, primary_key=True)
#     emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'))
#     scheduled_date = db.Column(db.Date)
#     joining_date = db.Column(db.Date)
#     completion_date = db.Column(db.Date)
#     training_name = db.Column(db.String(100))

# class VerificationStatus(db.Model):
#     __tablename__ = 'verification_status'
#     certificate_id = db.Column(db.Integer, primary_key=True)
#     emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'))
#     training_id = db.Column(db.Integer, db.ForeignKey('training.training_id'))
#     verification_status = db.Column(db.Integer, default=0)
#     reviewer_one_status = db.Column(db.String(20), default='pending')
#     reviewer_two_status = db.Column(db.String(20), default='pending')

# def generate_certificate(emp_id, training_id):
#     employee = Employee.query.filter_by(emp_id=emp_id).first()
#     training = Training.query.filter_by(training_id=training_id).first()
#     if employee and training:
#         cert_text = f"Certificate of Completion\n\nThis is to certify that {employee.emp_name} (ID: {emp_id}) completed training: {training.training_name} on {training.completion_date}."
#         with open(f"certificates/{emp_id}_{training_id}.txt", "w") as f:
#             f.write(cert_text)

# @app.route('/')
# def home():
#     return '''<h1>Welcome to Certificate System</h1> Go to <a href="/login">Login</a> or <a href="/register">Register</a>'''

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])
#         role = request.form['role']
#         if role == 'lower':
#             role = 'reviewer_one'
#         elif role == 'higher':
#             role = 'reviewer_two'

#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash('Username already exists')
#             return redirect('/register')

#         user = User(username=username, password=password, role=role)
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = user.username
#             session['role'] = user.role
#             if user.role == 'reviewer_one':
#                 return redirect('/reviewer_one_dashboard')
#             elif user.role == 'reviewer_two':
#                 return redirect('/reviewer_two_dashboard')
#             elif user.role == 'admin':
#                 return redirect('/admin_dashboard')
#             else:
#                 return "Unauthorized role", 403
#         else:
#             flash("Invalid credentials")
#             return redirect('/login')
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/login')

# @app.route('/reviewer_one_dashboard')
# def reviewer_one_dashboard():
#     if session.get('role') == 'reviewer_one':
#         return render_template('dashboard_reviewer_one.html', username=session['username'])
#     return redirect(url_for('login'))

# @app.route('/reviewer_two_dashboard')
# def reviewer_two_dashboard():
#     if session.get('role') == 'reviewer_two':
#         return render_template('dashboard_reviewer_two.html', username=session['username'])
#     return redirect(url_for('login'))

# @app.route('/admin_dashboard')
# def admin_dashboard():
#     if session.get('role') != 'admin':
#         return redirect(url_for('login'))
#     employees = Employee.query.all()
#     trainings = Training.query.all()
#     return render_template('admin_dashboard.html', employees=employees, trainings=trainings)

# @app.route('/upload_pdf', methods=['GET', 'POST'])
# def upload_pdf():
#     if session.get('role') not in ['reviewer_one', 'admin']:
#         return redirect(url_for('login'))

#     emp_name = emp_id = training_status = ""
#     if request.method == 'POST':
#         submit_type = request.form['submit_type']
#         if submit_type == 'Upload PDF':
#             file = request.files['pdf']
#             if file:
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(filepath)
#                 images = convert_from_path(
#                     filepath,
#                     poppler_path=r'C:\Users\Poshank Markam\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'
#                 )
#                 text = "".join([pytesseract.image_to_string(image) for image in images])
#                 emp_name, emp_id, training_status = extract_name_id_status(text)
#         else:
#             emp_name = request.form['manual_name']
#             emp_id = request.form['manual_id']
#             training_status = request.form['training_status']

#         employee = Employee.query.filter_by(emp_id=emp_id, emp_name=emp_name).first()
#         print("Searching training for emp_id:", emp_id)

#         training = Training.query.filter_by(emp_id=emp_id).order_by(Training.training_id.desc()).first()
#         print("DEBUG: Training =", training)

#         if training:
#             existing = VerificationStatus.query.filter_by(emp_id=emp_id, training_id=training.training_id).first()
#             if not existing:
#                 verification = VerificationStatus(
#                     emp_id=emp_id,
#                     training_id=training.training_id,
#                     verification_status=0,
#                     reviewer_one_status='pending',
#                     reviewer_two_status='pending'
#                 )
#                 db.session.add(verification)
#                 db.session.commit()
#         else:
#             print("\u26a0\ufe0f Training not found or verification already exists.")

#         verification = VerificationStatus.query.filter_by(emp_id=emp_id).order_by(VerificationStatus.certificate_id.desc()).first()
#         training_id = training.training_id if training else None

#         verification_status = "Matched" if employee else "Unmatched"

#         return render_template(
#             'upload_result.html',
#             emp_name=emp_name,
#             emp_id=emp_id,
#             training_status=training_status,
#             verification_status=verification_status,
#             employee=employee,
#             verification=verification,
#             role=session.get('role'),
#             training_id=training_id
#         )

#     return render_template('upload_pdf.html')

# def extract_name_id_status(text):
#     name = emp_id = training_status = "Not Found"
#     for line in text.split('\n'):
#         line = line.strip()
#         if 'Name' in line:
#             name = line.split(':')[-1].strip()
#         elif 'Employee ID' in line or 'ID' in line:
#             emp_id = line.split(':')[-1].strip()
#         elif 'Training Status' in line:
#             training_status = line.split(':')[-1].strip()
#     return name, emp_id, training_status

# @app.route('/reviewer_one_decision', methods=['POST'])
# def reviewer_one_decision():
#     emp_id = request.form['emp_id']
#     training_id = int(request.form['training_id'])
#     decision = request.form['decision'].lower()

#     verification = VerificationStatus.query.filter_by(emp_id=emp_id, training_id=training_id).first()
#     if verification:
#         verification.reviewer_one_status = 'approved' if decision == 'approve' else 'rejected'
#         db.session.commit()

#     return redirect('/reviewer_one_dashboard')

# @app.route('/reviewer_two_decision', methods=['POST'])
# def reviewer_two_decision():
#     emp_id = request.form['emp_id']
#     training_id = int(request.form['training_id'])
#     decision = request.form['decision'].lower()

#     verification = VerificationStatus.query.filter_by(emp_id=emp_id, training_id=training_id).first()
#     if verification and verification.reviewer_one_status == 'approved' and verification.reviewer_two_status == 'pending':
#         verification.reviewer_two_status = 'approved' if decision == 'approve' else 'rejected'
#         db.session.commit()
#         if verification.reviewer_two_status == 'approved':
#             generate_certificate(emp_id, training_id)
#             flash("Certificate generated and request fully approved.")

#     return redirect('/reviewer_two_dashboard')

# if __name__ == '__main__':
#     with app.app_context():
#         app.run(debug=True, use_reloader=False)import uuid







from flask import flash, Flask, render_template, request, redirect, url_for, session
import pytesseract
from pdf2image import convert_from_path
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:poshank%4014database@localhost/nmdc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists('certificates'):
    os.makedirs('certificates')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), unique=True, nullable=False)

class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = db.Column(db.String(20), primary_key=True)
    emp_name = db.Column(db.String(50))
    father_name = db.Column(db.String(50))
    mother_name = db.Column(db.String(50))
    sap_id = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(100))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

class VerificationStatus(db.Model):
    __tablename__ = 'verification_status'
    certificate_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(50), db.ForeignKey('employee.emp_id'))
    # training_id = db.Column(db.Integer)
    training_status = db.Column(db.String(50))  # or adjust size if needed

    verification_status = db.Column(db.String(20), default='pending')
    reviewer_one_status = db.Column(db.String(20), default='pending')
    reviewer_two_status = db.Column(db.String(20), default='pending')



@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        if role == 'lower':
            role = 'reviewer_one'
        elif role == 'higher':
            role = 'reviewer_two'

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect('/register')

        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['role'] = user.role

            if user.role == 'reviewer_one':
                return redirect('/dashboard_reviewer_one')
            elif user.role == 'reviewer_two':
                return redirect('/dashboard_reviewer_two')
            elif user.role == 'admin':
                return redirect('/admin_dashboard')
            else:
                return "Invalid role assigned."
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/reviewer_one_dashboard')
def reviewer_one_dashboard():
    if session.get('role') == 'reviewer_one':
        return render_template('dashboard_reviewer_one.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/dashboard_reviewer_one')
def dashboard_reviewer_one():
    if 'username' not in session or session.get('role') != 'reviewer_one':
        return redirect('/login')  # Protect the route

    username = session.get('username')
    return render_template('dashboard_reviewer_one.html', username=username)



@app.route('/dashboard_reviewer_two')
def dashboard_reviewer_two():
    if 'username' not in session or session.get('role') != 'reviewer_two':
        return redirect('/login')

    pending_verifications = VerificationStatus.query.filter_by(
        reviewer_one_status='approved',
        reviewer_two_status='pending'
    ).all()

    all_verifications = VerificationStatus.query.filter_by(
        reviewer_one_status='approved'
    ).all()

    return render_template(
        'dashboard_reviewer_two.html',
        username=session['username'],
        pending_verifications=pending_verifications,
        all_verifications=all_verifications
    )


@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    employees = Employee.query.all()
    return render_template('admin_dashboard.html', employees=employees)

@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():
    if session.get('role') not in ['reviewer_one', 'admin']:
        return redirect(url_for('login'))

    emp_name = emp_id = training_status = ""
    
    if request.method == 'POST':
        submit_type = request.form['submit_type']
        
        if submit_type == 'Upload PDF':
            file = request.files['pdf']
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                images = convert_from_path(
                    filepath,
                    poppler_path=r'C:\Users\Poshank Markam\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'
                )
                text = "".join([pytesseract.image_to_string(image) for image in images])
                emp_name, emp_id, training_status = extract_name_id_status(text)

        else:
            # Manual entry
            emp_name = request.form['manual_name']
            emp_id = request.form['manual_id']
            training_status = request.form['training_status']

        emp_id = emp_id.strip() if emp_id else None
        training_status = training_status.strip().lower() if training_status else ""

        employee = Employee.query.filter_by(emp_id=emp_id, emp_name=emp_name).first()
        verification = VerificationStatus.query.filter_by(emp_id=emp_id).first()

        if not employee:
            flash(f"Employee ID {emp_id} not found in database. Cannot proceed.")
            return redirect(url_for('upload_pdf'))

        if not verification:
            verification = VerificationStatus(
                emp_id=emp_id,
                verification_status=0,
                reviewer_one_status='pending',
                reviewer_two_status='pending'
            )
            db.session.add(verification)
            db.session.commit()

        verification_status = "Matched" if employee else "Unmatched"

        return render_template(
            'upload_result.html',
            emp_name=emp_name,
            emp_id=emp_id,
            training_status=training_status,
            verification_status=verification_status,
            employee=employee,
            verification=verification,
            role=session.get('role')
        )

    return render_template('upload_pdf.html')

def extract_name_id_status(text):
    name = emp_id = training_status = "Not Found"
    for line in text.split('\n'):
        line = line.strip()
        if 'Name' in line:
            name = line.split(':')[-1].strip()
        elif 'Employee ID' in line or 'ID' in line:
            emp_id = line.split(':')[-1].strip()
        elif 'Training Status' in line:
            training_status = line.split(':')[-1].strip()
    return name, emp_id, training_status

@app.route('/reviewer_one_decision', methods=['POST'])
def reviewer_one_decision():
    emp_id = request.form['emp_id']
    training_id = request.form.get('training_id')
    decision = request.form['decision'].lower()  # 'approve' or 'reject'

    verification = VerificationStatus.query.filter_by(emp_id=emp_id).first()
    if verification:
        verification.reviewer_one_status = 'approved' if decision == 'approve' else 'rejected'
        
        # If rejected, no need for reviewer two
        if decision == 'reject':
            verification.reviewer_two_status = 'rejected'
        
        db.session.commit()

    return redirect('/reviewer_one_dashboard')



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime

def generate_certificate(emp_id, emp_name, designation):
    # 🔍 Absolute path for debug
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_folder = os.path.join(base_dir, 'static', 'certificates')
    os.makedirs(cert_folder, exist_ok=True)

    cert_path = os.path.join(cert_folder, f"{emp_id}_certificate.pdf")

    print(f"\n[DEBUG] Saving certificate at: {cert_path}\n")

    c = canvas.Canvas(cert_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 160, f"This is to certify that")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 190, emp_name)
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 220, f"(Employee ID: {emp_id})")

    c.drawCentredString(width / 2, height - 260, f"Designation: {designation}")
    c.drawCentredString(width / 2, height - 290, f"has successfully completed the required training.")
    c.drawCentredString(width / 2, height - 340, f"Date: {datetime.now().strftime('%d %B %Y')}")

    c.save()

    # Return relative path for use in template
    return f"static/certificates/{emp_id}_certificate.pdf"



@app.route('/reviewer_two_decision/<emp_id>', methods=['GET', 'POST'])
def reviewer_two_decision(emp_id):
    if session.get('role') != 'reviewer_two':
        flash("Unauthorized access.")
        return redirect(url_for('login'))

    verification = VerificationStatus.query.filter_by(emp_id=emp_id).first()
    if not verification:
        flash("No verification request found.")
        return redirect(url_for('dashboard_reviewer_two'))

    employee = Employee.query.filter_by(emp_id=emp_id).first()

    if request.method == 'POST':
        decision = request.form.get('decision')

        if decision == 'approve':
            verification.reviewer_two_status = 'approved'
            verification.verification_status = 1

            # ✅ Generate certificate and ensure it goes inside /static/certificates/
            if employee:
                cert_path = generate_certificate(
                    emp_id=employee.emp_id,
                    emp_name=employee.emp_name,
                    designation=employee.designation
                )
                flash(f"Certificate generated for {emp_id}.")
            else:
                flash("Employee details missing, but approval saved.")

            db.session.commit()

        elif decision == 'reject':
            verification.reviewer_two_status = 'rejected'
            verification.verification_status = -1
            db.session.commit()
            flash(f"Verification rejected for {emp_id}.")

        else:
            flash("Invalid decision.")

        return redirect(url_for('dashboard_reviewer_two'))

    # Render review page (upload_result.html)
    return render_template('upload_result.html',
                           emp_id=emp_id,
                           emp_name=employee.emp_name if employee else None,
                           training_status='Completed',
                           verification_status='Matched',
                           employee=employee,
                           verification=verification,
                           role='reviewer_two')





if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, use_reloader=False)



@app.route('/reviewer_two_pending')
def reviewer_two_pending():
    if session.get('role') != 'reviewer_two':
        return redirect('/login')
    verifications = VerificationStatus.query.filter_by(reviewer_one_status='approved', reviewer_two_status='pending').all()
    return render_template('reviewer_two_dashboard.html', verifications=verifications)


@app.route('/review_request/<emp_id>')
def review_request(emp_id):
    if 'username' not in session or session.get('role') != 'reviewer_two':
        return redirect('/login')

    employee = Employee.query.filter_by(emp_id=emp_id).first()
    verification = VerificationStatus.query.filter_by(emp_id=emp_id).first()

    if not employee or not verification:
        flash("Employee or verification record not found.")
        return redirect('/dashboard_reviewer_two')

    return render_template('upload_result.html',
                           emp_name=employee.emp_name,
                           emp_id=emp_id,
                           training_status='Completed',  # Or extract from verification if stored
                           verification_status='Matched',  # Based on logic
                           role='reviewer_two',
                           verification=verification,
                           training_id=verification.training_id)



@app.route('/final_approval', methods=['POST'])
def final_approval():
    if 'username' not in session or session.get('role') != 'reviewer_two':
        return redirect('/login')

    emp_id = request.form['emp_id']
    decision = request.form['decision']
    training_id = request.form['training_id']

    verification = VerificationStatus.query.filter_by(emp_id=emp_id).first()
    if not verification:
        flash("Verification record not found.")
        return redirect('/dashboard_reviewer_two')

    if decision == 'approved':
        verification.status = 'fully_approved'

        # Generate certificate logic here (simple example)
        certificate = Certificate(
            emp_id=emp_id,
            training_id=training_id,
            issued_by=session['username']
        )
        db.session.add(certificate)

    elif decision == 'rejected':
        verification.status = 'rejected_by_reviewer_two'

    db.session.commit()
    flash("Decision saved successfully.")
    return redirect('/dashboard_reviewer_two')


