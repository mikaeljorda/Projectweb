from flask import Flask,render_template,url_for

justeat = Flask(__name__)

@justeat.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
 justeat.run(debug=True,port=3300) 