from flask import Flask

# __name__ if we are running the application directly, __main__
app = Flask(__name__)

@app.route('/') # www.mysite.com/api
def hello_method():
    return "Hello, world!"

if __name__ == '__main__':
    app.run()
