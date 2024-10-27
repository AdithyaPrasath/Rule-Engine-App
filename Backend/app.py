from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for
from rule_ast import create_rule, evaluate_rule, combine_rules, modify_rule, ast_to_string
import sqlite3
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer



app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Initialize the database and create necessary tables
def init_db():
    conn = sqlite3.connect('rules_database.db')
    cursor = conn.cursor()
    
    # Create rules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL
        )
    ''')
    
    # Create users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE  -- Add email column
        )
    ''')
    
    conn.commit()
    conn.close()

def update_rule_attribute():
    # Connect to the SQLite database
    with sqlite3.connect('rules_database.db') as conn:
        cursor = conn.cursor()

        # Execute the update query
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Age', 'age')")
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Salary', 'salary')")
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Spends', 'spends')")
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Department', 'department')")
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Experience', 'experience')")
        cursor.execute("UPDATE rules SET rule_string = REPLACE(rule_string, 'Name', 'name')")

        # Commit the changes
        conn.commit()

        print("Updated rule_string attribute from 'Age' to 'age' successfully.")
        print("Updated rule_string attribute from 'Salary' to 'salary' successfully.")
        

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login page

# @app.errorhandler(Exception)
# def handle_exception(e):
#     """Handle exceptions and return a generic error message."""
#     if isinstance(e, HTTPException):
#         return jsonify({"success": False, "error": e.description}), e.code
#     return jsonify({"success": False, "error": "An unexpected error occurred."}), 500


@app.before_request
def initialize_database():
    init_db()
    update_rule_attribute()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database and check credentials
        conn = sqlite3.connect('rules_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM user_credentials WHERE username = ?', (username,))
        result = cursor.fetchone()

        # Check if the user exists and password is correct
        if result and check_password_hash(result[0], password):
            session['username'] = username
            return render_template('index.html')  # Redirect to the index page after login
        else:
            flash('Invalid username or password!')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')  # Render the main application page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')  # Get email from the form

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = sqlite3.connect('rules_database.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT id FROM user_credentials WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists! Please choose a different one.')
            return render_template('register.html')

        # Check if the email already exists
        cursor.execute('SELECT id FROM user_credentials WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email already exists! Please use a different one.')
            return render_template('register.html')

        # Insert the new user
        cursor.execute('INSERT INTO user_credentials (username, password, email) VALUES (?, ?, ?)', 
                       (username, hashed_password, email))
        conn.commit()
        conn.close()

        flash('Registration successful! You can now log in.')
        return render_template('login.html')

    return render_template('register.html')

serializer = URLSafeTimedSerializer(app.secret_key)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check if the email exists in the database
        conn = sqlite3.connect('rules_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM user_credentials WHERE email = ?', (email,))
        result = cursor.fetchone()

        if result:
            username = result[0]
            # Generate a reset token and email it
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            send_reset_email(email, username, reset_link)
            flash('A password reset link has been sent to your email.')
        else:
            flash('Email not found.')
        
        return render_template('forgot_password.html')
    return render_template('forgot_password.html')




# Initialize Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change to your email provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adithyaplacement@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'bnnj xpnc uoks hqwm'   # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'adithyaplacement@gmail.com'  # Default sender
mail = Mail(app)


def send_password_email(to_email, username, password):
    msg = Message('Your Password', recipients=[to_email])
    msg.body = f'Hello {username},\n\nYour password is: {password}\n\nBest regards,\nYour Team'
    mail.send(msg)

def send_reset_email(to_email, username, reset_link):
    msg = Message('Password Reset Request', recipients=[to_email])
    msg.body = f'Hello {username},\n\nTo reset your password, click the following link:\n{reset_link}\n\nThis link will expire in 1 hour.\n\nBest regards,\nYour Team'
    mail.send(msg)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify the token and extract email
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        flash('The password reset link is invalid or has expired.')
        return render_template('forgot_password.html')

    if request.method == 'POST':
        new_password = request.form.get('password')
        hashed_password = generate_password_hash(new_password)

        # Update the password in the database
        conn = sqlite3.connect('rules_database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE user_credentials SET password = ? WHERE email = ?', (hashed_password, email))
        conn.commit()
        conn.close()

        flash('Your password has been reset successfully!')
        return render_template('login.html')

    return render_template('reset_password.html')


