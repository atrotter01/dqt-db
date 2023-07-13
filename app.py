from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
   flavor = 'coffee'
   return render_template('index.html', flavor=flavor)

if __name__ == '__main__':
   app.run(debug = True)
