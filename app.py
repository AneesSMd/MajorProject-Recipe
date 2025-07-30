from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key for sessions

# Simple user database (for demo only - use a real DB in production)
users = {
    "test@example.com": {"password": "1234567", "username": "testuser"}
}

@app.route('/')
def home():
    # Render the index page directly
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Support both JSON (AJAX) and form POST
        if request.is_json:
            data = request.get_json()
            email = data.get('email', '').strip()
            password = data.get('password', '')
        else:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

        # Print for debugging
        print(f"Login attempt: Email={email}, Password={password}")
        print(f"Available users: {users}")
        
        # Check credentials (demo only - insecure!)
        if email in users and users[email]['password'] == password:
            # Store user info in session
            session['user_email'] = email
            session['username'] = users[email]['username']
            
            if request.is_json:
                return jsonify({"success": True}), 200
            else:
                return redirect(url_for('main'))

        # # If login fails
        # if request.is_json:
        #     return jsonify({"success": False, "message": "Invalid credentials"}), 401
        # else:
        #     return render_template('index.html', error="valid credentials")

    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
    
    # Print for debugging
    print(f"Signup attempt: Email={email}, Username={username}, Password={password}")
    
    # Check if email already exists
    if email in users:
        if request.is_json:
            return jsonify({"success": False, "message": "Email already registered"}), 409
        else:
            return render_template('login.html', error="Email already registered")
    
    # Add to "database" (demo only)
    users[email] = {"password": password, "username": username}
    
    # Store user info in session
    session['user_email'] = email
    session['username'] = username
    
    if request.is_json:
        return jsonify({"success": True}), 201
    else:
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    # Clear session data
    session.pop('user_email', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/main')
def main():
    # Check if user is logged in
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/contacts')
def contacts():
    # Check if user is logged in
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('contacts.html')

# Add a debug endpoint to see current users
@app.route('/debug/users')
def debug_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)