from flask import Flask, session, render_template, request, redirect, url_for, flash
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Email validation regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@app.route('/')
def index():
    return render_template('contact_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']


    email = request.form['email']
    message = request.form['message']


    # Store values in session so we can repopulate them
    session['first_name'] = first_name
    session['last_name'] = last_name
    session['email'] = email
    session['message'] = message
    session['date_of_birth'] = date_of_birth



    if not first_name or not email or not message or not last_name or not date_of_birth:
        flash('All fields are required!')
        return redirect(url_for('index'))

    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        return redirect(url_for('index'))

    if len(message) < 10:
        flash('Message must be at least 10 characters long.')
        return redirect(url_for('index'))

    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []
    submission = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "message": message,
        "date_of_birth": date_of_birth,

    }
    data.append(submission)




    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=4)
    for key in ['first_name', 'last_name', 'email', 'message', 'date_of_birth']:
        session.pop(key, None)

    flash(f'Thank you, {first_name} {last_name}. Your message has been submitted successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

