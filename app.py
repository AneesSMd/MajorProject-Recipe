from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import mysql.connector  # type: ignore

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL DB configuration
mydb = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    database='food'
)



# ------------------------ ROUTES ------------------------ #

from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection setup

cursor = mydb.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Support both JSON (AJAX) and form POST
#         if request.is_json:
#             data = request.get_json()
#             email = data.get('email', '').strip()
#             password = data.get('password', '')
#         else:
#             email = request.form.get('email', '').strip()
#             password = request.form.get('password', '')

#         # Debugging output
#         print(f"Login attempt: Email={email}, Password={password}")

#         # Query database for user
#         sql = 'SELECT * FROM users WHERE email = %s'
#         val = (email,)
#         mycur.execute(sql, val)
#         user_data = mycur.fetchone()

#         if user_data:
#             # Adjust column index to match your table structure
#             stored_password = user_data[3]  # Password is 4th column
#             if password == stored_password:
#                 # Set session variables
#                 session['user_email'] = email
#                 session['username'] = user_data[2]  # Username is 3rd column

#                 if request.is_json:
#                     return jsonify({"success": True}), 200
#                 else:
#                     return redirect(url_for('main'))
#             else:
#                 msg = 'Password does not match!'
#                 if request.is_json:
#                     return jsonify({"success": False, "message": msg}), 401
#                 else:
#                     return render_template('login.html', msg=msg)
#         else:
#             msg = 'User with this email does not exist. Please register.'
#             if request.is_json:
#                 return jsonify({"success": False, "message": msg}), 404
#             else:
#                 return render_template('login.html', msg=msg)

#     # Render login page for GET requests
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email', '').strip()
            password = data.get('password', '')
        else:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

        print(f"Login attempt: Email={email}, Password={password}")

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()

            if user_data:
                stored_password = user_data['password']  # Use column name
                if password == stored_password:
                    session['user_email'] = email
                    session['username'] = user_data['username']  # Use column name
                    return redirect(url_for('main'))
                else:
                    msg = 'Password does not match!'
                    return render_template('login.html', msg=msg)
            else:
                msg = 'User with this email does not exist. Please register.'
                return render_template('login.html', msg=msg)
        except Exception as e:
            return render_template('login.html', msg=f"Database error: {str(e)}")

    return render_template('index.html')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     data = request.get_json()  # Accept JSON
#     email = data.get('email')
#     password = data.get('password')

#     query = "SELECT * FROM users WHERE email = %s AND password = %s"
#     cursor.execute(query, (email, password))
#     user = cursor.fetchone()

#     if user:
#         return jsonify({"message": "Login successful!"}), 200
#     else:
#         return jsonify({"message": "Invalid email or password."}), 401


# @app.route('/signup', methods=['POST'])
# def signup():
#     if request.is_json:
#         data = request.get_json()
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         confirm_password = data.get('confirmPassword')
#     else:
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirmPassword')

#     if not all([username, email, password, confirm_password]):
#         msg = 'All fields are required!'
#         return render_template('login.html', msg=msg)

#     if password != confirm_password:
#         msg = 'Passwords do not match!'
#         return render_template('login.html', msg=msg)

#     sql = 'SELECT * FROM users WHERE email=%s'
#     mycur.execute(sql, (email,))
#     existing_user = mycur.fetchone()

#     if existing_user:
#         msg = 'User already registered.'
#         return render_template('login.html', msg=msg)

#     sql = 'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'
#     mycur.execute(sql, (username, email, password))
#     mydb.commit()

#     msg = 'User registered successfully. Please log in.'
#     return render_template('login.html', msg=msg)

@app.route('/signup', methods=['POST'])
def signup():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

    if not all([username, email, password, confirm_password]):
        msg = 'All fields are required!'
        return render_template('login.html', msg=msg)

    if password != confirm_password:
        msg = 'Passwords do not match!'
        return render_template('login.html', msg=msg)

    try:
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = 'User already registered.'
            return render_template('login.html', msg=msg)

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        mydb.commit()  # Use correct connection
        msg = 'User registered successfully. Please log in.'
        return render_template('login.html', msg=msg)
    except Exception as e:
        mydb.rollback()
        return render_template('login.html', msg=f"Database error: {str(e)}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/main')
def main():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))




@app.route('/debug/users')
def debug_users():
    # Only for testing: shows session and dummy users dict
    return jsonify({
        "session": dict(session),
        "dummy_users": {
            "test@example.com": {"password": "1234567", "username": "testuser"}
        }
    })


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
