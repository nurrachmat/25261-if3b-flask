from flask import Flask, render_template

# Membuat objek aplikasi Flask
app = Flask(__name__)

# Menentukan route untuk halaman utama
@app.route('/')
def hello_world():
    title = "Home Page"
    return render_template('index.html', title=title)

@app.route('/about')
def about():
    title = "About Page"
    return render_template('about.html', title=title)

@app.route('/contact')
def contact():
    title = "Contact Page"
    return render_template('contact.html', title=title)

@app.route('/pmb')
def pmb():
    title = "Penerimaan Mahasiswa Baru"
    return render_template('pmb.html', title=title)

# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
