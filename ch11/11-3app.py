from flask import Flask, render_template, request
app = Flask(__name__)

# 브라우저에게, 캐시에 저장된 자바스크립트 파일의 수명을
# 0으로 설정하여 캐시에 저장된 파일을 사용하지 않도록 지시
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
  return render_template('11-3.html')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
