from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__== '__main__': # if we start all our projest starting with main.py
    app.run(debug=True) # show our error on webpage(after deploy-> True)

