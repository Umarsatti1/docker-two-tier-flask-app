import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure database connection using environment variables
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = 'message_db'

mysql = MySQL(app)

# Home route that displays the message submission form and messages list
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the message from the form
        message = request.form.get('message')
        
        # Insert the message into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        mysql.connection.commit()
        cur.close()
        
        # Redirect to the home page after submission
        return redirect(url_for('index'))

    # Retrieve all messages from the database to display
    cur = mysql.connection.cursor()
    cur.execute("SELECT content FROM messages")
    messages = cur.fetchall()
    cur.close()
    
    return render_template('index.html', messages=messages)

# Main function to run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
