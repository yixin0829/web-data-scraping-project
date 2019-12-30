from flask import Flask, render_template

# Creating the application (i.e. the website)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

@app.route('/plots')
def plot():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

