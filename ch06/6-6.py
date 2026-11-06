from flask import Flask

app = Flask(__name__)
balance = 0 # 잔액. 초기에는 0원

@app.route('/<op>/<int:money>/') # 2개의 variable: op와 money
def bank(op, money):
    global balance
    if op == 'deposit': # 입금
        balance += money
        return "<h2>입금 %d 원, 잔액 %d</h2>" % (money, balance)
    elif op == 'withdraw':
        # 인출금액이 잔액보다 많으면, 잔액만큼만 인출
        withdraw = balance if balance < money else money
        balance -= withdraw
        return "<h2>출금 %d 원, 잔액 %d</h2>" % (withdraw, balance)
    else:
        return "deposit 또는 withdraw 중 하나를 입력하세요"

@app.route('/inquiry/')
def inquiry():
    return "<h2>잔액 %d </h2>" % (balance)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
