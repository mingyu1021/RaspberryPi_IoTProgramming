from flask import Flask

app = Flask(__name__) # static/ 디렉터리는 /static/파일이름 으로 자동 서비스됨

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
