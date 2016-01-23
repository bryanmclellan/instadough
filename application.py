from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Dat Insta Doh -.-"

if __name__ == "__main__":
    app.run()
