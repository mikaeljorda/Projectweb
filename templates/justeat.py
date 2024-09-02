from flask import Flask

justeat = Flask(__name__)

@justeat.route('/')
def home():
   return'<h1>hola bebe</h1>'

if __name__ == '__main__':
 justeat.run(debug=True,port=3300) 