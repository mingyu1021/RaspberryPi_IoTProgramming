# 6주차 예제 전체를 한 화면에서 보여주는 대시보드 (포트 8080)
# 각 예제는 run_all.sh가 8081~8093 포트에 띄운다.
from flask import Flask, render_template, request

app = Flask(__name__)

EXAMPLES = [
    (8081, 'hello_flask.py', '기본 Flask 서버', ['/']),
    (8082, '6-1.py', '예제 6-1 웹 서버 만들기', ['/hello/']),
    (8083, '6-2.py', '예제 6-2 URL 라우팅', ['/kitae/', '/jmlee/']),
    (8084, '6-3.py', '예제 6-3 URL 끝의 / 유무', ['/kitae/', '/jmlee/']),
    (8085, '6-4.py', '예제 6-4 정적 콘텐츠', ['/static/image.jpg']),
    (8086, '6-5.py', '예제 6-5 variable 사용', ['/kitae/', '/jmlee/']),
    (8087, '6-6.py', '예제 6-6 은행 계좌', ['/deposit/20000/', '/withdraw/13000/', '/inquiry/']),
    (8088, '6-7.py', '예제 6-7 템플릿 HTML', ['/hello/']),
    (8089, '6-8.py', '예제 6-8 스크립트 템플릿', ['/hello/jmlee/', '/hello/kitae/']),
    (8090, '6-9.py', '예제 6-9 request 객체', ['/search?city=seoul&name=elvis']),
    (8091, '6-10.py', '예제 6-10 GET 사칙연산', ['/calc?op1=100&op=plus&op2=200', '/calc?op1=100&op=div&op2=200']),
    (8092, '6-11.py', '예제 6-11 form GET 전송', ['/']),
    (8093, '6-12.py', '예제 6-12 form POST 전송', ['/']),
]

@app.route('/')
def index():
    return render_template('dashboard.html', examples=EXAMPLES, host=request.host.split(':')[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
