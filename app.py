from flask import Flask, session, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Email validation regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@app.route('/')
def index():
    return render_template('contact_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Store values in session so we can repopulate them
    session['name'] = name
    session['email'] = email
    session['message'] = message

    if not name or not email or not message:
        flash('All fields are required!')
        return redirect(url_for('index'))

    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        return redirect(url_for('index'))

    if len(message) < 10:
        flash('Message must be at least 10 characters long.')
        return redirect(url_for('index'))

    # Clear session values after success
    session.pop('name', None)
    session.pop('email', None)
    session.pop('message', None)

    flash(f'Thank you, {name}. Your message has been submitted successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

