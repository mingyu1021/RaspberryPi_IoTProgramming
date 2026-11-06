from flask import Flask

app = Flask(__name__)

@app.route('/kitae/')
def doKitae():
    return "<h2>Hello, Kitae</h2>"

@app.route('/jmlee/')
def doJmlee():
    return "<h2>Hello, Jmlee</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