@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    rule_string = request.json.get('rule_string')
    if not rule_string:
        return jsonify({"success": False, "error": "Missing rule_string"}), 400

    try:
        ast = create_rule(rule_string)
        with sqlite3.connect('rules_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO rules (rule_string) VALUES (?)', (rule_string,))
            rule_id = cursor.lastrowid  # Get the last inserted ID
            conn.commit()
        return jsonify({"success": True, "message": "Rule created", "rule_string": rule_string, "rule_id": rule_id}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    rule_id = request.json.get('rule_id')
    user_data = request.json.get('user_data')

    # Ensure user_data includes required fields
    required_fields = ['name', 'age', 'department', 'salary', 'spends', 'experience']
    for field in required_fields:
        if field not in user_data:
            return jsonify({"success": False, "error": f"Missing field: {field}"}), 400

    with sqlite3.connect('rules_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT rule_string FROM rules WHERE id = ?', (rule_id,))
        result = cursor.fetchone()

    if result:
        rule_string = result[0]
        try:
            ast = create_rule(rule_string)
            is_eligible = evaluate_rule(ast, user_data)  # Evaluate with updated user data
            return jsonify({"success": True, "eligible": is_eligible})
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400
    else:
        return jsonify({"success": False, "error": "Rule not found"}), 404
    
@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    rule_strings = request.json.get('rule_strings')
    print("Rule strings received:", rule_strings)
    if not rule_strings or not isinstance(rule_strings, list):
        return jsonify({"success": False, "error": "Invalid input. Provide a list of rule strings."}), 400

    try:
        combined_ast = combine_rules(rule_strings)
        # Use the to_dict method to serialize the AST
        return jsonify({"success": True, "message": "Rules combined successfully", "ast": combined_ast.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    
@app.route('/modify_rule', methods=['POST'])
def modify_rule_endpoint():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    rule_id = request.json.get('rule_id')
    new_condition = request.json.get('new_condition')

    with sqlite3.connect('rules_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT rule_string FROM rules WHERE id = ?', (rule_id,))
        result = cursor.fetchone()

    if result:
        rule_string = result[0]
        try:
            ast = create_rule(rule_string)
            modified_node = modify_rule(ast, new_condition)
            modified_rule_string = ast_to_string(modified_node)  # Ensure this captures the correct modified rule
            with sqlite3.connect('rules_database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE rules SET rule_string = ? WHERE id = ?', (modified_rule_string, rule_id))
                conn.commit()
            return jsonify({"success": True, "message": "Rule modified", "new_rule_string": modified_rule_string})
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400
    else:
        return jsonify({"success": False, "error": "Rule not found"}), 404

def delete_rule_from_storage(rule_id):
    try:
        with sqlite3.connect('rules_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM rules WHERE id = ?', (rule_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Error deleting rule: {e}")
        return False

@app.route('/delete_rule', methods=['POST'])
def delete_rule():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.json
    rule_id = data.get('rule_id')
    
    if rule_id is None:
        return jsonify({'success': False, 'error': 'Rule ID is required'}), 400
    
    success = delete_rule_from_storage(rule_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Rule deleted successfully'})
    else:
        return jsonify({'success': False, 'error': 'Failed to delete rule'}), 404
    
@app.route('/rules', methods=['GET'])
def get_all_rules():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    with sqlite3.connect('rules_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, rule_string FROM rules')
        rules = cursor.fetchall()

    # Convert rules to a list of dictionaries
    rules_list = [{"id": rule[0], "rule_string": rule[1]} for rule in rules]
    return jsonify(rules_list)

if __name__ == '__main__':
    app.run(debug=True)
