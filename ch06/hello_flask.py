from flask import Flask

app = Flask(__name__) # Flask 객체 생성

@app.route('/') # 라우팅 테이블에 ['/':home] 저장
def home():
    return '<h2>Hello, Flask</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
