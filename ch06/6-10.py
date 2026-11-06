from flask import Flask, request

app = Flask(__name__)

@app.route('/calc')
def calc():
    if request.method != 'GET':
        return ""
    op1 = request.args['op1'] # 'op1' 키에 대한 값
    op2 = request.args['op2'] # 'op2' 키에 대한 값
    op = request.args['op']   # 'op' 키에 대한 값(연산자)
    num1 = int(op1) # 정수로 변환
    num2 = int(op2)
    if op == 'plus':
        return "<h2>%d + %d= %d</h2>" % (num1, num2, num1+num2)
    elif op == 'minus':
        return "<h2>%d - %d= %d</h2>" % (num1, num2, num1-num2)
    elif op == 'mul':
        return "<h2>%d * %d= %d</h2>" % (num1, num2, num1*num2)
    elif op == 'div':
        if num2 == 0:
            return "<h2>0으로 나눌 수 없습니다.</h2>"
        return "<h2>%d / %d= %f</h2>" % (num1, num2, num1/num2)
    else:
        return "<h2>잘못된 연산자입니다.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
