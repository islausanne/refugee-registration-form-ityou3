from flask import Flask, session,  render_template, request, redirect, url_for, flash, jsonify
import re
import json
import os
import datetime


app = Flask(__name__)
app.secret_key = 'supersecretkey'
spaces=" "
numbers="0123456789"

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
admin_password="123"
admin_username="admin"
PHONE_REGEX = r'^\+?[\d\s\-\(\)]{10,}$'
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

    curent_date = datetime.datetime.now().date() #cauculating the curent date
    old = curent_date - datetime.timedelta(days=365*100) # cauculating if the date is larger than 100

    #turning the date into a string containing year month and day
    dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    #checking if the date inputed is in the future
    if dob > curent_date:
        flash('Date of birth is greater than current date')
        return redirect(url_for('index'))
    #cheking if their birth is larger than what is plausible.
    if dob>old:
        flash('Date of birth is greater than current date')
        return redirect(url_for('index'))
    #checking if the name is writen in plain text without eny spaces or special charecters.
    if  not first_name.isalpha() or not  last_name.isalpha() :
        flash('Please enter your first name and last name corectly.')
        return redirect(url_for('form'))
    if len(first_name) < 2 or len(last_name) <2:
        flash('Please enter your first name and last name corectly.')
        return redirect(url_for('form'))
    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        return redirect(url_for('form'))
    if not re.match(PHONE_REGEX, phone_number):
        flash('Please enter a valid phone number.')
        return redirect(url_for('form'))


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
