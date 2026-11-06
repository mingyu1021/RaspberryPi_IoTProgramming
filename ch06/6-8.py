from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<myname>/') # myname은 variable
def hello(myname):
    return render_template('helloWithScript.html', name=myname, dept='Mobile Software')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
