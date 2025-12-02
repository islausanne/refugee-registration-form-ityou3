from flask import Flask, session,  render_template, request, redirect, url_for, flash, jsonify
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
spaces=" "
numbers=int
letters=str
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
admin_password="123"
admin_username="admin"

if os.path.exists('registrations.json'):
    with open('registrations.json', 'r') as file:
        data = json.load(file)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin']=True
            return redirect(url_for('view'))
        else: flash('Invalid username or password')
    return render_template('admin.html')
@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form')
def form():
    return render_template('contact_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    sex = request.form['sex']
    country = request.form['country']
    family_size = request.form['family_size']
    email = request.form['email']
    message = request.form['message']
    health_details = request.form.get('health_details', '')
    phone_number = request.form['phone_number']



    # Save submission
    submission = {
        "first_name": first_name.lower(),
        "last_name": last_name.lower(),
        "email": email.lower(),
        "message": message.lower(),
        "date_of_birth": date_of_birth.lower(),
        "sex": sex.lower(),
        "family_size": family_size.lower(),
        "country": country.lower(),
        "health_details": health_details.lower(),
        "phone_number": phone_number.lower(),



    }

    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        return redirect(url_for('form'))
    if first_name and last_name in spaces or numbers :
        flash('Please enter your first and last name.')
    if phone_number in spaces or letters :
        flash('Please enter your phone number.')

    data.append(submission)
    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=4)

    flash(f"Thank you, {first_name} {last_name}. Your message has been submitted successfully!")
    return redirect(url_for('form'))


@app.route('/view')
def view():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            submissions = json.load(file)
    else:
        submissions = []

    return render_template('view_submissions.html', submissions=submissions)


if __name__ == '__main__':
    app.run(debug=True)
