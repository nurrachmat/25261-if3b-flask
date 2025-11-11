from flask import Flask, render_template

# Membuat objek aplikasi Flask
app = Flask(__name__)

# Menentukan route untuk halaman utama
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    title = "About Page"
    return render_template('about.html', title=title)

@app.route('/contact')
def contact():
    title = "Contact Page"
    return render_template('contact.html', title=title)

# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
