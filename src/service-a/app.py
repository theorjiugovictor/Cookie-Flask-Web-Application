from flask import Flask, render_template

app = Flask(__name__)

# Pass the required route to the decorator.
@app.route("/example")
def hello():
    return render_template('example.html')

@app.route("/")
def index():
    return "Homepage of GeeksForGeeks"

if __name__ == "__main__":
    app.run(debug=True)
