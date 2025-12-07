

#imports from external libraries

from flask import Flask, session,  render_template, request, redirect, url_for, flash, jsonify
import re
import json
import os
import datetime


app = Flask(__name__)
app.secret_key = 'supersecretkey'
spaces=" "
numbers="0123456789"
#creating a regex for the email
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#defining the username and pssword for the admin
admin_password="123"
admin_username="admin"
#creating a phoen regex
PHONE_REGEX = r'^\+?[\d\s\-\(\)]{10,}$'

#cheking if the file regristration.json exists
if os.path.exists('registrations.json'):
    #opening the file and reading it
    with open('registrations.json', 'r') as file:
        #saving the contents to the variable data
        data = json.load(file)
#creating a route to admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        #asking for the username and password.
        username = request.form['username']
        password = request.form['password']
        #cheking it if it maches.
        if username == admin_username and password == admin_password:
            session['admin']=True
            #redirecting the user to view.
            return redirect(url_for('view'))
        #if the password is wront tell the user its incorect
        else: flash('Invalid username or password')
    return render_template('admin.html')
#creating a base route the redirects the user to the form
@app.route('/')
def index():
    return redirect(url_for('form'))

#creating the for page
@app.route('/form')
def form():
    #opening the html file and loding it
    return render_template('contact_form.html')
#creating the submit page
@app.route('/submit', methods=['POST'])
#saving the inputs of the user.
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
        #redirecting the user to the form
        return redirect(url_for('index'))
    #cheking if their birth is larger than what is plausible.
    if dob>old:
        flash('Date of birth is greater than current date')
        # redirecting the user to the form
        return redirect(url_for('index'))
    #checking if the name is writen in plain text without eny spaces or special charecters.
    if  not first_name.isalpha() or not  last_name.isalpha() :

        flash('Please enter your first name and last name corectly.')
        # redirecting the user to the form
        return redirect(url_for('form'))

    #checking if teh name is long enough
    if len(first_name) < 2 or len(last_name) <2:
        flash('Please enter your first name and last name corectly.')
        # redirecting the user to the form
        return redirect(url_for('form'))
    #checks if the email maches teh regex
    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        # redirecting the user to the form
        return redirect(url_for('form'))
    #cheking if teh phone maches teh regex
    if not re.match(PHONE_REGEX, phone_number):
        flash('Please enter a valid phone number.')
        # redirecting the user to the form
        return redirect(url_for('form'))

    #opening the jdon file and writing data to it
    data.append(submission)
    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=4)

    flash(f"Thank you, {first_name} {last_name}. Your message has been submitted successfully!")
    return redirect(url_for('form'))

#creating the view directory
@app.route('/view')
def view():
    #cheking if the admin requirments are satisfied
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
