import re
import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'abcdefgh'

# Database configuration
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student WHERE sname = %s AND sid = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['sid']
            session['username'] = user['sname']
            return redirect(url_for('main_page'))
        else:
            message = 'Incorrect Username or Password!'
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bdate = request.form['bdate']
        dept = request.form['dept'].upper()
        year = request.form['year']
        gpa = request.form['gpa']

        allowed_departments = ['CS', 'EE', 'IE', 'ME', 'CE', 'BIO', 'PH']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM student WHERE sname = %s', (username,))
        account_by_name = cursor.fetchone()
        cursor.execute('SELECT * FROM student WHERE sid = %s', (password,))
        account_by_sid = cursor.fetchone()

        try:
            birthdate = datetime.strptime(bdate, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if account_by_name:
                message = 'Choose a different username!'
            elif account_by_sid:
                message = 'Choose a different password! It must be unique.'
            elif not username or not password or not bdate or not dept or not year or not gpa:
                message = 'Please fill out all fields!'
            elif dept not in allowed_departments:
                message = 'Invalid department selected!'
            elif not (1 <= int(year) <= 4):
                message = 'Year must be between 1 and 4!'
            elif not (0.0 <= float(gpa) <= 4.0):
                message = 'GPA must be between 0.0 and 4.0!'
            elif age < 16:
                message = 'Student must be at least 16 years old!'
            elif age > 100:
                message = 'Invalid birthdate. Too old to register!'
            else:
                cursor.execute('''
                    INSERT INTO student (sid, sname, bdate, dept, year, gpa)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (password, username, bdate, dept, year, gpa))
                mysql.connection.commit()
                message = 'User successfully created!'
        except ValueError:
            message = 'Invalid birthdate format!'

    return render_template('register.html', message=message)

@app.route('/main')
def main_page():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT company.cname, company.city, company.gpa_threshold, company.quota, apply.cid
            FROM apply
            JOIN company ON apply.cid = company.cid
            WHERE apply.sid = %s
        ''', (session['userid'],))
        applications = cursor.fetchall()
        return render_template('main.html', applications=applications)
    return redirect(url_for('login'))

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) AS app_count FROM apply WHERE sid = %s', (session['userid'],))
    app_count = cursor.fetchone()['app_count']

    if app_count >= 3:
        flash('You have already applied to 3 companies. Application limit reached!')
        return redirect(url_for('main_page'))

    cursor.execute('''
        SELECT * FROM company
        WHERE cid NOT IN (SELECT cid FROM apply WHERE sid = %s)
    ''', (session['userid'],))
    companies = cursor.fetchall()

    if request.method == 'POST':
        cid = request.form['cid']
        valid_cids = [company['cid'] for company in companies]

        if cid not in valid_cids:
            flash('Invalid company ID or already applied!')
            return redirect(url_for('apply'))

        cursor.execute('SELECT COALESCE(MAX(app_no), 0) + 1 AS next_app_no FROM apply')
        next_app_no = cursor.fetchone()['next_app_no']
        cursor.execute('INSERT INTO apply (app_no, sid, cid) VALUES (%s, %s, %s)', (next_app_no, session['userid'], cid))
        mysql.connection.commit()

        flash('Application submitted successfully!')
        return redirect(url_for('main_page'))

    return render_template('apply.html', companies=companies)

@app.route('/cancel_application/<cid>', methods=['GET', 'POST'])
def cancel_application(cid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM apply WHERE sid = %s AND cid = %s', (session['userid'], cid))
        mysql.connection.commit()
        flash('Application cancelled.')
        return redirect(url_for('main_page'))
    return redirect(url_for('login'))

@app.route('/summary')
def summary():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()

        cursor.execute('''
            SELECT company.cname, company.quota, company.gpa_threshold
            FROM apply
            JOIN company ON apply.cid = company.cid
            WHERE apply.sid = %s
            ORDER BY company.quota DESC
        ''', (session['userid'],))
        companies_applied = cursor.fetchall()

        cursor.execute('''
            SELECT MAX(gpa_threshold) AS max_gpa_threshold, MIN(gpa_threshold) AS min_gpa_threshold
            FROM apply
            JOIN company ON apply.cid = company.cid
            WHERE apply.sid = %s
        ''', (session['userid'],))
        gpa_thresholds = cursor.fetchone()

        cursor.execute('''
            SELECT company.city, COUNT(*) AS application_count
            FROM apply
            JOIN company ON apply.cid = company.cid
            WHERE apply.sid = %s
            GROUP BY company.city
        ''', (session['userid'],))
        applications_per_city = cursor.fetchall()

        cursor.execute('''
            SELECT cname AS company_with_max_quota
            FROM company
            JOIN apply ON company.cid = apply.cid
            WHERE apply.sid = %s
            ORDER BY quota DESC
            LIMIT 1
        ''', (session['userid'],))
        max_quota_company = cursor.fetchone()

        cursor.execute('''
            SELECT cname AS company_with_min_quota
            FROM company
            JOIN apply ON company.cid = apply.cid
            WHERE apply.sid = %s
            ORDER BY quota ASC
            LIMIT 1
        ''', (session['userid'],))
        min_quota_company = cursor.fetchone()

        return render_template('summary.html',
                               companies_applied=companies_applied,
                               gpa_thresholds=gpa_thresholds,
                               applications_per_city=applications_per_city,
                               max_quota_company=max_quota_company,
                               min_quota_company=min_quota_company)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
