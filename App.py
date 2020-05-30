from flask import Flask, url_for, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'flashed message'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'tutorials'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', contacts=data)


@app.route('/insert', methods=['post'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (name,email,phone,address) VALUES (%s,%s,%s,%s)',
                    (name, email, phone, address))
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name_edit']
        email = request.form['email_edit']
        phone = request.form['phone_edit']
        address = request.form['address_edit']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE contacts
               SET name=%s, email=%s, phone=%s, address=%s
               WHERE id=%s
            """, (name, email, phone, address, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
