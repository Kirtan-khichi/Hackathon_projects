from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5' 

# MySQL
db = pymysql.connect(
    host='localhost',
    user='root',
    password='0509',
    database='instantin',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

teacher_data = {
    'name': 'John Doe',
    'teacher_id': '123',
    'email': 'john.doe@example.com',
    'subject': 'Math',
}

# @app.route('/')
# def index():
#     return render_template('teacher.html', teacher_data = teacher_data, total_students=23, present_students_today=20, absent_students_today=3, upcoming_events=[{'name':'Math exam', 'data':10-10-23, 'time': '5:00 PM'}], attendance_rate=5, announcements_data=get_announcement_data())

# def get_student_list():
#     # Example student list, replace this with your database query
#     return [{'id': 1, 'name': 'kirtan'}, {'id': 2, 'name': 'sonal'}, {'id': 3, 'name': 'shadab'}]



# @app.route('/mark_attendance', methods=['GET', 'POST'])
# def mark_attendance():
#     student_data = get_student_list()
#     # Create a cursor object and initialize it to None
#     cursor = None
#     try:
#         # Get attendance data from the request
#         data = request.get_json()
#         attendance_data = data.get('attendanceData')

#         # Create a cursor object to execute SQL queries
#         cursor = db.cursor()

#         # Iterate through attendance data and update the database
#         for record in attendance_data:
#             user_id = record['userId']
#             status = record['status']
#             date = datetime.now().strftime('%Y-%m-%d')  # Use the current date and time
#             longitude = record.get('longitude', None)
#             latitude = record.get('latitude', None)
#             class_name = record.get('class', None)

#             # Check if the record already exists
#             cursor.execute("SELECT * FROM attendance WHERE user_id=%s AND DATE(date)", (user_id, date))
#             existing_record = cursor.fetchone()

#             if existing_record:
#                 # Update the status and other fields if the record exists
#                 cursor.execute("UPDATE attendance SET status=%s, longitude=%s, latitude=%s, class=%s WHERE user_id=%s AND date=%s",
#                                (status, longitude, latitude, 'java', user_id, date))
#             else:
#                 # Add a new record if it doesn't exist
#                 cursor.execute("INSERT INTO attendance (user_id, status, date, longitude, latitude, class) VALUES (%s, %s, %s, %s, %s, %s)",
#                                (user_id, status, date, longitude, latitude, class_name))

#         # Commit the changes to the database
#         db.commit()
#         print(jsonify({'message': 'Attendance submitted successfully'}))
        
#     except Exception as e:
#         # Handle any exceptions, log the error, and return an error response
#         return render_template('mark_attendance.html', student_data=student_data, teacher_data=teacher_data)
#     finally:
#         # Close the cursor if it's not None
#         if cursor:
#             cursor.close()

#     return render_template('mark_attendance.html', student_data=student_data, teacher_data=teacher_data)


# def get_attendance_data():
#     # Query your database to get attendance data
#     cursor = db.cursor()
#     cursor.execute("SELECT user_id, status, date FROM attendance ")
#     rows = cursor.fetchall()
#     cursor.close()

#     attendance_data = rows#[{'user_id': user_id, 'status': status, 'date': date} for user_id, status, date in rows]
#     # print(rows)

#     return attendance_data


# @app.route('/attendance_analysis')
# def attendance_analysis():
#     attendance_data = get_attendance_data()
#     return render_template('attendance_analysis.html', attendance_data=attendance_data, teacher_data=teacher_data)

def get_announcement_data():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ANNOUNCEMENT")
    announcements = cursor.fetchall()
    cursor.close()

    return announcements


# @app.route('/add_announcement', methods=['GET', 'POST'])
# def add_announcement():
#     if request.method == 'POST':
#         # Process the form data if needed
#         announcement_text = request.form.get('announcement')
#         # You can handle the announcement data as needed
#         teacher_id = teacher_data['name']
#         subject = teacher_data['subject']
#         # print(announcement_text)
#         cursor=db.cursor()
#         cursor.execute("INSERT INTO ANNOUNCEMENT (teacher_id, message, subject) values( %s, %s, %s)", (teacher_id, announcement_text, subject))
#         db.commit()
#         # For simplicity, just redirect to the Add Announcement page
#         return render_template('add_announcement.html', teacher_data=teacher_data, announcements_data= get_announcement_data())

#     return render_template('add_announcement.html', teacher_data=teacher_data, announcements_data = get_announcement_data())

def is_logged_in():
    return 'is_logged_in' in session

@app.route('/', methods=['GET', 'POST'])
def index():
    is_user_logged_in = is_logged_in()

    # Fetch user data from the database based on the user_id in the session
    user_data1 = None
    if True:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM attendance WHERE user_id=3')
        user_data1 = cursor.fetchall()

        cursor1 = db.cursor()
        cursor1.execute('SELECT * FROM signup WHERE id=1')
        user_data = cursor1.fetchall()
        print(user_data)



    return render_template('index.html', is_logged_in=is_user_logged_in, user_data1=user_data1, user_data = user_data[0], announcements_data=get_announcement_data())

@app.route('/timetable')
def timetable():
    if True:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM TIMETABLE')
        timetableData = cursor.fetchall()

    return render_template('timetable.html', timetableData = timetableData)

@app.route('/exam')
def exam():
    cursor = db.cursor()
    cursor.execute("select * from UPCOMINGEXAM")
    examData = cursor.fetchall()
    print(examData)
    return render_template('exam.html', examData = examData)

@app.route('/password')
def password():
    return render_template('password.html')



##################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check credentials against MySQL database
        cursor = db.cursor()
        cursor.execute('SELECT * FROM SIGNUP WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()

        if user:
            # Authentication successful, set session variables
            session['is_logged_in'] = True
            session['user_id'] = user['id']
            return redirect(url_for('success'))
        else:
            # Authentication failed
            flash('Invalid email or password.')

    return render_template('login.html')


@app.route('/checkin', methods=['GET','POST'])
def checkin():
    # User is logged in, continue with the check-in logic
    data = request.get_json()

    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Get the current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Store the location, date, and time data in the database
    cursor = db.cursor()
    cursor.execute('INSERT INTO LOCATION (user_id, latitude, longitude, date_time, subjects) VALUES (%s, %s, %s, %s, %s)',
                   (2, latitude, longitude, date_time, 'java'))
    db.commit()

    return jsonify({"message": "Checked in successfully!"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    is_logged_in = session.get('is_logged_in', False)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        school_name = request.form['school_name']
        erp_id = request.form['erp_id']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        is_logged_in = 'is_logged_in' in session  # Retrieve is_logged_in from the session

        # Check if the username is already taken
        cursor = db.cursor()
        cursor.execute('SELECT * FROM SIGNUP WHERE username=%s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username is already taken. Please choose another.')
        else:
            # Insert the new user information into the database
            cursor.execute('INSERT INTO SIGNUP (username, password, first_name, middle_name, last_name, gender, school_name, erp_id, mobile_number, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (username, password, first_name, middle_name, last_name, gender, school_name, erp_id, mobile_number, email))
            db.commit()

            flash('Registration successful! You can now log in.')

            # Redirect based on the is_logged_in value
            if is_logged_in:
                return redirect(url_for('checkin'))
            else:
                return redirect(url_for('index'))

    return render_template('register.html', is_logged_in=is_logged_in)

@app.route('/signout')
def signout():
    # Your signout logic here

    session.pop('is_logged_in', None)
    session.pop('user_id', None)
    return 'Signing out'

@app.route('/forgot_password')
def forgot_password():
    # Your forgot password logic here
    return render_template('forgot_password.html')

@app.route('/success')
def success():
    # Add logic to retrieve data from the database and pass it to the template
    cursor = db.cursor()
    cursor.execute('SELECT * FROM LOCATION WHERE user_id=%s', (session['user_id'],))
    location_data = cursor.fetchall()

    return render_template('success.html', location_data=location_data)

if __name__ == '__main__':
    app.run(debug=True)
