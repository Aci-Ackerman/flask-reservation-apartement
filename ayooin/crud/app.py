from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perhotelan", user="root", passwd="", host="localhost", port=3306, autocommit=True)
    cursor = conn.cursor()

def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        openDb()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        closeDb()
        if user:
            session['email'] = email
            if email == 'admin@gmail.com' and password == 'admin123':
                return redirect(url_for('admin_index'))
            else:
                return redirect(url_for('user_index'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        openDb()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        closeDb()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin_index():
    openDb()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    closeDb()
    return render_template('admin/index.html', bookings=bookings)

@app.route('/user')
def user_index():
    return render_template('user/index.html')

@app.route('/user/home')
def user_home():
    return render_template('user/index.html')

@app.route('/user/room')
def user_room():
    return render_template('user/room.html')

@app.route('/user/contact')
def user_contact():
    return render_template('user/contact.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        no_identitas = request.form['no_identitas']
        nama = request.form['nama']
        no_hp = request.form['no_hp']
        tipe_kamar = request.form['tipe_kamar']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jumlah_kamar = request.form['jumlah_kamar']
        openDb()
        cursor.execute("INSERT INTO bookings (no_identitas, nama, no_hp, tipe_kamar, checkin, checkout, jumlah_kamar) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (no_identitas, nama, no_hp, tipe_kamar, checkin, checkout, jumlah_kamar))
        closeDb()
        flash('Booking berhasil!')
        return redirect(url_for('user_index'))
    return render_template('user/booking.html')

@app.route('/admin/book', methods=['GET', 'POST'])
def admin_book():
    if request.method == 'POST':
        no_identitas = request.form['no_identitas']
        nama = request.form['nama']
        no_hp = request.form['no_hp']
        tipe_kamar = request.form['tipe_kamar']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jumlah_kamar = request.form['jumlah_kamar']
        openDb()
        cursor.execute("INSERT INTO bookings (no_identitas, nama, no_hp, tipe_kamar, checkin, checkout, jumlah_kamar) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (no_identitas, nama, no_hp, tipe_kamar, checkin, checkout, jumlah_kamar))
        closeDb()
        return redirect(url_for('admin_index'))
    return render_template('admin/booking.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    if request.method == 'POST':
        no_identitas = request.form['no_identitas']
        nama = request.form['nama']
        no_hp = request.form['no_hp']
        tipe_kamar = request.form['tipe_kamar']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jumlah_kamar = request.form['jumlah_kamar']
        openDb()
        cursor.execute("UPDATE bookings SET no_identitas=%s, nama=%s, no_hp=%s, tipe_kamar=%s, checkin=%s, checkout=%s, jumlah_kamar=%s WHERE id=%s", 
                       (no_identitas, nama, no_hp, tipe_kamar, checkin, checkout, jumlah_kamar, id))
        closeDb()
        return redirect(url_for('admin_index'))
    openDb()
    cursor.execute("SELECT * FROM bookings WHERE id=%s", (id,))
    booking = cursor.fetchone()
    closeDb()
    return render_template('admin/edit.html', booking=booking)

@app.route('/admin/delete/<int:id>')
def delete_booking(id):
    openDb()
    cursor.execute("DELETE FROM bookings WHERE id=%s", (id,))
    closeDb()
    return redirect(url_for('admin_index'))

@app.route('/admin/print/<int:id>')
def print_booking(id):
    openDb()
    cursor.execute("SELECT * FROM bookings WHERE id=%s", (id,))
    booking = cursor.fetchone()
    closeDb()
    if booking:
        return render_template('admin/print.html', booking=booking)
    return redirect(url_for('admin_index'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
