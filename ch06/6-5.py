from flask import Flask

app = Flask(__name__)

@app.route('/<name>/')
def hello(name):
    if name == 'kitae':
        str = "<h2>Hello, Kitae</h2>"
    elif name == 'jmlee':
        str = "<h2>Hello, Jmlee</h2>"
    else:
        str = "" # 빈 내용을 리턴
    return str

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
