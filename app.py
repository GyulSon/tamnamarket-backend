from flask import Flask
app = Flask(__name__)

@app.route('/api')
def hello():
    return "팀 귤손의 탐라장터입니다!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

