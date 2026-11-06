from flask import Flask

app = Flask(__name__)

@app.route('/kitae') # URL 끝에 /가 없는 경우
def doKitae():
    return "<h2>Hello, Kitae</h2>"

@app.route('/jmlee/') # URL 끝에 /가 있는 경우
def doJmlee():
    return "<h2>Hello, Jmlee</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
